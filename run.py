import os
import sys

from functools import partial

from sanic import Sanic
from sanic.worker.loader import AppLoader

from src.bootstrap import create_app


def start_server(_local: bool):
    loader = AppLoader(factory=partial(create_app))
    app = loader.load()
    host = os.environ.get("LOCAL_SERVER_HOST", "0.0.0.0")
    app.prepare(
        host=host,
        port=int(app.config["PORT"]),
        dev=_local,
        debug=_local,
        single_process=not _local,
    )

    if _local:
        Sanic.serve(primary=app, app_loader=loader)
        return

    Sanic.serve_single(primary=app)


if __name__ == "__main__":
    local = len(sys.argv) <= 1 or sys.argv[1] != "deployment"
    start_server(local)
