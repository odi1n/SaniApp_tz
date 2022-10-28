from sanic import Blueprint

from .product import product
from .transaction import transaction
from .bill import bill
from .payment import payment

api = Blueprint.group(bill,
                      product,
                      transaction,
                      payment,
                      url_prefix="/api")
