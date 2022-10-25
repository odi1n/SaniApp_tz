from sanic import Blueprint

from .product import product

api = Blueprint.group(product, url_prefix="/api")