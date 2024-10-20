from src.services.products.domain import Product
from src.services.orders.domain import Order
from src.shared.logger.logger import Logger

logger = Logger()


class StoreError(Exception):
    pass


class StoreService:
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

    # список из словарей (продукт, остаток на складе, сколько заказали)
    def get_list_products(self) -> list[tuple[Product, int, int]]:
        result = []

        products_ordered_count = {}
        for order in self.__orders:
            for product in order.products:
                if product not in products_ordered_count:
                    products_ordered_count[product] = order.products[product]
                else:
                    products_ordered_count[product] += order.products[product]

        for product in self.__products:
            ordered_count = (
                products_ordered_count[product]
                if product in products_ordered_count
                else 0
            )
            result.append((product, product.stock, ordered_count))

        return result

    # todo: плохая практика, печатать надо в контроллере
    def list_products(self) -> None:
        products = self.get_list_products()
        for product, stock, ordered_count in products:
            print(f"Товар {product.name} (id={product.id}), остаток на складе = {
                  stock}, продано всего = {ordered_count}")

    def __repr__(self):
        return "<StoreService>"
