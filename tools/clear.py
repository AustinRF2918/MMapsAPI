"""
Script that clears a tripout database. Following the use of this, we can use the revert script to
revert the database from a backup (backup.py/backup.json)
"""
import json
import sys
import requests
from requests.auth import HTTPBasicAuth

def clear_pins(root, username, password):
    pins = json.loads(requests.get(root + "/pins/").text)

    for el in pins:
        res = requests.delete(root + "/pins/" + el["_id"], auth=HTTPBasicAuth(username, password))
        if res.status_code == 401:
            print("Couldn't delete! authentication failed!")
            exit(2)
        print("Deleted pin with id: {}".format(el["_id"]))

def clear_decals(root, username, password):
    decals = json.loads(requests.get(root + "/decals/").text)

    for el in decals:
        res = requests.delete(root + "/decals/" + el["_id"], auth=HTTPBasicAuth(username, password))
        if res.status_code == 401:
            print("Couldn't delete! authentication failed!")
            exit(2)
        print("Deleted decal with id: {}".format(el["_id"]))

def clear_companies(root, username, password):
    companies = json.loads(requests.get(root + "/companies/").text)

    for el in companies:
        res = requests.delete(root + "/companies/" + el["_id"], auth=HTTPBasicAuth(username, password))
        if res.status_code == 401:
            print("Couldn't delete! authentication failed!")
            exit(2)
        print("Deleted companies with id: {}".format(el["_id"]))

if __name__ == "__main__":
    # Get the root that was passed in by the user
    try:
        root = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
    except IndexError: 
        print("root url, username and password must be entered to delete tripout db.")
        exit(1)

    # Download all collections on the api
    clear_pins(root, username, password)
    clear_decals(root, username, password)
    clear_companies(root, username, password)

    print("Done. Database is now empty.")
