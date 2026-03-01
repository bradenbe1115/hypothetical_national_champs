# Hypothetical National Champs

This project projects what the national champions in FBS NCAA football would be under different postseason structures. The genesis of this project was the question:

Would Nick Saban have won more or less national titles if the BCS was not replaced? 

## How to run

To run locally, run the make target `make deps`. 

Simulations are set up in `run.py` and can be ran with the make target `make run`. `run_series` is the main entrypoint into creating and running simulations, so supply your arguments to that function as needed.

Simulations are created based on the selected bracket format, the polls used to determine seeding, the decide_winner algorithm, and the ratings system used for the decider algorithms (defaults to sp+).

### Adding Bracket Formats

Bracket formats are specified in `./postseason_simulator/formats.py`. There are formats in that file already that can be used as examples.

### Deciders

Deciders are how winners in matchups are determined. These can be deterministic or probabilistic in nature. The only requirement is that they are a callable that takes two teams as an argument and returns one team as the "winner".

## Data

Real college football polls and advanced ratings data are used in the project. 

SP+ ratings are retrieved from: https://api.collegefootballdata.com/. These can be via through the `ingest_college_football_ratings_api` module. You will need to retrieve an API key from their website and set it as the env var CFB_DATA_API_KEY.

Polls data is manually copied over from College Football Sports Reference. 