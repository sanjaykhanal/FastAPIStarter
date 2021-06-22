from enum import Enum



from .api.example_console import router as example_console_router, start_example_console
from .api.example_console import routes as example_console_routes


class routers(Enum):
    example_console: list = [example_console_router]


class routes(Enum):
    example_console: list = [example_console_routes]


class cruds(Enum):
    example_console: list = []


class models(Enum):
    example_console: list = []


class schemas(Enum):
    example_console: list = []


class scopes(Enum):
    super_admin: list = [
        *[r.name for r in example_console_routes]
    ]

    admin: list = [
        *[r.name for r in example_console_routes]
    ]

    monitor: list = [
        *[r.name for r in example_console_routes]
    ]

    visitor: list = [
        *[r.name for r in example_console_routes]
    ]
