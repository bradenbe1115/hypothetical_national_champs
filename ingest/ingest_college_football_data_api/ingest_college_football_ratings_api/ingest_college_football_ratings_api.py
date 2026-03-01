import requests
import os
import json
from pathlib import Path

import yaml

REQUIRED_CONFIG_KEYS = {"start_year", "end_year", "endpoint"}

BASE_URL = "https://api.collegefootballdata.com/"

def _headers(api_key: str):
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

def _get(endpoint_url, params, headers):
    response = requests.get(endpoint_url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve results at {endpoint_url} with params {params}")
        return []
    
    return response.json()

def create_full_file_path(repo_root: str, config: dict):
    return f"{repo_root}/db/cfb_data/{config['endpoint']}/{config['start_year']}_{config['end_year']}.json"

def create_year_params_list(start_year: str, end_year: str) -> list[dict]:
    year_params = []
    for year in range(start_year, end_year):
        year_params.append({"year": year})
    
    return year_params

def load_config(repo_root: str, job_name: str) -> dict:
    jobs_dir = Path(repo_root) / "ingest" / "ingest_college_football_data_api" / "ingest_college_football_ratings_api" / "jobs"
    config_path = jobs_dir / f"{job_name}.yml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def validate_config_keys(config: dict) -> None:
    missing = REQUIRED_CONFIG_KEYS - config.keys()
    if missing:
        raise ValueError(f"Config is missing required keys: {', '.join(sorted(missing))}")

def validate_year_range(config: dict) -> None:
    if config["end_year"] <= config["start_year"]:
        raise ValueError(f"end_year ({config['end_year']}) must be after start_year ({config['start_year']})")

def ingest_ratings_api(job_name: str):

    repo_root = os.getenv("NATIONAL_CHAMPS_ROOT")
    if repo_root is None:
        raise RuntimeError("Requried env var NATIONAL_CHAMPS_ROOT is not set.")

    config = load_config(repo_root, job_name)
    if config['endpoint'] is None:
        raise RuntimeError("Paremeter endpoint is not set in config.")
    
    year_params_list = create_year_params_list(config['start_year'], config['end_year'])

    full_url = f"{BASE_URL}{config['endpoint']}"
    print(f"Querying API endpoint at: {full_url}")

    api_key = os.getenv("CFB_DATA_API_KEY")
    if api_key is None:
        raise RuntimeError("Required env var CFB_DATA_API_KEY is not set.")

    headers = _headers(api_key)

    results = []
    for year_param in year_params_list:
        result = _get(full_url, year_param, headers)
        if len(result) > 0:
            results += result
    
    full_file_name = create_full_file_path(repo_root, config)
    Path(full_file_name).parent.mkdir(parents=True, exist_ok=True)

    with open(full_file_name, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"Successfully saved data to {full_file_name}")
