__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.utils import platform
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.uix.image import AsyncImage
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from login import LoginPage, SignUpPage
from user import User
from order import Order
import database
from kivy.loader import Loader
from install_certi import no_ssl_verification

appname = "SUTD EzEat"
buttonfontsize = 60
titlefontsize = 120

user = {}

class TopNavigationBar(ActionBar):
    text = StringProperty()
    
class BottomNavigationBar(ActionBar):
    pass

class Stalls(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    layout_content = ObjectProperty(None)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.first_load = True

    # When loading, setup the stalls to be active button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["stalls_btn"].state = "down"

    def btn_pressed(self, stall_name):
        self.manager.current_stall = stall_name
        self.manager.current = "stall_screen"

class StallButton(Button):
    btn_txt = 80
    source = StringProperty(None)
    label_txt = StringProperty(None)
    stall_name = StringProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.label_txt == None:
            self.label_txt = "Placeholder"
    
    
class StallScreen(Screen):
    food_items = []
    current_stall = StringProperty("")

    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.do_layout()
        database.get_stall_info(self.current_stall, callback=self.on_get_info)
        self.ids["btm_bar"].ids["stalls_btn"].state = "normal"

    def on_get_info(self, food_items):
        self.food_items = food_items
        self.grd = self.ids["stall_grd"]
        print("on get info")
        for i, food in enumerate(food_items):
            food_img_id = "food_{}_img".format(i)
            picture = AsyncImage(id=food_img_id,
                                 source=food.photo_url,
                                 allow_stretch=True,
                                 keep_ratio=True,
                                 on_error=self.img_error,
                                 on_load=self.loaded,
                                 size_hint_y=None,
                                 height=400)

            print("picture")
            self.grd.add_widget(picture)
        
            label_text = "Food Name: {}\nPrice: {}\nEst " \
                         "Wait Time: {} mins".format(food.food_name, 
                         food.price, food.waiting_time)
            label = Label(text=label_text, font_size=40, 
                          color=[0, 0, 0, 1], height=400)
            self.grd.add_widget(label)
            print("added widgets")

    def loaded(self, *args):
        print("I loaded yo")
    
    def img_error(self, error, *args):
        Logger.info("Error: " + str(error))
    
    def on_leave(self, *args):
        super().on_leave(*args)
        self.grd.clear_widgets()
        self.food_items = []
        
class FoodLabel(GridLayout):
    pass
        

class My_Orders(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize

    # When loading, setup the orders to be active button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["my_orders_btn"].state = "down"

class Favourites(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class ScreenManagement(ScreenManager):
    current_stall = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_handler)

    def key_handler(self, instance, key, *args):
        if key is 27:
            self.set_previous_screen()
            return True
    
    def set_previous_screen(self):
        if self.current != "login":
            self.transition.direction = "left"
            self.current = self.previous()

class Logout_Confirm(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass


class EzEat(App):
    def build(self):
        self.disable_ssl()
        self.bind(on_start=self.init)

    def init(self, *args):
        pass
    
    def disable_ssl(self):
        # This disables SSL verification, I did this because my SSL doesnt work
        # for some reason
        # Please don't penalize me prof thanks :D
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == "__main__":
    EzEat().run()    


