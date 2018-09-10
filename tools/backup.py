"""
Script that goes to the tripout api endpoints and backs up all data into a JSON file. This file
can then be uploaded using the 'revert' program. Emits to backup.json.
"""
import json
import sys
import requests

def download_pins(root):
    return json.loads(requests.get(root + "/pins/").text)

def download_decals(root):
    return json.loads(requests.get(root + "/decals/").text)

def download_companies(root):
    return json.loads(requests.get(root + "/companies/").text)

def json_out(py_map):
    with open("backup.json", "w") as out:
        json.dump(py_map, out)

if __name__ == "__main__":
    # Get the root that was passed in by the user
    root = sys.argv[1]

    # Download all collections on the api
    pins_collection = download_pins(root)
    decals_collection = download_decals(root)
    companies_collection = download_companies(root)

    # Put into well formed map
    backup = {
        "pins": pins_collection,
        "decals": decals_collection,
        "companies": companies_collection
    }

    # Emit map as JSON.
    json_out(backup)

