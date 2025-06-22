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
from loguru import logger
from pydantic import ValidationError, BaseModel
from starlette import status

from app.database.models.employee_model import User, EmployeeRole
from app.services.user_service import UserService, verify_password

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


def authenticate(
        username: str,
        password: str,
        user_service: Annotated[UserService, Depends(UserService)]
) -> User | None:
    """
    Verifies user credentials
    :param username: username
    :param password: user password
    :param user_service: user service dependency
    :return: authenticated user
    """
    user = user_service.get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    logger.info("Successfully authenticated user {}", user)
    return user


def create_access_token(sub: str | Any, expire_time: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Creates a JWT access token
    :param sub: title
    :param expire_time: expire time
    :return: token as `string`
    """
    expire_in = datetime.now(timezone.utc) + expire_time
    to_encode = {"sub": str(sub), "exp": expire_in}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_current_user(
        token: TokenDep,
        user_service: Annotated[UserService, Depends(UserService)]
) -> User:
    """
    Get user by access token
    :param token:
    :param user_service:
    :return: authenticated user
    """
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


class CurrentUserByRole:
    """
        Class dependency for checking if user has required role
    """

    def __init__(self, role: EmployeeRole):
        self.role = role

    def __call__(self, user: CurrentUser):
        """
        Check if user has required role
        Otherwise raise exception
        :param user:
        :return: authenticated user with required role
        """
        if user.role is None or user.role != self.role:
            role_exception = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action is only available for {self.role.name} role",
            )
            logger.warning("User = {} tried illegal action", user)
            raise role_exception
        return user


manage_role_checker = CurrentUserByRole(EmployeeRole.MANAGER)
ManagerUser = Annotated[User, Depends(manage_role_checker)]
