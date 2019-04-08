import requests
from kivy.logger import Logger
from config import databaseURL
from order import Order

def check_request_success(req):
    success = None
    try:
        req.raise_for_status()
        success = True
    except:
        Logger.info("Downloading file failed")
        success = False
    return success

def get_stalls():
    catalogDatabaseURL = databaseURL + "Catalog.json"
    req = requests.get(catalogDatabaseURL)

    if check_request_success(req):
        result = req.json()
        for stall in result["stall"]:
            yield stall

def get_stall_info(stall):
    pass

def create_order(uid, stall, food_item, spec_req, amt_paid):
    order = Order(uid, stall, food_item, spec_req, amt_paid)