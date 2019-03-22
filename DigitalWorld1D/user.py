class User:
    def __init__(self, email, username, uid = None, **kwargs):
        self.__email = email
        self.__username = username
        if uid != None:
            self.__uid = kwargs["uid"]
        elif kwargs["db_result"]:
            self.__uid = self.create_new_uid(kwargs["db_result"])
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

    def create_new_uid(self, db_result):
        max_uid = 0
        for uid in db_result["Users"].keys():
            if int(uid) > max_uid:
                max_uid = int(uid)
        return max_uid + 1

    def to_dict(self):
        mydict = {}
        subdict = {}
        property_names = ["email", "uid", "user_name"]
        try:
            properties = [self.email, self.uid, self.username]
        except:
            properties = ["placeholder", "placeholder", "placeholder"]
        for property_name, prop in property_names, properties:
            subdict[property_name] = prop
        mydict[str(self.uid)] = subdict
        return mydict