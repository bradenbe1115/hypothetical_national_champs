"""Predefined bracket formats for common postseason structures."""

FOUR_TEAM_PLAYOFF = [
    # Round 0: Semifinals
    [
        {"seeds": (1, 4)},
        {"seeds": (2, 3)},
    ],
    # Round 1: Championship
    [
        {"winners_of": (0, 0, 0, 1)},
    ],
]

TWELVE_TEAM_PLAYOFF = [
    # Round 0: First round (seeds 5-12 play; seeds 1-4 have byes)
    [
        {"seeds": (5, 12), "team_a_is_home": True},
        {"seeds": (6, 11), "team_a_is_home": True},
        {"seeds": (7, 10), "team_a_is_home": True},
        {"seeds": (8, 9), "team_a_is_home": True},
    ],
    # Round 1: Quarterfinals (bye teams enter)
    [
        {"seed_vs_winner": (1, 0, 3)},  # seed 1 vs winner of R0G3
        {"seed_vs_winner": (2, 0, 2)},  # seed 2 vs winner of R0G2
        {"seed_vs_winner": (3, 0, 1)},  # seed 3 vs winner of R0G1
        {"seed_vs_winner": (4, 0, 0)},  # seed 4 vs winner of R0G0
    ],
    # Round 2: Semifinals
    [
        {"winners_of": (1, 0, 1, 1)},
        {"winners_of": (1, 2, 1, 3)},
    ],
    # Round 3: Championship
    [
        {"winners_of": (2, 0, 2, 1)},
    ],
]

BCS_CHAMPIONSHIP = [
    # Single game: #1 vs #2
    [
        {"seeds": (1, 2)},
    ],
]
