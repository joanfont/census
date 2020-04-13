from starlette.applications import Starlette
from census.config import config
from census.routes import routes
from census.errors import exception_handlers


app = Starlette(
    debug=config.DEBUG,
    routes=routes,
    exception_handlers=exception_handlers
)
