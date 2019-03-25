__version__ = "1.0"
from kivy.app import App
#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from config import apikey, authDomain, databaseURL
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from functools import partial
from user import User

firebase_config = {
    "apikey": apikey,
    "authDomain": authDomain,
    "databaseURL": databaseURL
}

label_font_size = 70
appname = "SUTD EzEat"
buttonfontsize = 60
wrong_credential_colour = (1, 0.4, 0.4, 1)
WHITE = (1, 1, 1, 1)


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
        _username, _pw = self.ids["login"].text, self.ids["passw"].text
        headers = ["Users"]
        self.req = UrlRequest(databaseURL + ".json", partial(self.got_json,
                              _username, _pw), debug=True)

    def got_json(self, username, pw, *args):
        Logger.info("json: got json")
        result = self.req.result
        print(result)
        login_success = False
        try:
            for cur_uid, user in result["Users"].items():
                if user["user_name"] == username:
                    if user["password"] == pw:
                        uid = cur_uid
                        username = user["user_name"]
                        email = user["email"]
                        login_success = True
                    break
        except:
            Logger.info("Error: Login Error")
            self.login_error()

        if login_success:
            self.login(uid, username, pw, email)
        else:
            self.login_error()


    def error_json(self, *args):
        Logger.info("json: error")

    def signup(self):
        self.manager.current = "signup"

    def login(self, uid, username, pw, email):
        login_user = User(email, username, pw, uid = uid)
        User.current_user = login_user
        self.manager.current = "main"

    def login_error(self):
        self.ids["login"].background_color = wrong_credential_colour
        self.ids["passw"].background_color = wrong_credential_colour
        
class SignUpPage(Screen):
    _titlefontsize = 80
    _labelfontsize = label_font_size
    _buttonfontsize = buttonfontsize

    def __init__(self, **kwargs):
        super(SignUpPage, self).__init__(**kwargs)
        

    def get_ids(self):
        self.email_field = self.ids["email_signup_input"]
        self.username_field = self.ids["username_signup_input"]
        self.password_field = self.ids["passw_signup_input"]
        self.password2_field = self.ids["passw_confirm_signup_input"]
        self.info_text_field = self.ids["info_text"]
            
    def firebase_signup(self):
        self.get_ids()
        self.__email = self.email_field.text
        self.__username = self.username_field.text
        self.__password = self.password_field.text
        self.__password2 = self.password2_field.text

        if self.__email == "" or self.__username == "" \
        or self.__password == "" or self.__password2 == "":
            self.info_text_field.text = "Please fill in all fields"
        elif self.__password == self.__password2:
            req = UrlRequest(databaseURL + ".json", self.got_json)
        else:
            self.passwords_different()


    def got_json(self, req, result, *args):
        Logger.info("json: got json")
        print(result)
        signup_success = True
        for cur_uid, user in result["Users"].items():
            if user["email"] == self.__email:
                self.email_taken()
                signup_success = False
                break
            if user["user_name"] == self.__username:
                self.username_taken()
                signup_success = False
                break
        if signup_success:
            Logger.debug("Signup Success!")
            user = User(self.__email, self.__username,
                        self.__password, db_result = result)
            Logger.debug("user created")
            self.upload_to_firebase(user)
            Logger.debug("user uploaded")

    def reset_input_field_colours(self):
        self.email_field.background_color = WHITE
        self.username_field.background_color = WHITE
        self.password_field.background_color = WHITE
        self.password2_field.background_color = WHITE
        self.info_text_field.text = ""

    def passwords_different(self):
        self.password_field.background_color = wrong_credential_colour
        self.password2_field.background_color = wrong_credential_colour
        self.info_text_field.text = "Passwords don't match"

    def email_taken(self):
        self.reset_input_field_colours
        self.email_field.background_color = wrong_credential_colour
        self.info_text_field.text = "Email is already Taken!"

    def username_taken(self):
        self.reset_input_field_colours
        self.username_field.background_color = wrong_credential_colour
        self.info_text_field.text = "Username is already Taken!"

    def upload_to_firebase(self, user):
        Logger.debug("ul to firebase")
        import json
        data = json.dumps(user.to_dict())
        headers = {'Content-Type': 'application/json'}
        usersDatabaseURL = databaseURL + "Users.json"
        req = UrlRequest(usersDatabaseURL, req_body=data, req_headers = headers,
                         on_success=partial(self.upload_success, user),
                         debug=True)

    def upload_success(self, user, *args):
        Logger.info("Upload Successful")
        User.current_user = user
        self.manager.current = "main"
