from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ..database.models.employee_model import UserPublic
from ..security.security import create_access_token, CurrentUser, authenticate, Token
from ..services.user_service import UserService

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Employee not found"}},
)


@router.post("/access-token")
async def access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: Annotated[UserService, Depends()]
) -> Token:
    user = authenticate(form_data.username, form_data.password, user_service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.username)
    return Token(access_token=token, token_type="bearer")


@router.get("/info", response_model=UserPublic)
async def info(current_user: CurrentUser) -> UserPublic:
    return current_user
