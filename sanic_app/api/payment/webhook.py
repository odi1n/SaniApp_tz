from sanic import Blueprint, json, exceptions
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from tortoise import transactions
from tortoise.expressions import F

from sanic_app.config import Config
from sanic_app.models import Transaction, Bill
from sanic_app.serializers import WebhookParams, Status
from sanic_app.until import decrypto

webhook = Blueprint("webhook", url_prefix="/webhook", strict_slashes=True)


@webhook.post('/', strict_slashes=False)
@openapi.summary("Webhook")
@openapi.description("Webhook balance")
@openapi.response(200, {"json": Status}, description="Model Webhook")
@openapi.definition(body={'application/json': WebhookParams})
@validate(json=WebhookParams, body_argument="webhook_params")
async def set_webhook(request, webhook_params: WebhookParams):
    decrypt = decrypto(private_key=Config.private_key,
                       transaction_id=webhook_params.transaction_id,
                       user_id=webhook_params.user_id,
                       bill_id=webhook_params.bill_id,
                       amount=0)
    if webhook_params.signature != decrypt:
        exceptions.NotFound("Error signature")

    transaction = await Transaction.filter(id=webhook_params.transaction_id).first()
    if transaction is None:
        raise exceptions.NotFound("Incorrect transaction id")

    bill = await Bill.filter(id=webhook_params.bill_id).first()
    if bill is None:
        raise exceptions.NotFound("Incorrect bill id")

    async with transactions.in_transaction():
        bill.balance = F('balance') + webhook_params.amount
        await bill.save(update_fields=['balance'])

    return json(Status().dict())
