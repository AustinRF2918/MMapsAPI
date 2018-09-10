import requests
from requests.auth import HTTPBasicAuth
import sys
import json

"""Given a list of JSON objects matching mmaps schema, actually converts it to our new schema."""

def translate_from_old(old):
    return {
            "phone_number": old["phoneNumber"],
            "description": old["description"],
            "address": old["address"],
            "image": old["logoId"],
            "name": old["name"],
            "website_link": old["url"],
            "video": old["videourl"],
            "latitude": old["lat"],
            "longitude": old["long"],
            "facebook_link": old["facebook"],
            "offer_title": old["offerTitle"],
            "offer_description": old["offerDescription"],
    }

def translate_to_old(new):
    return {
        "phoneNumber": new["phone_number"],
        "description": new["description"],
        "address": new["address"],
        "logoId": new["image"],
        "url": new["website_link"],
        "name": new["name"],
        "videourl": new["video"],
        "lat": new["latitude"],
        "long": new["longitude"],
        "facebook": new["facebook_link"],
        "offerTitle": new["offer_title"],
        "offerDescription": new["offer_description"],
    }

def translate_file_to_endpoint(file, root, username, password):
    with open(file) as f:
        data = json.load(f)
        for item in data:
            new_item = translate_from_old(item)
            requests.post(root + "/pins/", json=new_item, auth=HTTPBasicAuth(username, password))
            print("Translated item with name: {}".format(new_item["name"]))

if __name__ == "__main__":
    # Get the root that was passed in by the user
    try:
        root = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        filename = sys.argv[4]
    except IndexError: 
        print("root url, username, password, and filename must be entered to migrate tripout db.")
        exit(1)

    translate_file_to_endpoint(filename, root, username, password)
