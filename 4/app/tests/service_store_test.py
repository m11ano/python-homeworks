import pytest

from src.shared.logger.logger import Logger

from src.services.products.domain import Product
from src.services.orders.domain import Order
from src.services.store.service import StoreService, StoreError

logger = Logger()
logger.set_mock(True)


def test_store_service_creation():
    # Проверим корректное создание магазина
    store = StoreService()
    assert store.get_list_products() == []


def test_add_product_to_store():
    # Проверим корректное добавление продукта в магазин
    product = Product("Test Product", 10.0, 5)
    store = StoreService()

    store.add_product(product)
    products_list = store.get_list_products()

    assert len(products_list) == 1
    assert products_list[0][0] == product
    assert products_list[0][1] == 5
    assert products_list[0][2] == 0


def test_add_existing_product_error():
    # Проверим выброс исключения при добавлении продукта, который уже добавлен
    product = Product("Test Product", 10.0, 5)
    store = StoreService()

    store.add_product(product)
    with pytest.raises(StoreError):
        store.add_product(product)


def test_create_order():
    # Проверим корректное создание нового заказа
    store = StoreService()

    order = store.create_order()
    assert isinstance(order, Order)


def test_get_list_products_with_orders():
    # Проверим корректный список продуктов с учетом заказов
    product1 = Product("Product 1", 10.0, 5)
    product2 = Product("Product 2", 20.0, 10)
    store = StoreService()

    store.add_product(product1)
    store.add_product(product2)

    # Создаем заказ и добавляем продукт
    order1 = store.create_order()
    order1.add_product(product1, 1)

    order2 = store.create_order()
    order2.add_product(product1, 1)

    products_list = store.get_list_products()

    assert len(products_list) == 2
    assert products_list[0][0] == product1
    assert products_list[0][1] == 3  # Остаток на складе
    assert products_list[0][2] == 2  # Заказано 3
    assert products_list[1][0] == product2
    assert products_list[1][1] == 10  # Остаток не изменился, т.к. продукт не заказывали
    assert products_list[1][2] == 0  # Заказов нет
