"""Pluggable winner-decision functions."""

from __future__ import annotations

import random

import numpy as np

from .models import Team


def higher_seed_wins(team_a: Team, team_b: Team, home_team: Team | None = None) -> Team:
    """Lower seed number (higher rank) always wins. Deterministic."""
    if team_a.seed is None or team_b.seed is None:
        raise ValueError("Both teams must be seeded")
    return team_a if team_a.seed < team_b.seed else team_b


def coin_flip(team_a: Team, team_b: Team, home_team: Team | None = None) -> Team:
    """Random 50/50."""
    return team_a if random.random() < 0.5 else team_b


def _adjust_sp_for_location(
    team: Team, home_team: Team | None, home_team_adjustment: float = 3.0,
) -> float:
    """Adjust a team's SP rating based on whether they are home, away, or neutral."""
    sp = team.data["sp"]
    if home_team is None:
        return sp
    if team is home_team:
        return sp + home_team_adjustment
    return sp - home_team_adjustment


def sp_random(team_a: Team, team_b: Team, home_team: Team | None = None) -> Team:
    print(team_a.name)
    print(team_b.name)
    team_a_adj_sp = _adjust_sp_for_location(team_a, home_team)
    team_b_adj_sp = _adjust_sp_for_location(team_b, home_team)

    spread = team_a_adj_sp - team_b_adj_sp

    # logit win probability based off: https://dbgriffith01.github.io/blog/2017/02/27/cfb-win-probs
    team_a_win_prob = 1 / (1 + np.exp(-(-.1212 + .1259 * spread)))

    return team_a if random.random() < team_a_win_prob else team_b
