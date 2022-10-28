from sanic import Blueprint, json
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user, exceptions
from tortoise import transactions
from tortoise.expressions import F

from sanic_app.config import Config
from sanic_app.models import User, Transaction, Bill
from sanic_app.serializers import WebhookParams
from sanic_app.until import decrypto

webhook = Blueprint("webhook", url_prefix="/webhook", strict_slashes=True)


@webhook.post('/', strict_slashes=False)
@openapi.summary("Webhook")
@openapi.description("Webhook balance")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, {"json": WebhookParams.schema()}, description="Model Webhook")
@inject_user()
@validate(json=WebhookParams, body_argument="webhook_params")
async def set_webhook(request, user: User, webhook_params: WebhookParams):
    decrypt = decrypto(private_key=Config.private_key,
                       transaction_id=webhook_params.transaction_id,
                       user_id=webhook_params.user_id,
                       bill_id=webhook_params.bill_id,
                       amount=0)
    if webhook_params.signature != decrypt:
        exceptions.RequiredKeysNotFound("Error signature")

    transaction = await Transaction.filter(id=webhook_params.transaction_id).first()
    if transaction is None:
        raise exceptions.RequiredKeysNotFound("Transaction error id")

    bill = await Bill.filter(id=webhook_params.bill_id).first()
    if bill is None:
        raise exceptions.RequiredKeysNotFound("Transaction error id")

    async with transactions.in_transaction():
        bill.balance = F('balance') + webhook_params.amount
        await bill.save(update_fields=['balance'])

    return json({"status": "ok"})
