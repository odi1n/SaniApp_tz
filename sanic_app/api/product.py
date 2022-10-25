from sanic import Blueprint
from sanic.response import text, json, HTTPResponse
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected

from sanic_app.models import Product, ProductPydanticOut

product = Blueprint("product", url_prefix="/product", strict_slashes=True)


@openapi.summary("Get  products")
@openapi.description("Get all products")
@openapi.parameter("Authorization", str, "Bearer Token")
@product.get('/list', strict_slashes=False)
@protected()
async def get_products(request):
    products = await ProductPydanticOut.from_queryset(Product.all())
    return HTTPResponse(body=products.json())