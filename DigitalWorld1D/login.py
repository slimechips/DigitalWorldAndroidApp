__version__ = "1.0"

# Kivy Module Imports
from kivy.app import App
#kivy.require("1.10.1")
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.properties import ColorProperty, BooleanProperty

from functools import partial

# Import app classes/strings/dimens from other python files
import user
import database
import orders
import appstrings
import appcolours
import appdimens
from config import apikey, authDomain, databaseURL

# LoginPage Screen
class LoginPage(Screen):

    # Initialize with no user logged in
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.user = None

    # Checks with database if login details are correct
    def verify_credentials(self):
        _username, _pw = self.ids["login"].text, self.ids["passw"].text
        usersDatabaseURL = databaseURL + "Users.json"
        # Make a URL request
        req = UrlRequest(usersDatabaseURL,
                         on_success=partial(self.got_json, _username, _pw),
                         verify=False,
                         on_error=self.error_json)

    # Callback on success of verifying credentials
    def got_json(self, username, pw, req, result, *args):
        Logger.info("json: got json")
        print(result)
        login_success = False
        try:
            for cur_uid, user in result.items():
                if user["user_name"] == username:
                    if user["password"] == pw:
                        uid = cur_uid
                        username = user["user_name"]
                        email = user["email"]
                        login_success = True
                    break
        except:
            # Encountered some network error
            Logger.info("Error: Login Error")
            self.login_error()

        if login_success:
            # User credentials are valid
            self.login(uid, username, pw, email)
        else:
            # User credentials are invalid
            self.login_error()

    # If verification failed for some reason
    def error_json(self, req, error, *args):
        Logger.info(error)
        self.login_error()

    # Switch to signup page
    def signup(self):
        self.manager.current = "signup"

    # Brings user to main menu after successful login
    def login(self, uid, username, pw, email):
        login_user = user.User(email, username, pw, uid = uid)
        user.current_user = login_user
        self.manager.current = "stalls"

    # UI change when user credentials are invalid
    def login_error(self):
        self.ids["login"].set_wrong()
        self.ids["passw"].set_wrong()
        
