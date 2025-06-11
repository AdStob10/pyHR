from typing import Annotated

from fastapi import Depends
from loguru import logger

from app.database.models.employee_model import User, EmployeePublic, EmployeePublicWithManager, EmployeeRole
from app.database.repositories.user_repository import UserRepository
from app.dependencies.deps import NotFound, Response
from app.i18n import _


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository


    def get_user_by_username(self, username: str) -> User | None:
        user =  self.user_repository.get_user_by_username(username)
        return user

    def get_user_details(self, user: User) -> Response[EmployeePublicWithManager]:
        details = self.user_repository.get_user_details(user.id)
        if not details:
            msg = _("User not found")
            return NotFound(message=f"{msg} id:{user.id}")

        return Response(data=details)

    def get_user_subordinate_details(self, user: User, employee_id) -> Response[EmployeePublicWithManager]:
        details = self.user_repository.get_user_subordinate_details(user.id, employee_id)
        if not details:
            msg = _("User not found")
            return NotFound(message=f"{msg} id:{employee_id}")

        return Response(data=details)

    def get_user_all_subordinates(self, user: User, offset: int, limit: int) -> list[EmployeePublic]:
        return self.user_repository.get_user_all_subordinates(user.id, offset, limit)

    def get_user_manager(self, user: User) -> Response[EmployeePublic]:
        manager = self.user_repository.get_user_manager(user.id)
        if not manager:
            logger.info("manager is none = {}", manager)
            return Response(message=_("Manager not found"), status_code=404)

        return Response(data=manager)


UserServiceDep = Annotated[UserService, Depends(UserService)]