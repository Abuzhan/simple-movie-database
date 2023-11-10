import jwt
from sanic import Blueprint, text

LOGIN_ROUTES = Blueprint('login', url_prefix='/v1')


@LOGIN_ROUTES.post("/login")
async def do_login(request):
    token = jwt.encode({'some': 'payload'}, request.app.config.SECRET)
    return text(token)
