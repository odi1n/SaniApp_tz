from sanic import Blueprint, json, HTTPResponse
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import protected, inject_user, scoped
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from sanic_app.models import User, UserPydanticOut
from sanic_app.serializers.params.user_params import UserUpdate

user = Blueprint("user", url_prefix="/user", strict_slashes=True)


@user.get('/', strict_slashes=False)
@openapi.summary("Get user_apis")
@openapi.description("Get all user_apis")
@openapi.parameter("Authorization", str, "Bearer Token")
@protected()
@scoped('admin')
async def get_list(request):
    test = pydantic_queryset_creator(User)
    user_pydantic = await test.from_queryset(User.all())
    return HTTPResponse(user_pydantic.json(), content_type="application/json")


@user.put('/<user_id>', strict_slashes=False)
@openapi.summary("Get user_apis")
@openapi.description("Get all user_apis")
@openapi.parameter("Authorization", str, "Bearer Token")
@openapi.response(200, {}, description="Product params")
@openapi.definition(body={'application/json': UserUpdate.schema()})
@protected()
@scoped('admin')
@validate(json=UserUpdate, body_argument="user_params")
async def update_user(request, user_id: int, user_params: UserUpdate):
    user = await User.filter(id=user_id).first()
    if not user:
        pass
    user.is_active = user_params.is_active
    await user.save(update_fields=['is_active'])
    test = await UserPydanticOut.from_tortoise_orm(user)
    return HTTPResponse(test.json(), content_type="application/json")
