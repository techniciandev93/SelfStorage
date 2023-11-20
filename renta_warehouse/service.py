import uuid

from django.conf import settings

from yookassa import Configuration
from yookassa import Payment


def create_payment_order(amount, order_num,):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
          "value": f"{amount}",
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "confirmation": {
          "type": "redirect",
          "return_url": f"http://127.0.0.1:8000/order_confirmation/?&order={order_num}"
        },
        "description": f"Заказ №{order_num}"
    }, idempotence_key)

    confirmation = payment.confirmation.confirmation_url
    return confirmation
