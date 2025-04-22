from fastapi import Depends
from typing import Annotated
from loguru import logger

from app.database.models.employee import User, Employee
from app.database.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository


    def get_user_by_username(self, username: str) -> User | None:
        user =  self.user_repository.get_user_by_username(username)
        return user