from enum import Enum

from .api.users import router as users_router
from .api.users import routes as users_routes

from .crud.users import username_exists,\
    create_user,\
    update_user,\
    update_password,\
    login,\
    get_by_id,\
    get_by_username,\
    user_list,\
    delete_user,\
    get_email_address

from .models.users import Users

from .schema.users import LoginBase,\
    UpdatePassword,\
    PasswordChangeRequest,\
    UserBase,\
    UserCreate,\
    UserUpdate,\
    User


class routers(Enum):
    users: list = [users_router]


class routes(Enum):
    users: list = [users_routes]


class cruds(Enum):
    users: list = [username_exists, create_user, update_user, update_password,\
        login, get_by_id, get_by_username, user_list, delete_user, get_email_address]


class models(Enum):
    users: list = [Users]


class schemas(Enum):
    users: list = [LoginBase, UpdatePassword, PasswordChangeRequest, UserBase,\
        UserCreate, UserUpdate, User]


class scopes(Enum):
    super_admin: list = [
        *[r.name for r in users_routes]
    ]

    admin: list = [
        users_routes.users_create.name,
        users_routes.users_update.name,
        users_routes.users_read_all.name,
        users_routes.users_read_me.name,
        users_routes.users_delete.name,
        users_routes.users_change_password.name
    ]

    monitor: list = [
        users_routes.users_read_me.name,
        users_routes.users_change_password.name
    ]

    visitor: list = [
        users_routes.users_login.name
    ]
