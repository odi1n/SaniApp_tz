from sanic import Blueprint, exceptions
from sanic.response import HTTPResponse, json
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user, scoped
from tortoise import transactions
from tortoise.expressions import F

from sanic_app.models import Product, ProductQueryCreate, User, Bill, Transaction, TransactionModelCreate, \
    ProductModelCreateExl, ProductModelCreate
from sanic_app.serializers import TransactionParams, Status

product = Blueprint("product", url_prefix="/product", strict_slashes=True)


@product.get('/', strict_slashes=False)
@openapi.summary("Get  products")
@openapi.description("Get all products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, ProductQueryCreate, description="Product params")
@protected()
async def get_product(request):
    products = await ProductQueryCreate.from_queryset(Product.all())
    return HTTPResponse(body=products.json(), content_type="application/json")


@product.post('/', strict_slashes=False)
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, ProductModelCreate, description="Product params")
@openapi.definition(body={'application/json': ProductModelCreateExl})
@protected()
@scoped('admin')
@validate(json=ProductModelCreateExl, body_argument="product_params")
async def create_product(request, product_params: ProductModelCreateExl):
    product = await Product.create(**product_params.dict())
    product_ser = await ProductModelCreate.from_tortoise_orm(product)
    return HTTPResponse(product_ser.json(), content_type="application/json")


@product.put('/<product_id>', strict_slashes=False)
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, ProductModelCreate, description="Product params")
@openapi.definition(body={'application/json': ProductModelCreateExl})
@protected()
@scoped('admin')
@validate(json=ProductModelCreateExl, body_argument="product_params")
async def update_product(request, product_id: int, product_params: ProductModelCreateExl):
    product = await Product.filter(id=product_id).first()
    if not product:
        raise exceptions.NotFound("Error product id")
    product = await product.update_from_dict(product_params.dict())
    product_ser = await ProductModelCreate.from_tortoise_orm(product)
    return HTTPResponse(product_ser.json(), content_type="application/json")


@product.delete('/<product_id>', strict_slashes=False)
@openapi.parameter("Authorization", str, "Bearer Token")
@protected()
@scoped('admin')
async def delete_product(request, product_id: int):
    product = await Product.filter(id=product_id).first()
    if not product:
        raise exceptions.NotFound("Incorrect product id")
    await product.delete()
    return HTTPResponse(Status().json(), content_type="application/json", status=204)


@product.post('buy/', strict_slashes=False)
@openapi.summary("Buy products")
@openapi.description("Buy products")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.definition(body={'application/json': TransactionParams.schema()})
@openapi.response(200, TransactionModelCreate, description="Buy model")
@protected()
@inject_user()
@validate(json=TransactionParams, body_argument="transaction_params")
async def buy_product(request, user: User, transaction_params: TransactionParams):
    bill = await Bill.filter(id=transaction_params.bill_id, user__id=user.id).first()
    if bill is None:
        raise exceptions.NotFound("Incorrect bill id")

    product = await Product.filter(id=transaction_params.product_id).first()
    if product is None:
        raise exceptions.NotFound("Incorrect product id")

    if bill.balance < product.price:
        raise exceptions.NotFound("Not balance")

    async with transactions.in_transaction():
        bill.balance = F("balance") - product.price
        await bill.save(update_fields=['balance'])
        transaction = await Transaction.create(bill=bill, product=product)

    transaction = await TransactionModelCreate.from_tortoise_orm(transaction)
    return json(transaction.dict())
