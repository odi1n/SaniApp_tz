from sanic import Blueprint
from .webhook import webhook

payment = Blueprint.group(webhook,
                      url_prefix="/payment")
