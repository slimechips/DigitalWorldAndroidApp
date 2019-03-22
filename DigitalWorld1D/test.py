from kivy.network.urlrequest import UrlRequest
from config import apikey, authDomain, databaseURL

firebase_config = {
    "apikey": apikey,
    "authDomain": authDomain,
    "databaseURL": databaseURL
}

def verify_credentials():

    req = UrlRequest(databaseURL, got_json, on_progress=got_error)

def got_json(req, result):
    print("got json")
    for cur_uid, user in result.items():
        print(cur_uid, user)

def got_error(req, current_size, total_size):
    print("error")
            

verify_credentials()

