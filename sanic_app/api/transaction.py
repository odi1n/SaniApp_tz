from sanic import Blueprint, HTTPResponse
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected

from sanic_app.models import TransactionQueryCreate, Transaction

transaction = Blueprint("transaction", url_prefix="/transaction", strict_slashes=True)


@transaction.get('/', strict_slashes=False)
@openapi.summary("Get transactions")
@openapi.description("Get all transactions")
@openapi.parameter("Authorization", str, "Bearer Token")
@protected()
async def get_transactions(request):
    transaction = await TransactionQueryCreate.from_queryset(Transaction.all())
    return HTTPResponse(body=transaction.json())
