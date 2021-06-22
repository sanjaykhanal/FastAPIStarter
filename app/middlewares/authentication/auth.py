import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from flags import get_flags


flags = get_flags()



SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class Oauth(OAuth2PasswordBearer):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
        ):
        OAuth2PasswordBearer.__init__(self, tokenUrl, scheme_name, scopes, auto_error)


    async def __call__(self, request: Request) -> Optional[str]:

        if not flags.enable_authentication:
            return "dummy token"

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = Oauth(tokenUrl="users/login")



credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

not_authorized_error = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="User is not authorized to access the resource",
        headers={"WWW-Authenticate": "Bearer"},
    )


def __get_token_payload():
    return {
        "sub": None,
        "iat": datetime.utcnow(),
        "scope": "visitor",
        "exp": datetime.utcnow() + timedelta(minutes=1440)
    }


class TokenData(BaseModel):
    sub: str
    scope: str
    exp: datetime
    extra_data: Optional[dict] = {}


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        return False


def create_access_token(sub: Optional[int]=None, scope:str="visitor", expires_delta: Optional[timedelta] = None, extra_data: dict = {}):
    to_encode = __get_token_payload()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})
    to_encode.update({"sub": sub})
    to_encode.update({"scope": scope})
    to_encode.update(extra_data)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str = Depends(oauth2_scheme)):

    if not flags.enable_authentication:
        return TokenData(sub="sub", scope="scope", exp=datetime.utcnow(), extra_data={})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    sub = payload.get('sub')
    if sub is None:
        raise credentials_exception

    scope = payload.get('scope')
    if scope is None:
        raise credentials_exception

    exp = payload.get('exp')
    if exp is None:
        raise credentials_exception

    if exp < datetime.utcnow().replace(tzinfo=timezone.utc).timestamp():
        pass

    extra_data = payload.get('extra_data')
    if extra_data is None:
        extra_data = {}

    token_data = TokenData(sub=sub, scope=scope, exp=exp, extra_data=extra_data)

    return token_data


async def validate_token(token_data: TokenData = Depends(decode_token)):
    return token_data


def __load_scopes():
    with open(os.path.join(os.path.dirname(__file__), 'scopes.json')) as f:
        scopes = json.load(f)

    with open(os.path.join(os.path.dirname(__file__), 'routes.json')) as f:
        routes = json.load(f)

    route_scopes = {}
    for key, values in scopes.items():
        route_scopes[key] = []
        for value in values:
            route_scopes[key].append([routes[value]["url"], routes[value]["method"]])

    with open(os.path.join(os.path.dirname(__file__), 'route_scopes.json'), 'w+') as f:
        json.dump(route_scopes, f)

    return route_scopes



def authorization(request: Request, token_data: Optional[TokenData] = Depends(decode_token)):

    if not flags.enable_authentication:
        return token_data

    route_scopes = __load_scopes()

    path_params = request.path_params
    method = request.method.upper()
    url = request.url.path

    for _,value in path_params.items():
        url = url.replace(value, ":id")

    scope = token_data.scope

    if [url, method] in route_scopes[scope]:
        return token_data

    raise not_authorized_error

