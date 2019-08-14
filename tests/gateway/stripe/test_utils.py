from decimal import Decimal
from math import isclose
from saleor.payment.gateways.stripe_new import (
    get_amount_for_stripe,
    get_amount_from_stripe,
    get_currency_from_stripe,
    get_currency_for_stripe,
)


def test_get_amount_for_stripe():
    assert get_amount_for_stripe(Decimal(1), "USD") == 100
    assert get_amount_for_stripe(Decimal(1), "usd") == 100

    assert get_amount_for_stripe(Decimal(0.01), "USD") == 1
    assert get_amount_for_stripe(Decimal(24.24), "USD") == 2424
    assert get_amount_for_stripe(Decimal(42.42), "USD") == 4242

    assert get_amount_for_stripe(Decimal(1), "JPY") == 1
    assert get_amount_for_stripe(Decimal(1), "jpy") == 1


def test_get_amount_from_stripe():
    assert get_amount_from_stripe(100, "USD") == Decimal(1)
    assert get_amount_from_stripe(100, "usd") == Decimal(1)

    assert isclose(get_amount_from_stripe(1, "USD"), Decimal(0.01))
    assert isclose(get_amount_from_stripe(2424, "USD"), Decimal(24.24))
    assert isclose(get_amount_from_stripe(4242, "USD"), Decimal(42.42))

    assert get_amount_from_stripe(1, "JPY") == Decimal(1)
    assert get_amount_from_stripe(1, "jpy") == Decimal(1)


def test_get_currency_for_stripe():
    assert get_currency_for_stripe("USD") == "usd"
    assert get_currency_for_stripe("usd") == "usd"
    assert get_currency_for_stripe("uSd") == "usd"


def test_get_currency_from_stripe():
    assert get_currency_from_stripe("USD") == "USD"
    assert get_currency_from_stripe("usd") == "USD"
    assert get_currency_from_stripe("uSd") == "USD"
