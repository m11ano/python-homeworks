import uuid
from src.services.products.domain import Product
from src.shared.logger.logger import Logger

logger = Logger()


class OrderError(Exception):
    pass


class Order:
    __products: dict[Product, int] = {}

    def __init__(self):
        self.__id = str(uuid.uuid4())

    @property
    def id(self) -> str:
        return self.__id

    @property
    def products(self):
        return self.__products

    def add_product(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            error_text = "quantity should more then zero"
            logger.error(f"{self} - {product} {error_text}")
            raise OrderError(error_text)

        if product.stock < quantity:
            error_text = f"cannot add {quantity} items, thats more then stock"
            logger.error(f"{self} - {product} {error_text}")
            raise OrderError(error_text)

        # Tx start
        if product in self.__products:
            self.__products[product] += quantity
        else:
            self.__products[product] = quantity

        product.update_stock(-quantity)
        # Tx end

        logger.log(f"{self} - {product} added to order")

    def calculate_total(self) -> float:
        total: float = 0
        for product in self.__products:
            total += product.price * self.__products[product]

        return total

    def return_product(self, product: Product, quantity: int | None = None) -> None:
        if product not in self.__products:
            error_text = "cant return product, dont exists in order"
            logger.error(f"{self} - {product} {error_text}")
            raise OrderError(error_text)

        if quantity is None:
            quantity = self.__products[product]

        # Tx start
        product.update_stock(quantity)
        if quantity == self.__products[product]:
            del self.__products[product]
        else:
            self.__products[product] -= quantity
        # Tx end

        logger.log(f"{self} - {product} returned to store")

    def clear(self) -> None:
        # Tx start
        for product in self.__products:
            product.update_stock(product.stock + self.__products[product])
        self.__products.clear()
        # Tx end

        logger.log(f"{self} products list cleared, all returned to store")

    def __repr__(self):
        return f"<Order(id={self.__id})>"

    def __hash__(self):
        return hash(self.__id)
