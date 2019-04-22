from datetime import datetime
from kivy.logger import Logger

class Order:
    def __init__(self, uid, stall, stall_id, food_item, food_id,
                 spec_req, amt_paid, num_in_q):
        self.__uid = uid
        self.__current_stall = stall
        self.__stall_id = stall_id
        self.__food_item = food_item
        self.__food_id = food_id
        self.__special_requests = spec_req
        self.time_of_order = str(datetime.now()).split('.')[0]
        self.__amt_paid = amt_paid
        self.__num_in_q = num_in_q
        self.__status = "sent"

    def to_dict(self, barcode_no):
        mydict = {}
        property_names = ["estimated_waiting_time", "food_item", "order_id",
                          "orders_in_queue", "special_requests", "stall", 
                          "status", "time_of_order", "time_of_order_collection",
                          "time_of_order_completion", "user_id"]
        properties = [self.uid, self.food_item, barcode_no,
                      2, self.special_requests, self.current_stall,
                      self.status, self.time_of_order, "None",
                      "None", 1]

        for idx in range(len(property_names)):
            mydict[property_names[idx]] = properties[idx]
            bigdict = {barcode_no: mydict}
        Logger.info("Big Dict:" + str(bigdict))
        return bigdict

    @property
    def uid(self):
        return self.__uid
    @uid.setter
    def uid(self, value):
        self.__uid = value

    @property
    def current_stall(self):
        return self.__current_stall
    @current_stall.setter
    def current_stall(self, value):
        self.__current_stall = value

    @property
    def stall_id(self):
        return self.__stall_id
    @stall_id.setter
    def stall_id(self, value):
        self.__stall_id = value
    
    @property
    def time_of_order(self):
        return self.__time_of_order
    @time_of_order.setter
    def time_of_order(self, value):
        self.__time_of_order = value

    @property
    def food_item(self):
        return self.__food_item
    @food_item.setter
    def food_item(self, value):
        self.__food_item = value

    @property
    def food_id(self):
        return self.__food_id
    @food_id.setter
    def food_id(self, value):
        self.__food_id = value

    @property
    def special_requests(self):
        return self.__special_requests
    @special_requests.setter
    def special_requests(self, value):
        self.__special_requests = value

    @property
    def time_of_order_completion(self):
        return self.__time_of_order_completion
    @time_of_order_completion.setter
    def time_of_order_completion(self, value):
        self.__time_of_order_completion = value
    
    @property
    def time_of_order_collection(self):
        return self.__time_of_order_collection
    @time_of_order_collection.setter
    def time_of_order_collection(self, value):
        self.__time_of_order_collection = value

    @property
    def amt_paid(self):
        return self.__amt_paid
    @amt_paid.setter
    def amt_paid(self, value):
        self.__amt_paid = value

    @property
    def num_in_q(self):
        return self.__num_in_q
    @num_in_q.setter
    def num_in_q(self, value):
        self.__num_in_q = value

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, value):
        self.__status = value
