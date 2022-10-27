from sanic import Blueprint

from .product import product
from .transaction import transaction
from .bill import bill

api = Blueprint.group(bill,
                      product,
                      transaction,
                      url_prefix="/api")
