from services.products.domain import Product
from services.orders.domain import Order
from shared.logger.logger import Logger

logger = Logger()


class StoreError(Exception):
    pass


class StoreService():

    __products: list[Product] = []
    __orders: list[Order] = []

    def add_product(self, product: Product) -> None:
        if product.stock < 0:
            error_text = "stock should be positive"
            logger.error(f"{self} - {product} {error_text}")
            raise StoreError(error_text)

        if product in self.__products:
            error_text = "product already added to store"
            logger.error(f"{self} - {product} {error_text}")
            raise StoreError(error_text)

        self.__products.append(product)
        logger.log(f"{self} - {product} added to store")

    def create_order(self) -> Order:
        order = Order()
        self.__orders.append(order)
        return Order()

    def __repr__(self):
        return f"<StoreService>"
