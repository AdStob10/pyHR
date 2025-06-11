from logging import Manager
from typing import Annotated

from fastapi import APIRouter, Path

from app.database.models.employee_model import EmployeePublic, EmployeePublicWithManager
from app.dependencies.deps import FilterParamsDep
from app.security.security import CurrentUser, ManagerUser
from app.services.user_service import UserServiceDep

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


@router.get("/details")
def get_user_details(
        user: CurrentUser,
        user_service: UserServiceDep,
) -> EmployeePublicWithManager:
    return user_service.get_user_details(user).get_model()

@router.get("/details/{employee_id}")
def get_user_subordinate_details(
        employee_id: Annotated[int, Path(title="Vacation Request ID", ge=1)],
        user: ManagerUser,
        user_service: UserServiceDep,
) -> EmployeePublicWithManager:
    return user_service.get_user_subordinate_details(user, employee_id).get_model()