from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import BaseEndpoint, exceptions

# https://github.com/ahopkins/sanic-jwt/issues/111
# https://sanic-jwt.readthedocs.io/en/latest/pages/endpoints.html
from sanic_app.models import User
from sanic_app.params import UserRegistrationParams


class Register(BaseEndpoint):
    @openapi.summary("Login a user")
    @openapi.description("Authorization user in service")
    @openapi.parameter("Authorization", str, "header")
    @openapi.response(200, {"access_token": str, "refresh_token": str},
                      description="the token to use for api interaction")
    @openapi.definition(body={'application/json': UserRegistrationParams.schema()})
    @validate(json=UserRegistrationParams, body_argument="user_params")
    async def post(self, request, user_params: UserRegistrationParams, *args, **kwargs):
        user = await User.filter(username=user_params.username).first()
        if user is not None:
            return exceptions.SanicUnauthorized(message="There is already such a user")
        user = await User.create(username=user_params.username,
                                 hashed_password=user_params.password1)

        access_token, output = await self.responses.get_access_token_output(
            request,
            user.to_dict(),
            self.config,
            self.instance)

        response = self.responses.get_token_response(
            request,
            access_token,
            output,
            config=self.config)

        return response
