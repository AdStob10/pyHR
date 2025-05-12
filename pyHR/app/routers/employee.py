from typing import Annotated
from fastapi import APIRouter, Query
from loguru import logger

from app.database.db import SessionDep
from app.database.models.employee_model import Employee, EmployeePublic
from app.dependencies.deps import BaseListParams, FilterParamsDep, Response
from app.security.security import TokenDep, CurrentUserByRole, CurrentUser, ManagerUser
from app.services.user_service import UserService, UserServiceDep

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    responses={404: {"description": "Employee not found"}},
)



@router.get("/manager")
def get_user_manager(
        user: CurrentUser,
        user_service: UserServiceDep
) -> EmployeePublic:
    return user_service.get_user_manager(user).get_model()

@router.get("/all")
def get_employees(
        filer_query: FilterParamsDep,
        user_service: UserServiceDep,
        user: ManagerUser,
) -> list[EmployeePublic]:
    return user_service.get_user_all_subordinates(user, **filer_query.model_dump())