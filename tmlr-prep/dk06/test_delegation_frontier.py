"""Regression tests for DK-06. Standard library only.

Run from the repository root:
    python3 -B -m unittest -v tmlr-prep/dk06/test_delegation_frontier.py
"""
import importlib.util
import inspect
import pathlib
import random
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


original = _load(
    "harmonized_scoring_v0_4",
    REPO / "datasets/ai-level-bench-v0.4/verifiers/harmonized_scoring.py",
)
fixed = _load("delegation_frontier_cumulative", HERE / "delegation_frontier_cumulative.py")
VERIFIERS = REPO / "datasets/ai-level-bench-v0.4/verifiers"
gui = _load("gui_scoring_v0_4", VERIFIERS / "gui_scoring.py")
memory = _load("memory_scoring_v0_4", VERIFIERS / "memory_scoring.py")
ai_level = _load("ai_level_scoring_v0_4", VERIFIERS / "ai_level_scoring.py")


def policy_frontier(cell_scores, h_band, p, max_t=7):
    """Direct transcription of cumulative_policy.json DI.frontier_law, used as an oracle."""
    h_max = int(h_band[1:])

    def s_net(t):
        vals = [q for (tt, hh), q in cell_scores.items() if tt == t and hh <= h_max]
        return max(vals) if vals else float("-inf")

    passing = [k for k in range(max_t + 1) if min(s_net(j) for j in range(k + 1)) >= p]
    return max(passing) if passing else None


# Non-monotone surface at H1: T2 fails, T3 passes. Paper/policy: frontier is T1.
GAP_SURFACE = {(0, 1): 0.95, (1, 1): 0.90, (2, 1): 0.50, (3, 1): 0.85}


class OriginalHelperDefect(unittest.TestCase):
    """Documents the published defect; expected to keep passing while the snapshot is unchanged."""

    def test_original_skips_failed_lower_band(self):
        self.assertEqual(original.delegation_frontier(GAP_SURFACE, "H1", 0.80), 3)

    def test_original_disagrees_with_policy(self):
        self.assertNotEqual(
            original.delegation_frontier(GAP_SURFACE, "H1", 0.80),
            policy_frontier(GAP_SURFACE, "H1", 0.80),
        )


class CumulativeFrontier(unittest.TestCase):
    def test_failed_lower_band_blocks_higher_pass(self):
        self.assertEqual(fixed.delegation_frontier_cumulative(GAP_SURFACE, "H1", 0.80), 1)

    def test_monotone_surface_matches_original(self):
        surface = {(0, 0): 0.99, (1, 0): 0.95, (2, 0): 0.85, (3, 0): 0.60}
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H0", 0.80), 2)
        self.assertEqual(original.delegation_frontier(surface, "H0", 0.80), 2)

    def test_unmeasured_lower_band_is_not_skipped(self):
        surface = {(0, 1): 0.95, (2, 1): 0.95, (3, 1): 0.95}
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H1", 0.80), 0)

    def test_t0_failure_gives_none(self):
        surface = {(0, 0): 0.40, (1, 0): 0.95}
        self.assertIsNone(fixed.delegation_frontier_cumulative(surface, "H0", 0.80))

    def test_empty_surface_gives_none(self):
        self.assertIsNone(fixed.delegation_frontier_cumulative({}, "H2", 0.80))

    def test_cells_above_ceiling_are_ignored(self):
        surface = {(0, 0): 0.90, (1, 0): 0.90, (2, 3): 0.99}
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H1", 0.80), 1)
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H3", 0.80), 2)

    def test_lower_assistance_cell_counts_under_higher_ceiling(self):
        surface = {(0, 0): 0.90, (1, 2): 0.90}
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H2", 0.80), 1)

    def test_threshold_is_inclusive(self):
        surface = {(0, 1): 0.80, (1, 1): 0.7999}
        self.assertEqual(fixed.delegation_frontier_cumulative(surface, "H1", 0.80), 0)

    def test_randomized_agreement_with_policy_oracle(self):
        rng = random.Random(20260916)
        for _ in range(5000):
            surface = {
                (t, h): round(rng.random(), 2)
                for t in range(8)
                for h in range(6)
                if rng.random() < 0.5
            }
            h_band = f"H{rng.randrange(6)}"
            p = rng.choice([0.5, 0.8, 0.9])
            got = fixed.delegation_frontier_cumulative(surface, h_band, p)
            self.assertEqual(got, policy_frontier(surface, h_band, p), (surface, h_band, p))
            old = original.delegation_frontier(surface, h_band, p)
            if got is not None:
                self.assertLessEqual(got, old)


class OtherPublishedScorers(unittest.TestCase):
    """Pins the behavior of the other public scorers as read for DK-06 (published files unchanged)."""

    def test_gp_gate_cannot_enforce_gp_retention(self):
        # Dataset gui_perception_lattice.json requires K_GP,<g, but gp_gate receives no level or
        # lower-level record, so a GP4 threshold pass is reported regardless of GP0-GP3.
        self.assertEqual(
            inspect.signature(gui.gp_gate).parameters.keys() - {"metrics", "thresholds"}, set()
        )
        self.assertEqual(gui.gp_gate({"P_transition": 0.9}, {"P_transition": 0.8}), 1)

    def test_retention_defaults_to_true_when_omitted(self):
        self.assertEqual(gui.cgui_gate(True), 1)
        self.assertTrue(original.unified_gate({"C": True}, True))
        self.assertEqual(ai_level.i_certification_with_memory("I2", True, "M3")["certified"], 1)

    def test_memory_scorer_does_enforce_no_skipping(self):
        passing = {"q_state": 1, "q_update": 1}
        thresholds = {"q_state_min": 0.5, "q_update_min": 0.5}
        m1_metrics = {"q_dur": 1, "q_prov": 1, "q_abl": 0}
        m1_thresholds = {"q_dur_min": 0.5, "q_prov_min": 0.5, "q_abl_max": 0.1}
        results = {
            "M0": {"level": "M0", "metrics": {"q_state": 0, "q_update": 0}, "thresholds": thresholds},
            "M1": {"level": "M1", "metrics": m1_metrics, "thresholds": m1_thresholds,
                   "retention": {"M0": True}},
        }
        self.assertIsNone(memory.highest_certified(results))
        results["M0"]["metrics"] = passing
        self.assertEqual(memory.highest_certified(results), "M1")

    def test_i_to_m_prerequisites_match_paper_table_7(self):
        table_7 = {"I0": "M0", "I1": "M1", "I2": "M3", "I3": "M4", "I4": "M4", "I5": "M5", "IΩ": "M5"}
        self.assertEqual(ai_level.I_MEMORY_PREREQ, table_7)
        self.assertEqual(
            ai_level.i_certification_with_memory("IΩ", True, "M5", True, True)["required_M"], "MΩ"
        )


if __name__ == "__main__":
    unittest.main()
