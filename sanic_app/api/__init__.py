from sanic import Blueprint

from .product import product
from .transaction import transaction
from .bill import bill
from .payment import payment
from .user import user

api = Blueprint.group(bill,
                      product,
                      transaction,
                      payment,
                      user,
                      url_prefix="/api")
