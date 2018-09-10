"""
Script that takes all of the items in a backup.json file and uploads them to the tripout API.
"""
import json
import sys
import requests
from requests.auth import HTTPBasicAuth

def upload_pins(root, pins, username, password):
    for pin in pins:
        res = requests.post(root + "/pins/", data = json.dumps(pin), auth=HTTPBasicAuth(username, password))
        print("Uploaded pin with name: {}".format(pin["name"]))

def upload_decals(root, decals, username, password):
    for decal in decals:
        res = requests.post(root + "/decals/", data = json.dumps(decal), auth=HTTPBasicAuth(username, password))
        print("Uploaded decal with url: {}".format(decal["url"]))

def upload_companies(root, companies, username, password):
    for company in companies:
        res = requests.post(root + "/companies/", data = json.dumps(company), auth=HTTPBasicAuth(username, password))
        print("Uploaded company with title: {}".format(company["title"]))

def json_in():
    with open("backup.json", "r") as backup_file:
        return json.load(backup_file)

if __name__ == "__main__":
    # Get the root that was passed in by the user
    try:
        root = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
    except IndexError: 
        print("root url, username and password must be entered to delete tripout db.")
        exit(1)

    # Load in the json
    backup = json_in()

    # Extract the collections
    upload_pins(root, backup["pins"], username, password)
    upload_decals(root, backup["decals"], username, password)
    upload_companies(root, backup["companies"], username, password)


