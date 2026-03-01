import argparse

from ingest_college_football_ratings_api.ingest_college_football_ratings_api import ingest_ratings_api

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", help="Name of the job config in jobs/ (without .yml)")
    args = parser.parse_args()

    ingest_ratings_api(args.job_name)
