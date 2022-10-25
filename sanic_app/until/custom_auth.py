from sanic_ext import validate
from sanic_jwt import exceptions
from tortoise.contrib.pydantic import pydantic_model_creator

from sanic_app.models import User, UserPydanticIn


@validate(json=UserPydanticIn, body_argument="user_params")
async def authenticate(request, user_params: UserPydanticIn, *args, **kwargs):
    user = await User.filter(**user_params.dict(exclude_unset=True)).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")
    if user.is_active is False:
        raise exceptions.AuthenticationFailed("User not confirm account.")
    return user.to_dict()
