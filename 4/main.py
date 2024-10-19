# Точка входа в приложение

import traceback
from src.shared.logger.logger import Logger
from src.services.store.service import StoreService
from src.services.products.domain import Product

logger = Logger()


def init_store() -> None:
    # Создаем сервис магазина
    store = StoreService()

    # Наполняем товара
    product_bread = Product("Хлеб", 100, 10)
    store.add_product(product_bread)

    product_sausage = Product("Колбаса", 500, 5)
    store.add_product(product_sausage)

    product_cheese = Product("Сыр", 300, 8)
    store.add_product(product_cheese)

    product_oil = Product("Масло", 200, 7)
    store.add_product(product_oil)

    # Выводим список товаров
    print("\nСписок товаров на старте:")
    store.list_products()
    print("")

    # Создаем заказ
    order = store.create_order()
    order.add_product(product_bread, 3)
    order.add_product(product_sausage, 4)
    order.add_product(product_cheese, 4)
    order.add_product(product_oil, 2)

    logger.log(f"order sum now is {order.calculate_total()}")

    # Выводим список товаров после заказа
    print("\nСписок товаров после заказа:")
    store.list_products()
    print("")

    # Делаем возврат части товаров
    order.return_product(product_bread, 1)
    order.return_product(product_oil)

    logger.log(f"order sum now is {order.calculate_total()}")

    # Полностью возвращаем заказ
    order.clear()

    logger.log(f"order sum now is {order.calculate_total()}")


def main() -> None:
    try:
        logger.log("app starting...")
        init_store()
        logger.log("all works fine...")

    except Exception as err:
        logger.error("app not started, something's wrong happend:", err)
        traceback.print_exc()


if __name__ == "__main__":
    main()
