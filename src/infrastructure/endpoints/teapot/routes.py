from sanic import Blueprint

from src.infrastructure.endpoints.utils import create_response

TEAPOT_ROUTES = Blueprint('teapot')

CAN_I_BREW_COFFEE = False


@TEAPOT_ROUTES.post("/brew-coffee")
async def brew_coffee(request):
    return create_response(
        status_code=418,
        data={'result': 'This server is a teapot, thus it cannot brew coffee.'},
    )
