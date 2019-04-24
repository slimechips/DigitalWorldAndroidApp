from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from config import databaseURL
from functools import partial
from order import Order
from importbarcode import barcode_generator
from datetime import datetime
import user
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
    # Get the info of the menu of a particular stall from firebase
    catalogDatabaseURL = databaseURL + "menu/" + current_stall + ".json"
    try:
        req = UrlRequest(catalogDatabaseURL,
                         on_success=partial(get_stall_success, callback),
                         verify=False,
                         on_error=network_failure)
    except:
        pass

def get_stall_success(callback, request, result, *args):
    # Callback to query for information of stall menu
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

def get_num_in_q(stall, callback):
    # Func to get number of orders in the queue of a particular stall
    stallDatabaseUrl = databaseURL + "active_orders/" + stall + ".json"
    req = UrlRequest(stallDatabaseUrl, 
                     on_success=partial(got_num_in_q, callback),
                     verify=False,
                     on_error=network_failure)

def got_num_in_q(callback, req, result, *args):
    # Callback from querying for get number in queue    
    Logger.info("Result:" + str(result))
    Logger.info(len(result))
    num_in_q = len(result) - 1
    if callback:
        callback(num_in_q)

def split_datetime_now():
    # Get datetime format for barcode
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


def create_order(uid, stall, stall_id, food_item, food_id, spec_req, amt_paid,
                 num_in_q, est_wait, callback):
    # Create a new order and uploads it to firebase    
    order = Order(uid, stall, stall_id, food_item, food_id, spec_req, amt_paid,
                  num_in_q, est_wait)
    date, time = split_datetime_now()
    barcode_no = barcode_generator(order.stall_id, order.food_id, 
                                   order.uid, date, time)
    order.order_id = barcode_no
    orderDatabaseURL = databaseURL + "active_orders/" + stall + ".json"
    Logger.info("Dbase URL:" + orderDatabaseURL)
    data = json.dumps(order.to_dict())
    Logger.info("Created order")
    headers = {'Content-Type': 'application/json'}

    # PATCH the new order information to firebase
    req = UrlRequest(orderDatabaseURL, req_body=data, req_headers=headers,
                     on_success=None,
                     method="PATCH", verify=False,
                     on_error=network_failure)

    userDatabaseURL = databaseURL + "Users/" + str(uid) + "/active_orders.json"  
    
    data_for_user = json.dumps({order.order_id: {"stall" : order.current_stall}})

    re2 = UrlRequest(userDatabaseURL, req_body=data_for_user, 
                     req_headers=headers,
                     on_success=partial(create_order_success, callback),
                     method="PATCH", verify=False,
                     on_error=network_failure)

def create_order_success(callback, req, result, *args):
    # Callback when order has been successfully created
    Logger.info("Order: Successfully created")
    if callback:
        callback()

def check_my_orders(uid, callback):
    # Function to find out a user's orders from firebase
    userDatabaseUrl = databaseURL + "Users/" + str(uid) + "/active_orders.json"

    # Queries to firebase, result passed to get_orders_data
    req = UrlRequest(userDatabaseUrl,
                     on_success=partial(got_orders_data, callback),
                     verify=False, on_error=network_failure)

def got_orders_data(callback, req, result, *args):
    # Callback to query for orders data
    Logger.info("Database: Got orders data")
    user.current_user.orders = []
    # Result will only contain the stall name of the order
    # Need to retrieve other order data from active_orders node
    if result == None or result == "":
        # User has no active orders!
        callback([]) # Inform UI there are no orders to show
    else:
        # User has at least 1 active order!
        # Add to list of orders to get
        user.current_user.orders = list(result.keys())
        # Convert the str list to a int list
        user.current_user.orders = list(map(int, user.current_user.orders))
        for order_no, order_data in result.items():
            order_no = int(order_no) # Cast self to an int
            Logger.info("Order_no: " + str(order_no))
            # Iterate through orders
            query_detailed_order(order_data["stall"], order_no, callback)

def query_detailed_order(stall, order_no, callback):
    # Query for detailed orders data
    orderUrl = "{}active_orders/{}/{}.json".format(databaseURL, stall,
                                                   order_no)
    req = UrlRequest(orderUrl, 
                     on_success=partial(got_detailed_order, order_no, callback),
                     verify=False, on_error=network_failure)

def got_detailed_order(order_no, callback, req, result, *args):
    # Callback when detailed order data comes
    if result == "" or result == None:
        # Stall has already completed/removed the order
        # Remove this order from our user's local order list
        idx = user.current_user.orders.index(order_no)
        user.current_user.orders.pop(idx)

        # Remove this order from user's firebase list
        remove_order(user.current_user.uid, order_no)

    else:
        # Order exists
        Logger.info("Order_data: " + str(result))
        order = Order.dict_to_obj(result) # Converts dict to order obj
        # Replace the 'vague' order with a proper order object
        for idx, orig_order in enumerate(user.current_user.orders):
            if type(orig_order) != Order:
                if order.order_id == int(orig_order):
                    user.current_user.orders[idx] = order
    
    # Check if all detailed order data is in
    all_orders_in = True
    for cur_order in user.current_user.orders:
        if type(cur_order) == int or type(cur_order) == str:
            # Order has not been received yet
            all_orders_in = False

    if all_orders_in:
        # Call our callback
        Logger.info("Orders in: " + str(user.current_user.orders))
        callback(user.current_user.orders)

def remove_order(uid, order_no):
    # Remove a order from user database
    Logger.info("Removing Order: " + str(order_no))
    orderUrl = "{}Users/{}/active_orders/{}.json".format(databaseURL,
                                                         uid, order_no)
    Logger.info("Remove from: " + orderUrl)
    # URL req to delete data
    req = UrlRequest(orderUrl, method="DELETE", on_success=order_removed,
                     verify=False, on_error=network_failure)

def order_removed(*args):
    Logger.info("Order: Order missing, removed...")

def query_picture_url(stall_name, food_name, idx, callback):
    # Get the food picture of an order given its stall id and food id
    imageUrl = "{}menu/{}/{}/photo_url.json" \
          .format(databaseURL,stall_name, food_name)
    
    # Query the url
    req = UrlRequest(imageUrl, 
                     on_success=partial(got_picture_url, idx, callback),
                     verify=False, on_error=network_failure)

def got_picture_url(idx, callback, req, result, *args):
    # Callback to query for picture url
    Logger.info("Database: Got picture url")
    callback(result, idx)

def network_failure(request, error, *args):
    # Callback when there is a network error
    Logger.info(error)

# Food Item Object
class FoodItem:
    # Constructor
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