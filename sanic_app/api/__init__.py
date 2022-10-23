from sanic import Blueprint

from .user import user

api = Blueprint.group(user, url_prefix="/api")