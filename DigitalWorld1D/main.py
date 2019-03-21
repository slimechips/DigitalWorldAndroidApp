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
from user import User
from order import Order

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


