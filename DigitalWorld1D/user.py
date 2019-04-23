from kivy.logger import Logger

class User:
    def __init__(self, email, username, password, uid = None, **kwargs):
        self.__email = email
        self.__username = username
        self.__password = password
        if uid != None:
            self.__uid = int(uid)
        elif kwargs["db_result"]:
            self.__uid = int(self.create_new_uid(kwargs["db_result"]))
        else:
            self.__uid = uid

    @property
    def email(self):
        return self.__email
    
    @property
    def uid(self):
        return self.__uid

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def orders(self):
        return self.__orders
    @orders.setter
    def orders(self, value):
        self.__orders = value

    def create_new_uid(self, db_result):
        max_uid = 0
        for user in db_result.values():
            uid = user["user_id"]
            if int(uid) > max_uid:
                max_uid = int(uid)
        return max_uid + 1

    def to_dict(self):
        mydict = {}
        property_names = ["email", "user_id", "user_name", "password"]
        try:
            properties = [self.__email, self.__uid, self.__username,
                          self.__password]
        except:
            properties = ["placeholder", "placeholder", "placeholder",
                          "placeholder"]
        for idx in range(len(property_names)):
            mydict[property_names[idx]] = properties[idx]
        bigdict = {self.__uid: mydict}
        return bigdict

current_user = None