from src.infrastructure.endpoints.utils import create_response


def handle_400():
    message = 'Request was invalid'
    return create_response(error_code='BAD_REQUEST', message=message, status_code=400)


def handle_404():
    message = 'Requested URL was not found'
    return create_response(error_code='NOT_FOUND', message=message, status_code=404)


def handle_405():
    message = 'Method not allowed'
    return create_response(error_code='NOT_ALLOWED', message=message, status_code=405)


def handle_500(e):
    return create_response(error_code='SERVER_ERROR', message=str(e), status_code=500)
