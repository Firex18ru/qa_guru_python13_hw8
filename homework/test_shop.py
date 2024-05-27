import pytest
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    cart = Cart()
    return cart


@pytest.fixture
def not_empty_cart(cart, product):
    cart.add_product(product)
    return cart


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000)
        assert product.check_quantity(600)
        assert product.check_quantity(1111) is False

    def test_product_buy(self, product):
        expected = product.quantity - 1
        product.buy(1)
        assert product.quantity == expected

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:

    def test_product_clear_cart(self, product, not_empty_cart):
        not_empty_cart.remove_product(product)
        assert not_empty_cart.products == {}

    def test_clear(self, not_empty_cart):
        not_empty_cart.clear()
        assert not not_empty_cart.products

    def test_add_product_to_empty_cart(self, cart, product):
        cart.add_product(product)
        assert product in cart.products
        assert cart.products[product] == 1

    def test_add_product_quantity_to_cart(self, cart, product):
        quantity = 9
        cart.add_product(product, buy_count=quantity)
        assert product in cart.products
        assert cart.products[product] == quantity

    def test_buy_rase_value_error(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
