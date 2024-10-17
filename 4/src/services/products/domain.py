import uuid
from shared.logger.logger import Logger


logger = Logger()


class ProductError(Exception):
    pass


class Product():

    def __init__(self, name: str, price: float, stock: int):
        errors = []

        self.__id = uuid.uuid4()

        if len(name) == 0:
            errors.append("name should not be empty")
        self.__name = name

        if price < 0:
            errors.append("price value should be positive")
        self.__price = price

        if stock < 0:
            errors.append("stock value should be positive")
        self.__stock = stock

        if len(errors) > 0:
            error_text = ", ".join(errors)
            logger.error(f"{self} {error_text}")
            raise ProductError(error_text)
        else:
            logger.log(f"{self} created")

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    def __repr__(self):
        return f"<Product(id={self.__id}, name={self.__name}, price={self.__price}, stock={self.__stock})>"

    def __hash__(self):
        return hash(self.__id)

    def update_stock(self, stock: int) -> None:
        if stock < 0:
            error_text = "stock value should be positive"
            logger.error(f"{self}, {error_text}")
            raise ProductError(error_text)
        self.__stock = stock
