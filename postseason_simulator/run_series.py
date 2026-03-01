"""Orchestrate a series of postseason simulations across multiple years and polls."""

from __future__ import annotations

from pathlib import Path

from .seed_postseason import seed_postseason
from .simulator import Decider, RESULTS_DIR, save_results, simulate


def run_series(
    spec: list[list[dict]],
    year_poll_ranges: list[tuple[int, int, str]],
    decide_winner: Decider,
    series_name: str,
    ratings: str = "sp",
    n_simulations: int = 1,
) -> Path:
    """Run simulations for a range of years and save results.

    Args:
        spec: Bracket format (e.g. TWELVE_TEAM_PLAYOFF).
        year_poll_ranges: List of (start_year, end_year, poll) tuples.
            e.g. [(1999, 2013, "bcs"), (2014, 2024, "cfp")]
        decide_winner: The decider callable.
        series_name: Subfolder name under db/results/ for this series.
        ratings: Ratings source passed to seed_postseason. Defaults to "sp".
        n_simulations: Number of times to simulate each year. Defaults to 1.

    Returns:
        Path to the output directory.
    """
    output_dir = RESULTS_DIR / series_name

    for start_year, end_year, poll in year_poll_ranges:
        for year in range(start_year, end_year + 1):
            teams = seed_postseason(spec, poll, year, ratings)
            year_dir = output_dir / str(year)
            for sim in range(1, n_simulations + 1):
                results = simulate(spec, teams, decide_winner)
                save_results(results, f"{sim}.json", results_dir=year_dir)

    return output_dir
