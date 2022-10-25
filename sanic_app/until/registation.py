from sanic.response import json, text
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_jwt import BaseEndpoint, exceptions

# https://github.com/ahopkins/sanic-jwt/issues/111
# https://sanic-jwt.readthedocs.io/en/latest/pages/endpoints.html
from sanic_app.models import User
from sanic_app.serializers import UserRegistrationParams, Status, StatusLink


class Register(BaseEndpoint):
    @openapi.summary("Create new user")
    @openapi.description("Create new user")
    @openapi.response(200, {"status": bool, "link": str},
                      description="Data user registration")
    @openapi.definition(body={'application/json': UserRegistrationParams.schema()})
    @validate(json=UserRegistrationParams, body_argument="user_params")
    async def post(self, request, user_params: UserRegistrationParams, *args, **kwargs):
        user = await User.filter(username=user_params.username).first()
        if user is not None:
            raise exceptions.SanicUnauthorized(message="There is already such a user")

        user = await User.create(username=user_params.username,
                                 hashed_password=user_params.password1)

        # access_token, output = await self.responses.get_access_token_output(
        #     request, user.to_dict(), self.config, self.instance)
        # response = self.responses.get_token_response(request, access_token, output, config=self.config)

        return json(StatusLink(status=True,
                               link=f"http://localhost:8000/auth/confirm/{user.confirmation}").dict())


class Confirm(BaseEndpoint):
    @openapi.summary("Confirmation user")
    @openapi.description("Confirmation new user")
    @openapi.response(200, {"status": bool},
                      description="Status confirmation user")
    async def get(self, request, conf_key: str):
        users = await User.filter(confirmation=conf_key)
        if len(users) == 0:
            raise exceptions.AuthenticateNotImplemented("Error confirmation key")

        user = users[0]
        if user.is_active:
            raise exceptions.AuthenticateNotImplemented("Error confirmation key")
        else:
            user.is_active = True
            await user.save()
        return json(Status(status=True).dict())
