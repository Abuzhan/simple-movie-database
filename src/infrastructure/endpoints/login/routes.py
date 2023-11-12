from datetime import datetime

import jwt
from sanic import Blueprint

from src.infrastructure.endpoints.utils import create_response

LOGIN_ROUTES = Blueprint('login', url_prefix='/v1')


@LOGIN_ROUTES.post("/login")
async def do_login(request):
    current_date = datetime.utcnow()
    token = jwt.encode(
        {'datetime': current_date.isoformat()}, request.app.config.SECRET
    )
    return create_response({'token': token})
