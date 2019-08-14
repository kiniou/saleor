from decimal import Decimal

import pytest

from saleor.payment.gateways.stripe_new.forms import StripeCheckoutWidget

from saleor.payment.interface import GatewayConfig
from saleor.payment.utils import create_payment_information

TRANSACTION_AMOUNT = Decimal(42.42)
TRANSACTION_CURRENCY = "USD"


@pytest.fixture()
def gateway_config():
    return GatewayConfig(
        gateway_name="stripe",
        auto_capture=False,
        template_path="template.html",
        connection_params={
            "public_key": "public",
            "secret_key": "secret",
            "store_name": "Saleor",
            "store_image": "image.gif",
            "prefill": True,
            "remember_me": True,
            "locale": "auto",
            "enable_billing_address": False,
            "enable_shipping_address": False,
        },
    )


@pytest.fixture()
def stripe_payment(payment_dummy):
    payment_dummy.total = TRANSACTION_AMOUNT
    payment_dummy.currency = TRANSACTION_CURRENCY
    return payment_dummy


def test_widget_with_default_options(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment)
    widget = StripeCheckoutWidget(payment_info, gateway_config.connection_params)
    assert widget.render() == (
        '<script class="stripe-button" data-allow-remember-me="true" '
        'data-amount="4242" data-billing-address="false" data-currency="USD" '
        'data-description="Total payment" data-email="test@example.com" '
        'data-image="image.gif" data-key="public" data-locale="auto" '
        'data-name="Saleor" data-shipping-address="false" '
        'data-zip-code="false" src="https://checkout.stripe.com/checkout.js">'
        "</script>"
    )
