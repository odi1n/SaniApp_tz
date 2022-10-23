from textwrap import dedent

from sanic import Sanic
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from sanic_app.api import api
from sanic_app.config import Config, TORTOISE_ORM


def my_authenticate(request, *args, **kwargs):
    return dict(user_id='some_id')


# Sanic
app = Sanic("my-hello-world-app")
# config
app.update_config(Config)

# router
app.blueprint(api)
Initialize(app, authenticate=my_authenticate)  # jwt

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
            debug=True, auto_reload=True)
