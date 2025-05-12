from typing import Annotated

from fastapi import APIRouter, Path, Query

from ..database.models.vacation_request_model import VacationRequestPublic, VacationRequestCreate, \
    EmployeeAvailableDaysPublic, VacationRequestStatus
from ..dependencies.deps import FilterParamsDep, Response
from ..dependencies.query_params import VacationRequestListParams
from ..security.security import CurrentUser, ManagerUser
from ..services.vacation_service import VacationServiceDep

router = APIRouter(
    prefix="/vacation",
    tags=["vacation"],
    responses={404: {"description": "Vacation request not found"}},
)



@router.get("/")
async def get_user_vacation_requests(
    get_user_vacations_query: Annotated[VacationRequestListParams, Query()],
    user: CurrentUser,
    vacation_service: VacationServiceDep
) -> list[VacationRequestPublic]:
    return vacation_service.get_user_vacation_requests(user, get_user_vacations_query)

@router.get("/subordinates")
async def get_subordinates_vacation_requests(
    filter_query: FilterParamsDep,
    user: ManagerUser,
    vacation_service: VacationServiceDep
) -> list[VacationRequestPublic]:
    return vacation_service.get_subordinates_requests(user, **filter_query.model_dump())



@router.get("/available", response_model=list[EmployeeAvailableDaysPublic])
async def get_user_all_available_days(
    filter_query: FilterParamsDep,
    user: CurrentUser,
    vacation_service: VacationServiceDep
) -> list[EmployeeAvailableDaysPublic]:
    return vacation_service.get_user_all_available_days(user, **filter_query.model_dump())


@router.get("/available/{vacation_type}", response_model=EmployeeAvailableDaysPublic)
async def get_user_available_days(
    vacation_type: Annotated[int, Path(title="Type of vacation", ge=1)],
    user: CurrentUser,
    vacation_service: VacationServiceDep
) -> EmployeeAvailableDaysPublic:
    return vacation_service.get_user_available_days(user, vacation_type).get_model()


@router.post("/add", response_model=VacationRequestPublic)
async def add_vacation_request(
        vacation_request: VacationRequestCreate,
        user: CurrentUser,
        vacation_service: VacationServiceDep
) -> VacationRequestPublic:
    return vacation_service.add_new_vacation_request(user, vacation_request).get_model()

@router.post("{vacation_request_id}/status")
async def change_vacation_request_status(
        vacation_request_id: Annotated[int, Path(title="Vacation Request ID", ge=1)],
        status: VacationRequestStatus,
        user: ManagerUser,
        vacation_service: VacationServiceDep
) -> VacationRequestPublic:
    return vacation_service.change_vacation_request_status(user, vacation_request_id, status).get_model()