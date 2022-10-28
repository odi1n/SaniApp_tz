from sanic import Blueprint, exceptions
from sanic.response import HTTPResponse, json
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user
from tortoise import transactions
from tortoise.expressions import F

from sanic_app.models import Product, ProductPydanticOut, User, Bill, Transaction, TransactionPydanticOut
from sanic_app.serializers import TransactionParams

product = Blueprint("product", url_prefix="/product", strict_slashes=True)


@product.get('/', strict_slashes=False)
@openapi.summary("Get  products")
@openapi.description("Get all products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, ProductPydanticOut, description="Product params")
@protected()
async def get_products(request):
    products = await ProductPydanticOut.from_queryset(Product.all())
    return HTTPResponse(body=products.json())


@product.post('/', strict_slashes=False)
@openapi.summary("Buy products")
@openapi.description("Buy products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.definition(body={'application/json': TransactionParams.schema()})
@protected()
@inject_user()
@validate(json=TransactionParams, body_argument="transaction_params")
async def buy_products(request, user: User, transaction_params: TransactionParams):
    bill = await Bill.filter(id=transaction_params.bill_id,
                             user__id=user.get('id')).first()
    if bill is None:
        raise exceptions.NotFound("Incorrect score")

    product = await Product.filter(id=transaction_params.product_id).first()
    if product is None:
        raise exceptions.NotFound("Incorrect product")

    if bill.balance < product.price:
        raise exceptions.NotFound("Not balance")

    async with transactions.in_transaction():
        bill.balance = F("balance") - product.price
        await bill.save(update_fields=['balance'])
        transaction = await Transaction.create(bill=bill,
                                               product=product)
    transaction = await TransactionPydanticOut.from_tortoise_orm(transaction)
    return json(transaction.dict())
