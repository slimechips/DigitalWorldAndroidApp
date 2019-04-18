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

def get_stall_info(current_stall, callback = None):
    catalogDatabaseURL = databaseURL + "menu/" + current_stall + ".json"
    try:
        req = UrlRequest(catalogDatabaseURL,
                         on_success=partial(get_stall_success, callback),
                         verify=False,
                         on_error=network_failure)
    except:
        pass

def get_stall_success(callback, request, result, *args):
    # Split the stall data
    food_items = []
    print("Food info", result)
    for name, item in result.items():
        food_info = FoodItem(waiting_time=item["est_waiting_time"],
                              food_name=name,
                              photo_url=item["photo_url"],
                              price=item["price"])
        food_items.append(food_info)
    if callback:
        callback(food_items)

def create_order(uid, stall, food_item, spec_req, amt_paid, callback):
    order = Order(uid, stall, food_item, spec_req, amt_paid)
    orderDatabaseURL = databaseURL + "Order.json"
    req = UrlRequest(orderDatabaseURL,
                     on_success=partial(create_order_success, callback),
                     method="PATCH", verify=False,
                     on_error=network_failure)

def create_order_success(callback, req, result, *args):
    # Do something
    if callback:
        callback()

def network_failure(request, error, *args):
    Logger.info(error)


class FoodItem:
    def __init__(self, waiting_time=0, food_name="", photo_url="", price=""):
        self.__waiting_time = waiting_time
        self.__food_name = food_name
        self.__photo_url = photo_url
        self.__price = price

    @property
    def waiting_time(self):
        return self.__waiting_time

    @property
    def food_name(self):
        return self.__food_name

    @property
    def photo_url(self):
        return self.__photo_url

    @property
    def price(self):
        return self.__price