from sanic import Blueprint, text

auth = Blueprint("auth", url_prefix="/auth",  strict_slashes=True)

@auth.get('test', strict_slashes=False)
def handler(request):
    return text('OK')