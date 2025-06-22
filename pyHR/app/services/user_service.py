from typing import Annotated

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext

from app.database.model_utils import PaginatedList
from app.database.models.employee_model import User, EmployeePublic, EmployeePublicWithManager, EmployeeRole, \
    EmployeeCreate, Employee
from app.database.models.vacation_request_model import EmployeeVacationTypeAvailableDays
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.vacation_repository import VacationRepository
from app.dependencies.deps import NotFound, Response, BadRequest
from app.dependencies.query_params import SubordinatesListParams
from app.i18n import _

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)],
                 vacation_repository: Annotated[VacationRepository, Depends(VacationRepository)]):
        self.user_repository = user_repository
        self.vacation_repository = vacation_repository

    def get_user_by_username(self, username: str) -> User | None:
        user = self.user_repository.get_user_by_username(username)
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

    def get_user_all_subordinates(self, user: User, filter_params: SubordinatesListParams) -> PaginatedList[
        EmployeePublic]:
        return self.user_repository.get_user_all_subordinates(user.id, filter_params)

    def get_user_manager(self, user: User) -> Response[EmployeePublic]:
        manager = self.user_repository.get_user_manager(user.id)
        if not manager:
            logger.info("manager is none = {}", manager)
            return Response(message=_("Manager not found"), status_code=404)

        return Response(data=manager)

    def create_new_user(self, user: User, new_user_model: EmployeeCreate) -> Response[EmployeePublic]:
        existing_user = self.user_repository.get_user_by_username(new_user_model.username)
        if existing_user is not None:
            _msg = _("User with provided name already exists, username=")
            return BadRequest(message=f"{_msg} {existing_user.username}")
        hashed_password = get_password_hash(new_user_model.password)
        new_user = Employee(**new_user_model.model_dump())
        new_user.password = hashed_password
        new_user.manager_id = user.id
        new_user.role = EmployeeRole.BASIC_EMPLOYEE
        new_user = self.user_repository.create_new_user(new_user, self._get_new_user_default_vacations(new_user))
        return Response(data=new_user)

    def _get_new_user_default_vacations(self, employee: Employee) -> list[EmployeeVacationTypeAvailableDays]:
        """
        Get new user default vacation type available days
        :param employee:
        :return: list of default available days in different vacation types
        """
        user_vacations = []
        vacation_types = self.vacation_repository.get_vacation_types_with_default_available_days()
        for vacation_type in vacation_types:
            user_vac = EmployeeVacationTypeAvailableDays()
            user_vac.employee = employee
            user_vac.vacation_type_id = vacation_type.id
            user_vac.available_days = vacation_type.default_available_days
            user_vacations.append(user_vac)
        return user_vacations


UserServiceDep = Annotated[UserService, Depends(UserService)]
