from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Team:
    """A team in the tournament."""

    name: str
    seed: int | None = None
    data: dict[str, Any] = field(default_factory=dict, compare=False)


@dataclass
class GameResult:
    """The outcome of a single game."""

    team_a: Team
    team_b: Team
    winner: Team
    home_team: Team | None = None
