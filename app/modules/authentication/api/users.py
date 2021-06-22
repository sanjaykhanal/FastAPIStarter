from enum import Enum
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import engine, get_db, Base
from middlewares.authentication.auth import TokenData, decode_token, authorization

import logging

from .. import schema
from .. import crud



Base.metadata.create_all(bind=engine)

ROUTE_PREFIX = '/users'

router = APIRouter(
    prefix=ROUTE_PREFIX
)


incorrect_old_password_exception = HTTPException(
        status_code=400,
        detail="Old password did not match",
        headers={"WWW-Authenticate": "Bearer"},
    )

login_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

user_registration_error = HTTPException(
        status_code = 400,
        detail="User registation failed"
    )


@router.post("/", response_model=schema.users.UsersSuccessResponse)
async def create_user(user: schema.users.UserCreate, db: Session = Depends(get_db), tokenData = Depends(authorization)):
    email_address = user.email
    is_already_email = crud.users.get_email_address(
        db=db, email_address=email_address)
    if is_already_email:
        raise HTTPException(
            status_code=400,
            detail="email already exists")
    output = crud.users.create_user(db=db, user=user)

    if not output:
        raise user_registration_error

    return {"data": output}


@router.put("/{user_id}", response_model=schema.users.UsersSuccessResponse)
async def update_user(user: schema.users.UserUpdate, user_id: int, db: Session = Depends(get_db), tokenData = Depends(authorization)):
    obj = crud.users.update_user(db=db, id=user_id, user=user)

    return {"data": obj}


@router.get("/", response_model=schema.users.UsersListSuccessResponse)
async def get_user_list(request: Request, db: Session = Depends(get_db), tokenData = Depends(authorization)):
    logging.info("\nThis is request:\n")
    logging.info(request.path_params)
    obj = crud.users.user_list(db=db)

    return {"data": obj}


@router.post("/login", response_model=schema.users.LoginResponse)
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    obj = crud.users.login(db=db, user=user)

    if not obj:
        raise login_error

    return {"access_token": obj}


@router.delete("/",response_model= schema.users.UserDeleteSuccessResponse)
async def delete_user(delete_id:int,db:Session=Depends(get_db), tokenData = Depends(authorization)):
    obj = crud.users.delete_user(db=db,id=delete_id)

    return {"data": obj}


@router.get("/me", response_model=schema.users.UsersSuccessResponse)
async def get_me(token:TokenData = Depends(decode_token), db:Session = Depends(get_db), tokenData = Depends(authorization)):
    obj = crud.users.get_by_username(db=db,username=token.sub)

    return {"data": obj}


@router.post("/change-password", response_model=schema.users.UsersSuccessResponse)
async def get_me(passwords:schema.users.PasswordChangeRequest, token:TokenData = Depends(decode_token), db:Session = Depends(get_db), tokenData = Depends(authorization)):
    pass_obj = schema.users.UpdatePassword(username=token.sub, old_password=passwords.old_password, new_password=passwords.new_password)

    updated = crud.users.update_password(db, pass_obj)
    if not updated:
        raise incorrect_old_password_exception

    return {"data": updated}


@router.get("/{user_id}", response_model=schema.users.UsersSuccessResponse)
async def get_by_id(user_id: int,db: Session = Depends(get_db), tokenData = Depends(authorization)):
    obj = crud.users.get_by_id(db=db,id=user_id)

    return {"data": obj}


class routes(Enum):
    users_create: dict = {
        "url": ROUTE_PREFIX + "/",
        "method": "POST"
    }

    users_update: dict = {
        "url": ROUTE_PREFIX + "/",
        "method": "PUT"
    }

    users_read_all: dict = {
        "url": ROUTE_PREFIX + "/",
        "method": "GET"
    }

    users_read_id: dict = {
        "url": ROUTE_PREFIX + "/:id",
        "method": "GET"
    }

    users_read_me: dict = {
        "url": ROUTE_PREFIX + "/me",
        "method": "GET"
    }

    users_delete: dict = {
        "url": ROUTE_PREFIX + "/",
        "method": "DELETE"
    }

    users_login: dict = {
        "url": ROUTE_PREFIX + "/login",
        "method": "POST"
    }

    users_change_password: dict = {
        "url": ROUTE_PREFIX + "/change-password",
        "method": "POST"
    }
