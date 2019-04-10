from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from config import databaseURL
from functools import partial
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

def get_stalls(callback = None):
    catalogDatabaseURL = databaseURL + "Catalog.json"
    try:
        req = UrlRequest(catalogDatabaseURL,
                         on_success=partial(get_stalls_success, callback),
                         verify=False,
                         on_error=network_failure)
    except:
        pass
    # if check_request_success(req):
    #     result = req.json()
    #     for stall in result["stall"]:
    #         yield stall

def get_stalls_success(request, result, callback, *args):
    # Split the stall data
    stall_info = None
    if callback:
        callback(stall_info)

def get_stall_info(stall):
    pass

def create_order(uid, stall, food_item, spec_req, amt_paid):
    order = Order(uid, stall, food_item, spec_req, amt_paid)

def network_failure(request, error, *args):
    Logger.info(error)