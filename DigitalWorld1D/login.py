__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from config import apikey, authDomain, databaseURL
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from user import User

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

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        Logger.info("test: xd")
        self.firebaseUrl = firebase_config["databaseURL"]
        self.user = None
        # self.verify_credentials()

    def verify_credentials(self):
        self.email, self.pw = self.ids["login"].text, self.ids["passw"].text
        headers = ["Users"]
        req = UrlRequest(databaseURL, self.got_json,
                        debug=True)

    def got_json(self, req, result, *args):
        Logger.info("json: got json")
        print(result)
        login_success = False
        try:
            for cur_uid, user in result["Users"].items():
                if user["email"] == self.email:
                    if user["password"] == self.pw:
                        uid = cur_uid
                        username = user["user_name"]
                        login_success = True
                    break
        except:
            Logger.info("Error: Login Error")
            self.login_error()

        if login_success:
            self.login(uid, self.email, username)
        else:
            self.login_error()


    def error_json(self, *args):
        Logger.info("json: error")

    def signup(self):
        self.manager.current = "signup"

    def login(self, email, uid, username):
        self.user = User(email, uid, username)
        self.manager.current = "main"

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
