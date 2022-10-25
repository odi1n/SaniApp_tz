from textwrap import dedent

from sanic import Sanic
from sanic_ext import openapi, validate
from sanic_jwt import initialize, Initialize
from sanic_jwt.endpoints import AuthenticateEndpoint
from tortoise.contrib.sanic import register_tortoise

from sanic_app.api import api
from sanic_app.config import Config, TORTOISE_ORM
# Sanic
from sanic_app.until import authenticate, retrieve_user
from sanic_app.until.registation import Register, Confirm

app = Sanic("my-hello-world-app")
# config
app.update_config(Config)

# router
app.blueprint(api)

my_views = (
    ('/register', Register),
    ('/confirm/<conf_key>', Confirm),
)
Initialize(app,
           authenticate=authenticate,
           retrieve_user=retrieve_user,
           class_views=my_views)  # jwt

# swagger
app.ext.openapi.describe(
    "Sanic_app test api",
    version="1.0.0",
    description=dedent(
        """
        # Info
        This is a description. It is a good place to add some _extra_ doccumentation.

        **MARKDOWN** is supported.
        """
    ),
)

# DB
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, )  # Tortoise

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,
            debug=False, auto_reload=True)
