from sanic import json
from sanic_ext import validate
from sanic_jwt import exceptions
from tortoise.contrib.pydantic import pydantic_model_creator

from sanic_app.models import User, UserPydanticIn, UserPydanticOut


@validate(json=UserPydanticIn, body_argument="user_params")
async def authenticate(request, user_params: UserPydanticIn, *args, **kwargs):
    user = await User.filter(**user_params.dict(exclude_unset=True)).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")
    if user.is_active is False:
        raise exceptions.AuthenticationFailed("User not confirm account.")
    return user


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        users = await User.filter(id=payload.get("user_id"))
        user_pydantic = await UserPydanticOut.from_tortoise_orm(users[0])
        user_pydantic.confirmation = str(user_pydantic.confirmation)
        return user_pydantic.dict()
    return None

async def my_scope_extender(user, *args, **kwargs):
    return user.get_scopes