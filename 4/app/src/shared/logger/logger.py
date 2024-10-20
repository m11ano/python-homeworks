from src.shared.metaclasses.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self.__mock = False

    def set_mock(self, value: bool) -> None:
        self.__mock = value

    def log(self, str: str, *args) -> None:
        if not self.__mock:
            print(f"\033[92mLog:\033[00m {str}", *args)

    def error(self, str: str, *args) -> None:
        if not self.__mock:
            print(f"\033[91mError log: {str}\033[00m", *args)
