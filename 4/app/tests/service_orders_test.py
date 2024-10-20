import pytest

from src.shared.logger.logger import Logger

from src.services.products.domain import Product
from src.services.orders.domain import Order, OrderError

logger = Logger()
logger.set_mock(True)


def test_order_creation():
    # Проверим корректное создание заказа
    order = Order()
    assert len(order.id) > 0
    assert order.products == {}


def test_add_product_to_order():
    # Проверим корректное добавление продукта в заказ
    product = Product("Test Product", 10.0, 5)
    order = Order()

    order.add_product(product, 2)

    assert order.products[product] == 2
    assert product.stock == 3

    order.add_product(product, 1)

    assert order.products[product] == 3
    assert product.stock == 2


def test_add_product_quantity_error():
    # Проверим выброс исключения при добавлении продукта с количеством <= 0
    product = Product("Test Product", 10.0, 5)
    order = Order()

    with pytest.raises(OrderError):
        order.add_product(product, 0)


def test_add_product_stock_error():
    # Проверим выброс исключения при добавлении продукта в количестве больше, чем на складе
    product = Product("Test Product", 10.0, 5)
    order = Order()

    with pytest.raises(OrderError):
        order.add_product(product, 10)


def test_calculate_total():
    # Проверим корректный расчет суммы заказа
    product1 = Product("Product 1", 10.0, 20)
    product2 = Product("Product 2", 20.0, 20)
    order1 = Order()
    order2 = Order()

    order1.add_product(product1, 2)
    order1.add_product(product2, 1)

    order2.add_product(product1, 5)
    order2.add_product(product2, 10)

    assert order1.calculate_total() == 40.0
    assert order2.calculate_total() == 250.0


def test_return_product():
    # Проверим корректный возврат продукта из заказа
    product = Product("Test Product", 10.0, 10)
    order = Order()

    order.add_product(product, 5)
    order.return_product(product, 1)

    assert order.products[product] == 4
    assert product.stock == 6

    order.return_product(product)

    assert product not in order.products
    assert product.stock == 10


def test_return_nonexistent_product_error():
    # Проверим, что при попытке вернуть несуществующий продукт выбрасывается ошибка
    product = Product("Test Product", 10.0, 5)
    order = Order()

    with pytest.raises(OrderError):
        order.return_product(product)


def test_clear_order():
    # Проверим полную очистку заказа
    product1 = Product("Product 1", 10.0, 5)
    product2 = Product("Product 2", 20.0, 10)
    order = Order()

    order.add_product(product1, 2)
    order.add_product(product2, 3)
    order.clear()

    assert order.products == {}
    assert product1.stock == 5
    assert product2.stock == 10
