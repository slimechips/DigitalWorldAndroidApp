class Order:
    def __init__(self):
        pass
    def get_current_stall(self):
        return self._current_stall
    def set_current_stall(self, value):
        self._current_stall = value
    _current_stall = property(get_current_stall, set_current_stall)

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
    def food_items(self):
        return self.__food_items
    @food_items.setter
    def food_items(self, value):
        self.__food_items = value

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
    def total_amt_paid(self):
        return self.__total_amt_paid
    @total_amt_paid.setter
    def total_amt_paid(self, value):
        self.__total_amt_paid = value
