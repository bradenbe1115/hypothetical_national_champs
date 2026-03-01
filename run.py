from postseason_simulator import run_series
from postseason_simulator.formats import BCS_CHAMPIONSHIP, TWELVE_TEAM_PLAYOFF, FOUR_TEAM_PLAYOFF
from postseason_simulator.deciders import sp_random

if __name__ == "__main__":
    run_series(BCS_CHAMPIONSHIP, year_poll_ranges=[(2014, 2023, "cfp")], decide_winner=sp_random, series_name="bcs_from_2014_2023", n_simulations=1000)
    run_series(TWELVE_TEAM_PLAYOFF, year_poll_ranges=[[2014,2023, "cfp"]], decide_winner=sp_random, series_name="cfp12_from_2014_2023", n_simulations=1000)
    run_series(FOUR_TEAM_PLAYOFF, year_poll_ranges=[[2007, 2013, "bcs"],[2014,2023, "cfp"]], decide_winner=sp_random, series_name="cfp4_from_2007_2023", n_simulations=1000)
    run_series(TWELVE_TEAM_PLAYOFF, year_poll_ranges=[[2007, 2013, "bcs"],[2014,2023, "cfp"]], decide_winner=sp_random, series_name="cfp12_from_2007_2023", n_simulations=1000)
