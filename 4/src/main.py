# Точка входа в приложение

from shared.logger.logger import Logger
from services.store.service import StoreService
from services.products.domain import Product

logger = Logger()


def init_store() -> None:
    store = StoreService()

    product_bread = Product('Хлеб', 100, 10)
    store.add_product(product_bread)

    product_sausage = Product('Колбаса', 500, 5)
    store.add_product(product_sausage)

    product_cheese = Product('Сыр', 300, 8)
    store.add_product(product_cheese)

    product_oil = Product('Масло', 200, 7)
    store.add_product(product_oil)

    order = store.create_order()
    order.add_product(product_bread, 3)
    order.add_product(product_sausage, 4)
    order.add_product(product_cheese, 4)
    order.add_product(product_oil, 2)

    logger.log(order.calculate_total())

    order.return_product(product_bread, 1)
    order.return_product(product_oil)

    logger.log(order.calculate_total())

    order.clear()

    logger.log(order.calculate_total())


def main() -> None:
    try:
        logger.log('app starting...')
        init_store()
        logger.log('all works fine...')

    except Exception as err:
        logger.error(f"app not started, something's wrong happend: {err}")


if __name__ == '__main__':
    main()
