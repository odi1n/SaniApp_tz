from sanic import Blueprint, text
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected

product = Blueprint("product", url_prefix="/product",  strict_slashes=True)


@openapi.summary("Get  products")
@openapi.description("Get all products")
@openapi.parameter("Authorization", str, "Bearer Token")
@product.get('/list', strict_slashes=False)
@protected()
async def get_products(request):
    return text('OK')