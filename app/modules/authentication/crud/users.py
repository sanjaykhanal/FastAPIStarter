from pydantic.networks import EmailStr
from typing import List
from sqlalchemy.orm import Session
from ..schema import users as schema
from ..models import users as models
from middlewares.authentication.auth import get_password_hash, verify_password, create_access_token



def username_exists(db: Session, username: str) :
    return db.query(models.Users).filter(models.Users.username == username).first()


def create_user(db: Session, user: schema.UserCreate):
    try:
        user_data = models.Users(**user.dict())
        user_data.password = get_password_hash(user_data.password)
        output = db.add(user_data)
        print("output",output)
        db.commit()
        db.refresh(user_data)
        print("user data: ", user_data)
        return user_data
    except Exception as e:
        print(e)
        return False


def update_user(db: Session, id: int, user: schema.UserUpdate):
    obj = db.query(models.Users).filter(models.Users.id == id).first()
    set_values = user.dict(exclude_unset=True)

    for key,value in set_values.items():
        setattr(obj, key, value)

    db.commit()
    return obj


def update_password(db: Session, password: schema.UpdatePassword):
    obj = db.query(models.Users).filter(
        models.Users.username == password.username).first()

    old_password = obj.password

    if not verify_password(password.old_password, old_password):
        return False

    password = get_password_hash(password.new_password)
    db.commit()
    return obj


def login(db: Session, user: schema.LoginBase):
    obj = db.query(models.Users).filter(
        models.Users.username == user.username).first()
    password = obj.password
    print("\nThis is password: {}\n".format(password))

    if not verify_password(user.password, password):
        return False

    token = create_access_token(obj.username, obj.role)
    return token


def get_by_id(db: Session, id: int):
    obj = db.query(models.Users).filter(models.Users.id == id).first()
    return obj


def get_by_username(db:Session, username:str):
    obj = db.query(models.Users).filter(models.Users.username == username).first()
    return obj


def user_list(db:Session,skip: int = 0, limit: int = 100) -> List[schema.User]:
    obj = db.query(models.Users).offset(skip).limit(limit).all()
    return obj


def delete_user(db:Session,id:int):
    output = db.query(models.Users).filter(models.Users.id == id).delete()
    db.commit()
    return output


def get_email_address(db:Session,email_address: EmailStr):
    output = db.query(models.Users).filter(models.Users.email == email_address).first()
    return output
