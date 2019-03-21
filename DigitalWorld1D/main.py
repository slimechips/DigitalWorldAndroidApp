__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.utils import platform
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from login import LoginPage, SignUpPage

appname = "SUTD EzEat"
buttonfontsize = 60

user = {}

class MainPage(Screen):
    _buttonfontsize = buttonfontsize
    pass


class ScreenManagement(ScreenManager):
    def go_back(self, name):
        if name == "signup":
            self.manager.current = "login"

kv_file = Builder.load_file("ezeat.kv")

class EzEat(App):
    def build(self):
        return kv_file
    
    def init(self, *args):
        if platform() == "android":
            import android
            android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, mods):
        if keycode1 in [27, 1001]:
            self.manager.current = self.manager.previous()
            return True
        else:
            return False

if __name__ == "__main__":
    EzEat().run()    


class User:
    def __init__(self, email, uid, *args):
        self._email = email
        self._uid = uid

class Order:
    def __init__(self):
    def get_current_stall(self):
        return self._current_stall
    def set_current_stall(self, value):
        self._current_stall = value
    _current_stall = property(get_current_stall, set_current_stall)

    @property
    def current_stall(self):
        return self.__current_stall
    @property.setter
    def current_stall(self, value)
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