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
    @property.setter
    def time_of_order(self, value):
        self.__time_of_order = value

    @property
    def food_items(self):
        return self.__food_items
    @property.setter
    def food_items(self, value):
        self.__food_items = value

    @property
    def special_requests(self):
        return self.__special_requests
    @property.setter
    def special_requests(self, value):
        self.__special_requests = value

    @property
    def time_of_order_completion(self):
        return self.__time_of_order_completion
    @property.setter
    def time_of_order_completion(self, value):
        self.__time_of_order_completion = value
    
    @property
    def time_of_order_collection(self):
        return self.__time_of_order_collection
    @property.setter
    def time_of_order_collection(self, value):
        self.__time_of_order_collection = value

    @property
    def total_amt_paid(self):
        return self.__total_amt_paid
    @property.setter
    def total_amt_paid(self, value):
        self.__total_amt_paid = value
    _time_of_order
    _number_in_queue
    _food_items
    _special_requests
    _time_of_order_completion
    _time_of_order_collection
    _total_amt_paid