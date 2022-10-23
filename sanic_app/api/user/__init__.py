from sanic import Blueprint

from .auth import auth

user = Blueprint.group(auth, url_prefix="/user")