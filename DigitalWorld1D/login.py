__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen

label_font_size = 70
appname = "SUTD EzEat"
buttonfontsize = 60

class LoginPage(Screen):

    _titlefontsize = 120
    _appname = appname
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def verify_credentials(self):
        
        wrong_credential_colour = (1, 0.4, 0.4, 1)

        # Authentication from Firebase; username and password to be encrypted
        if self.ids["login"].text == "username" \
            and self.ids["passw"].text == "password":
            self.manager.current = "main"
        else:
            self.ids["login"].background_color = wrong_credential_colour
            self.ids["passw"].background_color = wrong_credential_colour

    # On release of Sign Up button, login info to be encrypted and uploaded onto Firebase
    def signup(self):
        self.manager.current = "signup"

class SignUpPage(Screen):
    _titlefontsize = 80
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def firebase_signup(self):
        pass