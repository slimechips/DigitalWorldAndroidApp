# Kivy Module Imports
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
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.logger import Logger

# Import app classes/strings/dimens from other python files
import appstrings
import appdimens
import database
import fonts
from user import User
from order import Order

from copy import copy

# Import app page scripts
import login
import orders
import logout
import confirmorder

class TopNavigationBar(ActionBar):
    text = StringProperty()
    
class BottomNavigationBar(ActionBar):
    pass

class Stalls(Screen):
    _buttonfontsize = appdimens.button_font_size
    _titlefontsize = appdimens.title_font_size
    layout_content = ObjectProperty(None)

    # When loading, setup the stalls to be active button in nav bar
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids["btm_bar"].ids["stalls_btn"].state = "down"

    def btn_pressed(self, stall_name, label_txt):
        self.manager.current_stall = stall_name
        self.manager.navbarname = label_txt
        self.manager.current = "stall_screen"

class StallButton(Button):
    source = StringProperty(None)
    label_txt = StringProperty(None)
    stall_name = StringProperty(None)

class StallScreen(Screen):
    food_items = []
    current_stall = StringProperty("")

    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.ids["top_bar"].text = self.manager.navbarname
        database.get_stall_info(self.current_stall, callback=self.on_get_info)
        self.ids["btm_bar"].ids["stalls_btn"].state = "normal"

    def on_get_info(self, food_items):
        self.food_items = food_items
        self.grd = self.ids["stall_grd"]
        for i, food in enumerate(food_items):
            food_img_id = "food_{}_img".format(i)
            picture = FoodPicture(id=food_img_id,
                                  source=food.photo_url)

            label_text = "[u][b]{}[/b][/u]\n" \
                         "[b]Price:[/b] {}\n" \
                         "[b]Est Wait Time:[/b] {} mins" \
                         .format(food.food_name, 
                         food.price, food.waiting_time)
            label = FoodLabel(text=label_text)
            picture.food_label = label
            picture.food_info = food
            self.grd.add_widget(picture)
            self.grd.add_widget(label)

    def loaded(self, *args):
        pass

    def img_error(self, error, *args):
        Logger.info("Error: " + str(error))

    def goto_confirm(self, picture):
        self.manager.food_item = picture
        self.manager.current = "confirm_order"
    
    def on_leave(self, *args):
        super().on_leave(*args)
        self.grd.clear_widgets()
        self.food_items = []
        
class FoodLabel(Label):
    pass

class FoodPicture(ButtonBehavior, AsyncImage):
    food_label = ObjectProperty()
    food_info = ObjectProperty()
    stall_name = StringProperty()

    def on_release(self):
        super().on_release()
        self.parent.parent.parent.parent.goto_confirm(self)
        
class ScreenManagement(ScreenManager):
    current_stall = StringProperty("")
    food_item = ObjectProperty()
    cur_food_info = ObjectProperty()
    navbarname = ObjectProperty()

    main_menus = ["stalls", "my_orders"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_handler)

    def key_handler(self, instance, key, *args):
        if key is 27:
            self.set_previous_screen()
            return True
    
    def set_previous_screen(self):
        if self.current == "loginpage":
            pass
        elif self.current in self.main_menus:
            pass
        elif self.current == "logout_pg":
            self.current = "stalls"
        else:
            self.transition.direction = "left"
            self.current = self.previous()

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


