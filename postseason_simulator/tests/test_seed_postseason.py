"""Tests for seed_postseason using real poll data."""

import pytest
import pandas as pd

from postseason_simulator.formats import BCS_CHAMPIONSHIP, FOUR_TEAM_PLAYOFF, TWELVE_TEAM_PLAYOFF
from postseason_simulator.seed_postseason import (
    calculate_number_of_seeds_in_spec,
    load_all_polls,
    seed_postseason,
    get_final_poll_for_season,
)


# ── calculate_number_of_seeds_in_spec ──────────────────────────────

class TestCalculateSeeds:
    def test_bcs_championship(self):
        assert calculate_number_of_seeds_in_spec(BCS_CHAMPIONSHIP) == 2

    def test_four_team_playoff(self):
        assert calculate_number_of_seeds_in_spec(FOUR_TEAM_PLAYOFF) == 4

    def test_twelve_team_playoff(self):
        # 4 games with "seeds" (8 teams) + 4 games with "seed_vs_winner" (4 teams)
        assert calculate_number_of_seeds_in_spec(TWELVE_TEAM_PLAYOFF) == 12


# ── load_all_polls ─────────────────────────────────────────────────

class TestLoadAllPolls:
    @pytest.fixture(scope="class")
    def polls_df(self):
        return load_all_polls()

    def test_not_empty(self, polls_df):
        assert len(polls_df) > 0

    def test_expected_columns(self, polls_df):
        for col in ("Rk", "School", "Date", "poll", "year"):
            assert col in polls_df.columns

    def test_poll_types(self, polls_df):
        poll_types = set(polls_df["poll"].unique())
        assert {"ap", "bcs", "cfp"} <= poll_types

    def test_year_ranges(self, polls_df):
        ap = polls_df[polls_df["poll"] == "ap"]
        bcs = polls_df[polls_df["poll"] == "bcs"]
        cfp = polls_df[polls_df["poll"] == "cfp"]
        assert ap["year"].min() <= 2000
        assert bcs["year"].max() == 2013
        assert cfp["year"].min() == 2014

class TestGetFinalPollForSeason:
    def test_ap_poll_does_not_use_final(self):
        polls_df = load_all_polls()
        result = get_final_poll_for_season(polls_df[polls_df['poll'] == "ap"], "ap")
        assert len(result[result['Date'] == 'Final']) == 0
        assert len(result) > 0

    def test_other_polls_use_final(self):
        polls_df = load_all_polls()
        result = get_final_poll_for_season(polls_df[polls_df['poll'] == "bcs"], "bcs")
        assert len(result[result['Date'] == 'Final']) > 0
        assert len(result[result['Date'] != 'Final']) == 0

    def test_unknown_poll_raises_error(self):
        with pytest.raises(RuntimeError, match="Unexpected poll"):
            get_final_poll_for_season(pd.DataFrame(), "coaches")


# ── seed_postseason ────────────────────────────────────────────────

class TestSeedPostseason:
    def test_bcs_returns_two_teams(self):
        teams = seed_postseason(BCS_CHAMPIONSHIP, "bcs", 2012)
        assert len(teams) == 2
        assert teams[1].name == "Notre Dame"
        assert teams[2].name == "Alabama"

    def test_four_team_cfp_returns_four_teams(self):
        teams = seed_postseason(FOUR_TEAM_PLAYOFF, "cfp", 2024)
        assert len(teams) == 4
        assert teams[3].name == "Texas"

    def test_twelve_team_cfp_returns_twelve_teams(self):
        teams = seed_postseason(TWELVE_TEAM_PLAYOFF, "cfp", 2025)
        assert len(teams) == 12
        assert teams[10].name == "Miami"
