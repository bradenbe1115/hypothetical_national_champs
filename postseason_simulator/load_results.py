"""Load saved simulation results into a pandas DataFrame."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .simulator import RESULTS_DIR


def load_series(series_name: str, results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    """Load all simulation results for a series into a DataFrame.

    Args:
        series_name: The subfolder name under results_dir.
        results_dir: Root results directory. Defaults to db/results.

    Returns:
        DataFrame with columns: year, simulation, round, game, team_a, team_b,
        winner, home_team, is_championship.
    """
    series_dir = results_dir / series_name
    rows = []

    for year_dir in sorted(series_dir.iterdir()):
        if not year_dir.is_dir():
            continue
        year = int(year_dir.name)

        for sim_file in sorted(year_dir.glob("*.json")):
            simulation = int(sim_file.stem)

            with open(sim_file) as f:
                rounds = json.load(f)

            num_rounds = len(rounds)
            for round_idx, round_games in enumerate(rounds):
                is_championship = round_idx == num_rounds - 1
                for game_idx, game in enumerate(round_games):
                    rows.append({
                        "year": year,
                        "simulation": simulation,
                        "round": round_idx,
                        "game": game_idx,
                        "team_a": game["team_a"]["name"],
                        "team_b": game["team_b"]["name"],
                        "winner": game["winner"]["name"],
                        "home_team": game["home_team"]["name"] if game.get("home_team") else None,
                        "is_championship": is_championship,
                    })

    return pd.DataFrame(rows)
