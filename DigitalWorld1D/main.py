__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
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
        pass

class MainPage(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

kv_file = Builder.load_file("ezeat.kv")

class EzEat(App):
    def build(self):
        return kv_file

if __name__ == "__main__":
    EzEat().run()
