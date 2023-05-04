class User:

    __user_id: int
    __user_name: str
    __file_name_voice: str

    def __init__(self):
        self.__user_id = -1
        self.__user_name = None
        self.__file_name_voice = None

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        self.__user_id=value

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value: str):
        self.__user_name = value

    @property
    def file_name_voice(self):
        return self.__file_name_voice

    @file_name_voice.setter
    def user_name(self, value: str):
        self.__file_name_voice = value