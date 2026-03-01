"""Recursive single-elimination tournament simulator."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Callable

from .models import GameResult, Team

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

Decider = Callable[[Team, Team, Team | None], Team]

def _resolve_home_team(spec: dict, team_a: Team, team_b: Team) -> Team | None:
    if spec.get("team_a_is_home"):
        return team_a
    if spec.get("team_b_is_home"):
        return team_b
    return None

def simulate(
    format: list[list[dict]],
    teams: dict[int, Team],
    decide_winner: Decider,
) -> list[list[GameResult]]:
    """Simulate a single-elimination tournament.

    Args:
        format: Bracket structure — list of rounds, each a list of game specs.
        teams: Mapping of seed number to Team.
        decide_winner: Callable(team_a, team_b, home_team) that picks a winner.

    Returns:
        list[list[GameResult]] — one inner list per round, in round order.
    """
    results: list[list[GameResult | None]] = [
        [None] * len(round_games) for round_games in format
    ]

    def _resolve_teams(spec: dict) -> tuple[Team, Team]:
        if "seeds" in spec:
            seed_a, seed_b = spec["seeds"]
            return teams[seed_a], teams[seed_b]
        if "winners_of" in spec:
            r_a, g_a, r_b, g_b = spec["winners_of"]
            return _get_result(r_a, g_a).winner, _get_result(r_b, g_b).winner
        if "seed_vs_winner" in spec:
            seed, r, g = spec["seed_vs_winner"]
            return teams[seed], _get_result(r, g).winner
        raise ValueError(f"Unknown game spec: {spec}")

    def _get_result(round_idx: int, game_idx: int) -> GameResult:
        cached = results[round_idx][game_idx]
        if cached is not None:
            return cached
        spec = format[round_idx][game_idx]
        team_a, team_b = _resolve_teams(spec)
        home_team = _resolve_home_team(spec, team_a, team_b)
        winner = decide_winner(team_a, team_b, home_team)
        result = GameResult(
            team_a=team_a, team_b=team_b, winner=winner, home_team=home_team,
        )
        results[round_idx][game_idx] = result
        return result

    # Drive from the championship (last round, only game) backward via recursion.
    last_round = len(format) - 1
    for game_idx in range(len(format[last_round])):
        _get_result(last_round, game_idx)

    return results  # type: ignore[return-value]


def save_results(
    results: list[list[GameResult]],
    filename: str,
    results_dir: Path = RESULTS_DIR,
) -> Path:
    """Save simulation results to a JSON file.

    Args:
        results: Output from simulate().
        filename: Name for the JSON file (e.g. "cfp_2024.json").
        results_dir: Directory to save into. Created if it doesn't exist.

    Returns:
        Path to the written file.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / filename

    serializable = [
        [asdict(game) for game in round_games]
        for round_games in results
    ]

    with open(out_path, "w") as f:
        json.dump(serializable, f, indent=2)

    return out_path
