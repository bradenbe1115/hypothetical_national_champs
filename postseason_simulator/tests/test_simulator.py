"""Tests for the postseason simulator."""

import pytest

from postseason_simulator.deciders import higher_seed_wins
from postseason_simulator.formats import FOUR_TEAM_PLAYOFF, TWELVE_TEAM_PLAYOFF
from postseason_simulator.models import Team
from postseason_simulator.simulator import simulate, _resolve_home_team


def _make_teams(n: int) -> dict[int, Team]:
    return {i: Team(name=f"Team {i}", seed=i) for i in range(1, n + 1)}


class TestFourTeamPlayoff:
    def test_higher_seed_wins_championship(self):
        teams = _make_teams(4)
        results = simulate(FOUR_TEAM_PLAYOFF, teams, higher_seed_wins)
        assert len(results) == 2
        assert len(results[0]) == 2  # two semis
        assert len(results[1]) == 1  # championship
        champion = results[-1][-1].winner
        assert champion.seed == 1

    def test_correct_semifinal_matchups(self):
        teams = _make_teams(4)
        results = simulate(FOUR_TEAM_PLAYOFF, teams, higher_seed_wins)
        semi_a = results[0][0]
        semi_b = results[0][1]
        assert {semi_a.team_a.seed, semi_a.team_b.seed} == {1, 4}
        assert {semi_b.team_a.seed, semi_b.team_b.seed} == {2, 3}


class TestTwelveTeamPlayoff:
    def test_four_rounds(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        assert len(results) == 4

    def test_bye_teams_absent_from_round_0(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        round_0_seeds = set()
        for game in results[0]:
            round_0_seeds.add(game.team_a.seed)
            round_0_seeds.add(game.team_b.seed)
        for bye_seed in (1, 2, 3, 4):
            assert bye_seed not in round_0_seeds

    def test_higher_seed_wins_championship(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        assert results[-1][-1].winner.seed == 1

    def test_quarterfinal_matchups_with_byes(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        # Seed 1 should face winner of 8v9 (seed 8 wins)
        qf0 = results[1][0]
        assert qf0.team_a.seed == 1
        assert qf0.team_b.seed == 8  # higher seed wins 8v9

    def test_home_team_set_in_round_0(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        for game in results[0]:
            assert game.home_team is game.team_a

    def test_neutral_site_later_rounds(self):
        teams = _make_teams(12)
        results = simulate(TWELVE_TEAM_PLAYOFF, teams, higher_seed_wins)
        for rnd in results[1:]:
            for game in rnd:
                assert game.home_team is None


class TestRecordingDecider:
    def test_matchup_order(self):
        calls = []

        def recording_decider(a: Team, b: Team, home_team: Team | None) -> Team:
            calls.append((a.seed, b.seed))
            return a if a.seed < b.seed else b

        teams = _make_teams(4)
        simulate(FOUR_TEAM_PLAYOFF, teams, recording_decider)
        # Semis resolved first (driven by championship recursion), then final
        assert calls == [(1, 4), (2, 3), (1, 2)]

    def test_home_team_passed_to_decider(self):
        home_teams_seen = []

        def tracking_decider(a: Team, b: Team, home_team: Team | None) -> Team:
            home_teams_seen.append(home_team)
            return a if a.seed < b.seed else b

        teams = _make_teams(12)
        simulate(TWELVE_TEAM_PLAYOFF, teams, tracking_decider)
        # Round 0 has 4 games with home teams, rest are neutral
        assert len([x for x in home_teams_seen if x is not None])==4


class TestUnknownSpec:
    def test_raises_value_error(self):
        bad_format = [[{"bogus": 42}]]
        teams = _make_teams(2)
        with pytest.raises(ValueError, match="Unknown game spec"):
            simulate(bad_format, teams, higher_seed_wins)

@pytest.mark.parametrize(
    ("spec", "team_a", "team_b", "expected_team"),
    [
        (
            {"seeds": (5, 12), "team_a_is_home": True},
            Team(name="a", seed=5),
            Team(name="b", seed=12),
            Team(name="a", seed=5)
        ),

        (
            {"seeds": (5, 12), "team_b_is_home": True},
            Team(name="a", seed=5),
            Team(name="b", seed=12),
            Team(name="b", seed=12)
        ),

        (
            {"seeds": (5, 12)},
            Team(name="a", seed=5),
            Team(name="b", seed=12),
            None
        )
    ]
)
def test_resolve_home_team(spec, team_a, team_b, expected_team):
    home_team = _resolve_home_team(spec, team_a, team_b)
    assert home_team == expected_team