class SignUpPage(Screen):
    def __init__(self, **kwargs):
        super(SignUpPage, self).__init__(**kwargs)
        
    # Function to get information from text fields
    def get_ids(self):
        self.email_field = self.ids["email_signup_input"]
        self.username_field = self.ids["username_signup_input"]
        self.password_field = self.ids["passw_signup_input"]
        self.password2_field = self.ids["passw_confirm_signup_input"]
        self.info_text_field = self.ids["info_text"]
            
    # Initiate firebase signup process
    def firebase_signup(self):
        self.get_ids()
        self.__email = self.email_field.text
        self.__username = self.username_field.text
        self.__password = self.password_field.text
        self.__password2 = self.password2_field.text

        # Checks if user has filled in all textfields
        if self.__email == "" or self.__username == "" \
        or self.__password == "" or self.__password2 == "":
            self.info_text_field.text = "Please fill in all fields"
        self.check_email_validity(self.__email)
        self.check_password_validity(self.__password, self.__password2)

        # Checks if email, password and username meet requirements
        if self.check_email_validity(self.__email) \
            and self.check_password_validity(self.__password, self.__password2) \
            and self.check_username_validity(self.__username):
            usersDatabaseURL = databaseURL + "Users.json"
            # Send request to database to check validity of credentials
            self.req = UrlRequest(usersDatabaseURL, on_success=self.got_json,
                                  on_error=self.network_failure, verify=False)
        else:
            Logger.info("Some wrong information entered")

    # Algo to check if email meets requirements
    def check_email_validity(self, email):
        req_chars = ["@", "."]
        test_pass = True
        for char in req_chars:
            if char not in email:
                test_pass = False
        if not test_pass:
            self.reset_input_field_colours()
            self.email_field.set_wrong()
            self.info_text_field.text = "Invalid Email"
        return test_pass                

    # Algo to check if pw meets requirements
    def check_password_validity(self, pw1, pw2):
        import string
        req_chars = [string.ascii_letters, string.digits]
        test_pass = True
        # Checks if password and confirm password are the same
        if pw1 != pw2:
            self.passwords_different()
            test_pass = False
        else:
            for chars in req_chars:
                charset_found = False
                for char in chars:
                    if char in pw1:
                        charset_found = True
                        break
                if not charset_found:
                    test_pass = False
            if not test_pass:
                self.reset_input_field_colours()
                self.password_field.set_wrong()
                self.password2_field.set_wrong()
                self.info_text_field.text = "" \
                    "Password doesn't match requirements"
        return test_pass

    # Algo to check if username meets requirements
    def check_username_validity(self, username):
        test_pass = True
        if len(username) < 5:
            test_pass = False
        if not test_pass:
            self.reset_input_field_colours()
            self.username_field.set_wrong()
            self.info_text_field.text = "Invalid Username format"
        return test_pass

    # Callback when checking if user credentials already exists
    def got_json(self, request, result, *args):
        Logger.info("json: got json")
        Logger.info(result)
        signup_success = True

        # Iterates through user database to check email and username
        # have not already been taken
        for cur_uid, user in result.items():
            if user["email"] == self.__email:
                self.email_taken()
                signup_success = False
                break
            if user["user_name"] == self.__username:
                self.username_taken()
                signup_success = False
                break
        
        # If email username have not already been taken, and at this point
        # validity has already been verified, so we can actually start the
        # signup process
        if signup_success:
            Logger.debug("Signup Success!")

            # Creates a new user object, refer to User.py for actual properties
            # of the object
            user.current_user = user.User(self.__email, self.__username,
                                          self.__password, db_result = result)
            Logger.debug("user created")

            # Now we can upload the user object to firebase
            self.upload_to_firebase(user.current_user)
            Logger.debug("user uploaded")

    # If unable to connect to the database
    def network_failure(self, request, error, *args):
        self.reset_input_field_colours()
        self.password_field.set_wrong()
        self.password2_field.set_wrong()
        self.info_text_field.text = "Network failure"
        Logger.info(error)

    # Call this to clear any previous UI warnings to user
    def reset_input_field_colours(self):
        self.email_field.set_okay()
        self.username_field.set_okay()
        self.password_field.set_okay()
        self.password2_field.set_okay()
        self.info_text_field.text = ""

    # Handles UI change when passwords don't message
    def passwords_different(self):
        self.reset_input_field_colours()
        self.password_field.set_wrong()
        self.password2_field.set_wrong()
        self.info_text_field.text = "Passwords don't match"

    # Handles UI Change when email already exists in database
    def email_taken(self):
        self.reset_input_field_colours()
        self.email_field.set_wrong()
        self.info_text_field.text = "Email is already Taken!"

    # Handles UI chaange when username already exists in database
    def username_taken(self):
        self.reset_input_field_colours()
        self.username_field.set_wrong()
        self.info_text_field.text = "Username is already Taken!"

    # Uploads new user data to database. This is only called when
    # all requirements for user credentials are satisfied and verified
    # with the database
    def upload_to_firebase(self, user):
        import json
        data = json.dumps(user.to_dict())
        headers = {'Content-Type': 'application/json'}
        usersDatabaseURL = databaseURL + "Users.json"
        req = UrlRequest(usersDatabaseURL, req_body=data, req_headers=headers,
                         method="PATCH", verify=False,
                         on_success=partial(self.upload_success, user))

    # Switch user to main page after signup is successful
    def upload_success(self, user, *args):
        Logger.info("Upload Successful")
        user.current_user = user
        self.manager.current = "stalls"

# Custom button class SmoothButton
class SmoothButton(Button):
    btn_color = ColorProperty()

# Default transparent TextInput class
class TransparentInput(TextInput):
    cur_line_colour = ColorProperty()
    normal_line_colour = ColorProperty()
    focus_line_colour = ColorProperty()
    wrong_line_colour = ColorProperty()
    wrong = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wrong = False

    # Callback when focus events happen
    def on_focus(self, *args):
        if self.focus:
            # TextInput is focused
            self.cur_line_colour = self.focus_line_colour # Change Colour
        elif self.wrong:
            # User previously entered wrong info
            self.cur_line_colour = self.wrong_line_colour # Change Colour
        else:
            # Text input is not focused
            self.cur_line_colour = self.normal_line_colour # Change Colour

    # Change colour of TransparentInput if it does not meet requirements
    def set_wrong(self):
        self.wrong = True
        self.foreground_color = self.wrong_line_colour
        self.cur_line_colour = self.wrong_line_colour

    # Change colour of TransparentInput back to normal state
    def set_okay(self):
        self.wrong = False
        self.foreground_color = appcolours.WHITE
        self.cur_line_colour = self.normal_line_colour