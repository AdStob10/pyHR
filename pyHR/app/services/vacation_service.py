from datetime import date
from typing import Annotated

from fastapi import Depends
from loguru import logger

from ..database.model_utils import PaginatedList
from ..database.models.employee_model import User
from ..database.models.subordinate_request_model import SubordinateRequestPublic
from ..database.models.vacation_request_model import VacationRequestPublic, VacationRequestCreate, VacationRequest, \
    EmployeeAvailableDaysPublic, EmployeeVacationTypeAvailableDays, VacationRequestStatus
from ..database.repositories.user_repository import UserRepository
from ..database.repositories.vacation_repository import VacationRepository
from ..dependencies.deps import Response, NotFound, BadRequest
from ..dependencies.query_params import VacationRequestListParams, SubordinateRequestListParams
from ..i18n import _


class VacationService:
    def __init__(
            self,
            vacation_repository: Annotated[VacationRepository, Depends(VacationRepository)],
            user_repository: Annotated[UserRepository, Depends(UserRepository)],
    ):
        self.vacation_repository = vacation_repository
        self.user_repository = user_repository


    def get_user_vacation_requests(self, employee: User, filter_params: VacationRequestListParams) -> PaginatedList[VacationRequestPublic]:
        return self.vacation_repository.get_employee_requests(employee.id, filter_params)

    def get_user_request_by_id(self, employee: User, vacation_id: int) -> Response[VacationRequestPublic]:
        vacation_request = self.vacation_repository.get_employee_request_by_id(employee.id, vacation_id)
        if not vacation_request:
            msg = _("Not found vacation request for employee")
            return NotFound(message=f"{msg} (vacation_id = {vacation_id})")

        return Response(data=vacation_request)

    def get_subordinates_requests(self, manager: User, filter_params: SubordinateRequestListParams) -> PaginatedList[SubordinateRequestPublic]:
        return self.vacation_repository.get_subordinates_requests(manager.id, filter_params)

    def get_subordinate_request_by_id(self, manager: User, vacation_id: int) -> Response[SubordinateRequestPublic]:
        vacation_request = self.vacation_repository.get_subordinate_request_by_id(manager.id, vacation_id)
        if not vacation_request:
            msg = _("Not found subordinate vacation request for employee")
            return NotFound(message=f"{msg} (vacation_id = {vacation_id})")

        return Response(data=vacation_request)

    def get_user_all_available_days(self, employee: User, offset: int, limit: int) -> list[EmployeeAvailableDaysPublic]:
        return self.vacation_repository.get_employee_all_available_days(employee.id, offset, limit)

    def get_user_available_days(self, employee: User, vacation_type_id: int) -> Response[EmployeeVacationTypeAvailableDays]:
        available_days = self.vacation_repository.get_employee_available_days(employee.id, vacation_type_id)
        if not available_days:
            return NotFound(message=_("Not found available days for employee"))

        return Response(data=available_days)



    def get_available_vacation_types(self):
        return self.vacation_repository.get_available_vacation_types()

    @logger.catch(level='ERROR')
    def add_new_vacation_request(self, employee: User, vacation_request: VacationRequestCreate) -> Response[VacationRequest]:
        employee_available_vac = self.vacation_repository.get_employee_available_days(employee.id, vacation_request.vacation_type_id)
        manager = self.user_repository.get_user_manager(employee.id)
        if manager is None:
            logger.warning("Not found manager for user {}", employee)
            return NotFound(message=_("Not found manager for user {}"))

        vacation_request_entity = VacationRequest(**vacation_request.model_dump())
        vacation_request_entity.employee_id = employee.id
        vacation_request_entity.manager_id = manager.id

        if employee_available_vac is None:
            logger.warning("Not found available days for user {}", employee)
            return NotFound(message=_("Not found available days for employee"))


        now = date.today()
        if vacation_request_entity.end_date < now or vacation_request_entity.start_date < now:
            return BadRequest(message=_("Date range is in the past"))

        vacation_range = vacation_request_entity.end_date - vacation_request_entity.start_date
        vacation_duration = vacation_range.days

        # if start date is equal to end date then we have one day vacation
        if vacation_duration == 0:
            vacation_duration = 1
        # otherwise we have to add one day (count start date as first day of vacation)
        else:
            vacation_duration += 1

        if vacation_duration < 0:
            return BadRequest(message=_("Invalid date range"))

        if employee_available_vac.available_days < vacation_duration:
            msg = _("Available days limit exceeded. Available days:")
            return BadRequest(message=f"{msg} {employee_available_vac.available_days}")

        if self.vacation_repository.any_vacation_between_start_end_date(
                employee.id,
                vacation_request_entity.start_date,
                vacation_request_entity.end_date
        ):
            return BadRequest(message=_("You already have vacation in selected period"))


        logger.info("Add new vacation request {}", vacation_request_entity)
        employee_available_vac.available_days -= vacation_duration
        vacation_request_entity = self.vacation_repository.save_vacation_request_and_avail_days(vacation_request_entity, employee_available_vac)

        return Response(data=vacation_request_entity)

    @logger.catch(level='ERROR')
    def change_vacation_request_status(self, manager: User, vacation_request_id: int, vacation_request_status: VacationRequestStatus) -> Response[VacationRequest]:
        request: VacationRequest = self.vacation_repository.get_vacation_request_by_id(vacation_request_id)

        logger.info("Manager = {} change request (id: {}) status from {} to {}", manager, vacation_request_id, request.status, vacation_request_status)

        if request is None or request.manager_id != manager.id:
            return NotFound(message=_("Not found vacation request"))

        if request.status == vacation_request_status:
            msg = _("Vacation request already has status")
            return BadRequest(message=f"{msg} {request.status.name}")

        match vacation_request_status:
            case VacationRequestStatus.NEW | VacationRequestStatus.ACCEPTED:
                if request.status == VacationRequestStatus.REJECTED:
                    return BadRequest(message=_("Vacation request is rejected. You cannot change it status"))
                request.status = vacation_request_status
                request = self.vacation_repository.save_model(request)
                return Response(data=request)
            case VacationRequestStatus.REJECTED:
                employee_available_days = self.vacation_repository.get_employee_available_days(request.employee_id, request.vacation_type_id)
                vacation_range = request.end_date - request.start_date
                employee_available_days.available_days += vacation_range.days
                request.status = VacationRequestStatus.REJECTED
                request = self.vacation_repository.save_vacation_request_and_avail_days(request, employee_available_days)
                return Response(data=request)




VacationServiceDep = Annotated[VacationService, Depends(VacationService)]