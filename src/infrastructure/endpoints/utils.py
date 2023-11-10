from sanic.response import json


def create_response(
    data=None, error_code: str = None, message: str = None, status_code: int = None
):
    if status_code is None:
        status_code = _get_default_status_code(data, error_code)

    response = {}

    if data is not None:
        response['data'] = data
    if error_code is not None:
        response['error'] = _format_error(error_code, message)

    headers = {'Content-Type': 'application/json'}
    return json(response, status=status_code, headers=headers)


def _get_default_status_code(data=None, error=None):
    if data is not None:
        return 200

    if error is not None:
        return 400

    return 204


def _format_error(error_code: str, message: str):
    return {'code': error_code, 'message': message}


__all__ = ['create_response']
