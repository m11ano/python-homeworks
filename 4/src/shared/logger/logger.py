from ..metaclasses.singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self, print: bool = True):
        self.__print = print

    def log(self, str: str) -> None:
        if self.__print:
            print(f"Log: {str}")

    def error(self, str: str) -> None:
        if self.__print:
            print(f"Error log: {str}")
