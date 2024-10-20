import pytest

from src.shared.logger.logger import Logger

from src.services.products.domain import Product, ProductError

logger = Logger()
logger.set_mock(True)


def test_valid_product_creation():
    # Проверим корректное создание объекта
    product = Product("Test Product", 10.5, 5)

    assert product.name == "Test Product"
    assert product.price == 10.5
    assert product.stock == 5
    assert len(product.id) > 0


def test_exception_on_product_creation():
    # Проверим валидацию ошибок при создании объекта

    with pytest.raises(ProductError):
        Product("", 10.0, 5)

    with pytest.raises(ProductError):
        Product("Test Product", -1, 5)

    with pytest.raises(ProductError):
        Product("Test Product", 10.5, -1)


def test_update_stock_valid():
    # Проверим корректное обновление запаса, а также валидацию ошибок

    product = Product("Test Product", 10.5, 5)
    product.update_stock(3)
    assert product.stock == 8

    product.update_stock(-6)
    assert product.stock == 2

    with pytest.raises(ProductError):
        product.update_stock(-3)
