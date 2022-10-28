from sanic import Blueprint
from sanic.response import HTTPResponse
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user

from sanic_app.models import BillQueryCreate, Bill, User

webhook = Blueprint("webhook", url_prefix="/webhook", strict_slashes=True)


@webhook.get('/', strict_slashes=False)
# @openapi.summary("Get bills")
# @openapi.description("Get all bills")
# @openapi.parameter("Authorization", str, "Bearer Token")
# @protected()
# @inject_user()
async def set_webhook(request, user: User):
    pass