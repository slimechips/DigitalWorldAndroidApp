__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from config import apikey, authDomain, databaseURL
from libdw import pyrebase
from main import User

firebase_config = {
    "apikey": apikey,
    "authDomain": authDomain,
    "databaseURL": databaseURL
}

label_font_size = 70
appname = "SUTD EzEat"
buttonfontsize = 60

class LoginPage(Screen):

    _titlefontsize = 120
    _appname = appname
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def __init__(self):
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.db = self.firebase.database()
        self.root = self.db.child("/").get()
        self.user = None

    def verify_credentials(self):
        email, pw = self.ids["login"].text, self.ids["passw"].text
        login_success = False

        for cur_uid, user in self.db.child("users").get().items():
            if user["email"].get() == email:
                if user["password"].get() == pw:
                    uid = cur_uid
                    login_success = True
                break

        if login_success:
            self.login(uid, email)
        else:
            self.login_error()

    def signup(self):
        self.manager.current = "signup"

    def login(self, email, uid):
        self.user = User(email, uid)

    def login_error(self):
        wrong_credential_colour = (1, 0.4, 0.4, 1)
        self.ids["login"].background_color = wrong_credential_colour
        self.ids["passw"].background_color = wrong_credential_colour
        

class SignUpPage(Screen):
    _titlefontsize = 80
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def firebase_signup(self):
        pass
