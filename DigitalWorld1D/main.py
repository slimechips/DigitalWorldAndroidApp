__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.utils import platform
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from login import LoginPage, SignUpPage
from user import User
from order import Order

appname = "SUTD EzEat"
buttonfontsize = 60
titlefontsize = 120

user = {}

class MainPage(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class Logout_Confirm(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class Stalls(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class Dishes(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class Orders(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class Favourites(Screen):
    _buttonfontsize = buttonfontsize
    _titlefontsize = titlefontsize
    pass

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_handler)

    def key_handler(self, instance, key, *args):
        if key is 27:
            self.set_previous_screen()
            return True
    
    def set_previous_screen(self):
        if self.current != "main":
            self.transition.direction = "left"
            self.current = self.previous()

class EzEat(App):
    def build(self):
        self.bind(on_start=self.init)

    def init(self, *args):
        pass

if __name__ == "__main__":
    EzEat().run()    


