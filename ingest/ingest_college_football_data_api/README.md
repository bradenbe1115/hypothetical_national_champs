# Ingest College Football Data API

Small service to retrieve data from College Football Data API. https://apinext.collegefootballdata.com/

Querying the API require a free API key that can be obtained from the above link. Set this key to 
an env var CFB_DATA_API_KEY before ingesting data. You'll also need to set the NATIONAL_CHAMPS_ROOT env var
for the path to the repo on your computer.

We set this service up with an eye towards expanding the types of endpoints handled for this API, but we currently only query for ratings data. 

To set up a job to query ratings data from the API, create a config yml file in ingest_college_football_ratings_api/jobs. The only required fields are start_year, end_year, and endpoint. Ratings data for each year from start year to end_year-1 will be retrieved and saved to a file in the db directory.