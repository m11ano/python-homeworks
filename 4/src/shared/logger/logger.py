from shared.metaclasses.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, mock: bool = False):
        self.__mock = mock

    def log(self, str: str, *args) -> None:
        if not self.__mock:
            print(f"\033[92mLog:\033[00m {str}", *args)

    def error(self, str: str, *args) -> None:
        if not self.__mock:
            print(f"\033[91mError log: {str}\033[00m", *args)
