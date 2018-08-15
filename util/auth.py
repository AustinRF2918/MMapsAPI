from flask_httpauth import HTTPBasicAuth
import json

auth = HTTPBasicAuth()

USER_DATA = None
with open("credentials.json") as f:
    USER_DATA = json.load(f)

@auth.verify_password
def verify_password(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

