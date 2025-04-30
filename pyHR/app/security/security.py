import os
from datetime import datetime, timezone
from datetime import timedelta
from typing import Annotated, Any

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError, BaseModel
from starlette import status

from loguru import logger

from app.database.models.employee_model import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')
TokenDep = Annotated[str, Depends(oauth2_scheme)]

load_dotenv("./.env")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))


class TokenData(BaseModel):
    """Access Token Model"""
    sub: str

class Token(BaseModel):
    access_token: str
    token_type: str





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate(
        username: str,
        password: str,
        user_service: Annotated[UserService, Depends(UserService)]
) -> User | None:
    """Authenticate User - Verifies User Credentials"""
    user = user_service.get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    logger.info("Successfully authenticated user {}", user.username)
    return user


def create_access_token(sub: str | Any, expire_time: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Creates access token for user"""
    expire_in = datetime.now(timezone.utc) + expire_time
    to_encode = {"sub": str(sub), "exp": expire_in}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_current_user(
        token: TokenDep,
        user_service: Annotated[UserService, Depends(UserService)]
) -> User:
    """Gets current user based on token data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except (InvalidTokenError, ValidationError):
        logger.exception("USER TOKEN ERROR")
        raise credentials_exception

    user = user_service.get_user_by_username(token_data.sub)
    if not user:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)

