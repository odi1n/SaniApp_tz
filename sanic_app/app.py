from sanic import Sanic
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from sanic_app.api import api
from sanic_app.config import Config, TORTOISE_ORM


def my_authenticate(request, *args, **kwargs):
    return dict(user_id='some_id')


app = Sanic("my-hello-world-app")
app.update_config(Config)

app.blueprint(api)
Initialize(app, authenticate=my_authenticate)  # jwt

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, )  # Tortoise

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,
            debug=True, auto_reload=True)
