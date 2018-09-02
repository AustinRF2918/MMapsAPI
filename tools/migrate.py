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
            "video": old["videourl"],
            "latitude": old["lat"],
            "longitude": old["long"],
            "facebook_link": old["facebook"],
            "offer_title": old["offerTitle"],
            "offer_description": old["offerDescription"],
    }

# TODO - convert
def translate_to_old(new):
    return {
        "phoneNumber": new["phone_number"],
        "description": new["description"],
        "address": new["address"],
        "logoId": new["image"],
        "name": new["name"],
        "videourl": new["video"],
        "lat": new["latitude"],
        "long": new["longitude"],
        "facebook": new["facebook_link"],
        "offerTitle": new["offer_title"],
        "offerDescription": new["offer_description"],
    }

def translate_file_to_endpoint(file, url):
    with open(file) as f:
        data = json.load(f)
        for item in data:
            new_item = translate_from_old(item)
            requests.post(url, json=new_item, auth=HTTPBasicAuth("anne", "matrix"))

if __name__ == "__main__":
    translate_file_to_endpoint(sys.argv[1], sys.argv[2])
