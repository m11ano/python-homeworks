from ..metaclasses.singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self, print: bool = True):
        self.__print = print

    def log(self, str: str, *args) -> None:
        if self.__print:
            print(f"\033[92mLog:\033[00m {str}", *args)

    def error(self, str: str, *args) -> None:
        if self.__print:
            print(f"\033[91mError log: {str}\033[00m", *args)
