from sanic_ext import validate
from sanic_jwt import exceptions

from sanic_app.models import User
from sanic_app.params import UserAuthParams


@validate(json=UserAuthParams, body_argument="user_params")
async def authenticate(request, user_params: UserAuthParams, *args, **kwargs):
    user = await User.filter(username__icontains=user_params.username,
                             hashed_password=user_params.password).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")
    return user.to_dict()
