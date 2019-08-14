from decimal import Decimal

import pytest

from saleor.payment.gateways.stripe_new.forms import (
    StripeCheckoutWidget,
    StripePaymentModalForm,
)
from saleor.payment.gateways.stripe_new import create_form

from saleor.payment.interface import GatewayConfig
from saleor.payment.utils import create_payment_information

TRANSACTION_AMOUNT = Decimal(42.42)
TRANSACTION_CURRENCY = "USD"
FAKE_TOKEN = "fake-token"


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


def test_widget_with_additional_attr(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment)

    widget = StripeCheckoutWidget(
        payment_info,
        gateway_config.connection_params,
        attrs={"data-custom": "custom-data"},
    )
    assert 'data-custom="custom-data"' in widget.render()


def test_widget_with_prefill_option(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment)
    connection_params = gateway_config.connection_params
    connection_params["prefill"] = True
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-email="test@example.com"' in widget.render()

    connection_params["prefill"] = False
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-email="test@example.com"' not in widget.render()


def test_widget_with_remember_me_option(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment)
    connection_params = gateway_config.connection_params

    connection_params["remember_me"] = True
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-allow-remember-me="true"' in widget.render()

    connection_params["remember_me"] = False
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-allow-remember-me="false"' in widget.render()


def test_widget_with_enable_billing_address_option(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment, FAKE_TOKEN)
    connection_params = gateway_config.connection_params

    connection_params["enable_billing_address"] = True
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-billing-address="true"' in widget.render()
    assert 'data-zip-code="true"' in widget.render()

    connection_params["enable_billing_address"] = False
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-billing-address="false"' in widget.render()
    assert 'data-zip-code="false"' in widget.render()


def test_widget_with_enable_shipping_address_option(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment, FAKE_TOKEN)
    connection_params = gateway_config.connection_params

    connection_params["enable_shipping_address"] = True
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-shipping-address="true"' in widget.render()

    connection_params["enable_shipping_address"] = False
    widget = StripeCheckoutWidget(payment_info, connection_params)
    assert 'data-shipping-address="false"' in widget.render()


def test_stripe_payment_form(stripe_payment, gateway_config):
    payment_info = create_payment_information(stripe_payment, FAKE_TOKEN)
    form = create_form(
        None,
        payment_information=payment_info,
        connection_params=gateway_config.connection_params,
    )
    assert isinstance(form, StripePaymentModalForm)
    assert not form.is_valid()

    form = create_form(
        data={"stripeToken": FAKE_TOKEN},
        payment_information=payment_info,
        connection_params=gateway_config.connection_params,
    )
    assert isinstance(form, StripePaymentModalForm)
    assert form.is_valid()
