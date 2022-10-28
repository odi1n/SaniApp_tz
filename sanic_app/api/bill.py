from sanic import Blueprint
from sanic.response import HTTPResponse
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user

from sanic_app.models import BillQueryCreate, Bill, User

bill = Blueprint("bill", url_prefix="/bill", strict_slashes=True)


@bill.get('/', strict_slashes=False)
@openapi.summary("Get bills")
@openapi.description("Get all bills")
@openapi.parameter("Authorization", str, "Bearer Token")
@protected()
@inject_user()
async def get_bills(request, user: User):
    bill = await BillQueryCreate.from_queryset(Bill.filter(user__id=user.get('id')).all())
    return HTTPResponse(body=bill.json(), content_type="application/json")
