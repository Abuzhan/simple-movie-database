from functools import wraps

import jwt

from src.infrastructure.endpoints import create_response


def check_token(request):
    if not request.token:
        return False

    try:
        jwt.decode(request.token, request.app.config.SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return create_response(
                    error_code="UNAUTHORIZED",
                    message="You are not authorized to access this resource",
                    status_code=401,
                )

        return decorated_function

    return decorator(wrapped)
