"""Cumulative delegation frontier (DK-06 correction, version dk06-1).

Separately versioned correction for the public helper
``datasets/ai-level-bench-v0.4/verifiers/harmonized_scoring.py::delegation_frontier``,
which returns the largest individually passing T band and does not enforce
lower-band retention. The published snapshot file is intentionally left unchanged.

Rule implemented (``cumulative_policy.json`` -> ``objects.DI.frontier_law``; theory
v2.6 Section 6 note on Eq. (8) and addendum p. 69):

    DF(h, p) = max{ T_k : min_{j<=k} S_net(T_j, H<=h) >= p }

Interpretation choice, to be confirmed by the authors: ``S_net(T_j, H<=h)`` is
read as the best estimate among measured cells (T_j, H') with H' <= h. This keeps
the original helper's H filter and changes only the cumulative T behavior. A band
with no measured cell at or below h counts as not retained, so no band may be
skipped.
"""

VERSION = "dk06-1"


def band_score(cell_scores, t, h_max):
    """Best S_net estimate for band ``t`` among cells with H index <= ``h_max``."""
    scores = [q for (tt, hh), q in cell_scores.items() if tt == t and hh <= h_max]
    return max(scores) if scores else None


def delegation_frontier_cumulative(cell_scores, h_band, p):
    """Largest T index such that every band 0..T meets ``p`` at H <= ``h_band``.

    ``cell_scores`` keys are ``(T_index, H_index)``; values are S_net estimates.
    Returns ``None`` when T0 is not retained.
    """
    h_max = int(h_band[1:])
    frontier = None
    t = 0
    while True:
        q = band_score(cell_scores, t, h_max)
        if q is None or q < p:
            return frontier
        frontier = t
        t += 1
