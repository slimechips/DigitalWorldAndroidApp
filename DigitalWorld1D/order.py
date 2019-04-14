from datetime import datetime

class Order:
    def __init__(self, uid, stall, food_item, spec_req, amt_paid):
        self.__current_stall = stall
        self.__uid = uid
        self.__current_stall = stall
        self.__food_item = food_item
        self.__special_requests = spec_req
        self.time_of_order = datetime.now()
        self.__amt_paid = amt_paid

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
