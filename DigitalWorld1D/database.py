from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from config import databaseURL
from functools import partial
from order import Order
from importbarcode import barcode_generator
from datetime import datetime
import json
 
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
        if name != "!stall_id":
            food_info = FoodItem(waiting_time=item["est_waiting_time"],
                                food_name=name,
                                photo_url=item["photo_url"],
                                price=item["price"],
                                food_id=item["food_id"],
                                stall_id=item["stall_id"])
            food_items.append(food_info)
    if callback:
        callback(food_items)

def get_num_in_q(stall):
    pass

def split_datetime_now():
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    
    # Get date in ddmmyyyy format, adding leading zeroes when necessary
    date = str(day).zfill(2) + str(month).zfill(2) + str(year).zfill(4)

    # Get time in hhmmss format, adding leading zeroes when necessary
    time = str(hour).zfill(2) + str(minute).zfill(2) + str(second).zfill(2)

    Logger.info("Date: " + date)
    Logger.info("Time: " + time)
    return date, time


# Create a new order
def create_order(uid, stall, stall_id, food_item, food_id, spec_req, amt_paid,
                 num_in_q, callback):
    order = Order(uid, stall, stall_id, food_item, food_id, spec_req, amt_paid,
                  num_in_q)
    date, time = split_datetime_now()
    barcode_no = barcode_generator(stall_id, food_id, uid, date, time)
    orderDatabaseURL = databaseURL + "active_orders/" + stall + ".json"
    Logger.info("Dbase URL:" + orderDatabaseURL)
    data = json.dumps(order.to_dict(barcode_no))
    Logger.info("Created order")
    headers = {'Content-Type': 'application/json'}

    req = UrlRequest(orderDatabaseURL, req_body=data, req_headers=headers,
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
    def __init__(self, waiting_time=0, food_name="", photo_url="", price="",
                 food_id=0, stall_id=0):
        self.__waiting_time = waiting_time
        self.__food_name = food_name
        self.__photo_url = photo_url
        self.__price = price
        self.__food_id = food_id
        self.__stall_id = stall_id

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

    @property
    def food_id(self):
        return self.__food_id

    @property
    def stall_id(self):
        return self.__stall_id