import pandas as pd
from pathlib import Path
from .models import Team
from .team_mappings import TEAM_MAPPINGS

DB_DIR = Path(__file__).resolve().parent.parent / "db"
DB_POLLS_DIR = DB_DIR / "polls"
DB_RATINGS_DIR = DB_DIR / "cfb_data" / "ratings"


def load_all_polls(polls_dir: Path = DB_POLLS_DIR) -> pd.DataFrame:
    frames = []
    for poll_dir in sorted(polls_dir.iterdir()):
        if not poll_dir.is_dir():
            continue
        poll_type = poll_dir.name
        for csv_file in sorted(poll_dir.glob("*.csv")):
            year = csv_file.stem.split("_")[-1]
            df = pd.read_csv(csv_file)
            df["poll"] = poll_type
            df["year"] = int(year)
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)

def process_polls_school_name(raw_school_value: str):
    """
        Polls data includes team record in school name. This function scrubs that out.
    """
    find_start_of_record = raw_school_value.find('(')
    if find_start_of_record == -1:
        return raw_school_value
    return raw_school_value[0:find_start_of_record-1]


def load_ratings(ratings_dir: str) -> pd.DataFrame:
    """
        Load the first ratings file found in ratings_dir into a pandas Dataframe.
    """
    ratings_path = Path(ratings_dir)
    files = list(ratings_path.iterdir())
    if not files:
        raise FileNotFoundError(f"No files found in {ratings_dir}")
    ratings_file = files[0]
    if ratings_file.suffix == ".json":
        return pd.read_json(ratings_file)
    raise ValueError(f"Unsupported file type: {ratings_file.suffix}")

def calculate_number_of_seeds_in_spec(spec: dict) -> int:

    seeds = 0
    for round in spec:
        for game in round:
            if "seeds" in game.keys():
                seeds += 2
            if "seed_vs_winner" in game.keys():
                seeds += 1
    
    return seeds

def get_final_poll_for_season(polls_df: pd.DataFrame, poll: str) -> pd.DataFrame:
    """
        Return only the final poll results. 

        For BCS and CFP polls, these are the polls when the 'Date' field is set to 'Final'.

        For AP, this is the final poll of the year before the 'Final' poll. We need to find the max data the poll was recorded to return this.
    """

    if poll in ['bcs','cfp']:
        final_polls_df = polls_df[polls_df['Date'] == 'Final']
        return final_polls_df
    
    elif poll in ['ap']:
        intermediate_polls_df = polls_df[polls_df['Date'] != 'Final']
        max_date = intermediate_polls_df['Date'].max()
        final_polls_df = polls_df[polls_df['Date'] == max_date]
        return final_polls_df
    
    else:
        raise RuntimeError(f"Unexpected poll of {poll}. Do not know how to handle final poll.")
    

def seed_postseason(spec: dict, poll: str, year: str, ratings: str = "sp") -> dict[int, Team]:
    polls_df = load_all_polls()
    ratings_df = load_ratings(DB_RATINGS_DIR / ratings)
    
    # filter to only the poll we want to use
    filtered_polls_df = polls_df[(polls_df['poll'] == poll) & (polls_df['year'] == year)]

    # we want the final poll unless it's from ap since that includes postseason results
    final_polls_df = get_final_poll_for_season(filtered_polls_df, poll)
    final_polls_df.reset_index(drop=True, inplace=True)
    
    # remove record from school name
    final_polls_df['clean_school_name'] = final_polls_df.apply(lambda row: process_polls_school_name(row['School']),axis=1)
    
    # find number of seeds needed and populate team list
    seeds_in_format = calculate_number_of_seeds_in_spec(spec)
    teams = {}
    for i in range(1, seeds_in_format+1):
        team_name = final_polls_df[final_polls_df['Rk'] == i]['clean_school_name'].iloc[0]

        team_rating_lookup = ratings_df[(ratings_df['team'] == TEAM_MAPPINGS.get(team_name, team_name)) & (ratings_df['year'] == year)]
        if len(team_rating_lookup) > 0:
            team_rating = float(team_rating_lookup['rating'].iloc[0])
        else:
            team_rating = None
        teams[i] = Team(name=team_name, seed=i, data={ratings:team_rating})

    return teams



