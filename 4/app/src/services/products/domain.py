import uuid
from src.shared.logger.logger import Logger


logger = Logger()


class ProductUpdateStockError(Exception):
    pass


class Product:
    def __init__(self, name: str, price: float, stock: int):
        errors = []

        self.__id = str(uuid.uuid4())

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
            raise ValueError(error_text)
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

    def update_stock(self, delta: int) -> None:
        if self.__stock + delta < 0:
            error_text = f"total stock value should be positive, stock={self.__stock}, delta={delta}"
            logger.error(f"{self}, {error_text}")
            raise ProductUpdateStockError(error_text)

        old_stock = self.__stock
        self.__stock += delta
        logger.log(
            f"{self} stock updated by delta={delta} (prev stock value={old_stock})"
        )
