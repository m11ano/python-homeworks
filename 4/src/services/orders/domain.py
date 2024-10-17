from services.products.domain import Product
from shared.logger.logger import Logger
import uuid

logger = Logger()


class OrderError(Exception):
    pass


class Order():

    __products: dict[Product, int] = {}

    def __init__(self):
        self.__id = uuid.uuid4()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def products(self):
        return self.__products

    def add_product(self, product: Product, quantity: int) -> None:
        if quantity < 0:
            error_text = "quantity should positive"
            logger.error(f"{self} - {product} {error_text}")
            raise OrderError(error_text)

        if product in self.__products:
            if self.__products[product] + quantity > product.stock:
                error_text = "cannot add more items than are in stock"
                logger.error(f"{self} - {product} {error_text}")
                raise OrderError(error_text)
            self.__products[product] += quantity
        else:
            if quantity > product.stock:
                error_text = "cannot add more items than are in stock"
                logger.error(f"{self} - {product} {error_text}")
                raise OrderError(error_text)
            self.__products[product] = quantity

        logger.log(f"{self} - {product} added to order")

    def calculate_total(self) -> float:
        total = 0
        for product in self.__products:
            total += product.price * self.__products[product]

        return total

    def __repr__(self):
        return f"<Order(id={self.__id})>"

    def __hash__(self):
        return hash(self.__id)
