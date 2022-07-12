from typing import Union
from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import JWTError, jwt

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from odoo_fastapi.src.user_management.schemas import User, UserInDB, TokenData
from odoo_fastapi.project.dependency import odoo_env

from odoo.api import Environment
from odoo.exceptions import AccessDenied


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user_management/token")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b8lalit"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "lalitvasoya": {
        "username": "lalitvasoya",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$7q/cLclsSO9Pb8xOILrWO.N7tefUxn2lazC8EAozdj3neLXCLIA5.",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(env: Environment, email: str):
    # breakpoint()
    user = env['res.users'].search([('login', '=', email)])
    if user:
        return UserInDB(**user.read()[0])


def authenticate_user(env: Environment, email: str, password: str):
    user_cls = env["res.users"]
    db = env.registry.db_name
    try:
        uid = user_cls.authenticate(db=db, login=email, password=password, user_agent_env={})
        user = user_cls.browse(uid)
        env.user = user
        return UserInDB(**user.read()[0])
    except AccessDenied as ad:
        print({"access_denied": ad.args[0]})
        return False


def get_current_user(env: Environment = Depends(odoo_env), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user(env, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
