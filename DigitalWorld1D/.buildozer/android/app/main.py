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

appname = "SUTD EzEat"
label_font_size = 70
buttonfontsize = 60

class LoginPage(Screen):

    _titlefontsize = 120
    _appname = appname
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def verify_credentials(self):
        
        wrong_credential_colour = (1, 0.4, 0.4, 1)

        if self.ids["login"].text == "username" \
            and self.ids["passw"].text == "password":
            self.manager.current = "main"
        else:
            self.ids["login"].background_color = wrong_credential_colour
            self.ids["passw"].background_color = wrong_credential_colour

    def signup(self):
        self.manager.current = "signup"

class SignUpPage(Screen):
    _titlefontsize = 80
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def firebase_signup(self):
        pass


class MainPage(Screen):
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
