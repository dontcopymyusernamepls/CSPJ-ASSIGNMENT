import User


class SingpassUser(User.User):
    count_id = 0

    def __init__(self, first_name, last_name, username, email, Password):
        super().__init__(first_name, last_name, username, email, Password)
        User.count_id += 1
        self.__User_id = User.count_id


    def get_user_id(self):
        return self.__User_id


    def set_user_id(self, User_id):
       self.__User_id = User_id

