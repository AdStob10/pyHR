from datetime import date
from typing import Annotated

from fastapi import Depends
from loguru import logger

from app.database.models.employee_model import User
from app.database.models.vacation_request_model import VacationRequestPublic, VacationRequestCreate, VacationRequest, \
    EmployeeAvailableDaysPublic, EmployeeVacationTypeAvailableDays
from app.database.repositories.vacation_repository import VacationRepository
from app.dependencies.deps import Response, NotFound, BadRequest
from app.i18n import _


class VacationService:
    def __init__(
            self,
            vacation_repository: Annotated[VacationRepository, Depends(VacationRepository)]
    ):
        self.vacation_repository = vacation_repository

    def get_user_vacation_requests(self, employee: User, offset: int, limit: int) -> list[VacationRequestPublic]:
        return self.vacation_repository.get_employee_requests(employee.id, offset, limit)

    def get_user_all_available_days(self, employee: User, offset: int, limit: int) -> list[EmployeeAvailableDaysPublic]:
        return self.vacation_repository.get_employee_all_available_days(employee.id, offset, limit)

    def get_user_available_days(self, employee: User, vacation_type_id: int) -> Response[EmployeeVacationTypeAvailableDays]:
        available_days = self.vacation_repository.get_employee_available_days(employee.id, vacation_type_id)
        if not available_days:
            return NotFound(message=_("Not found available days for employee"))

        return Response(available_days)

    @logger.catch(level='ERROR')
    def add_new_vacation_request(self, employee: User, vacation_request: VacationRequestCreate) -> Response[VacationRequest]:
        try:
            employee_available_vac = self.vacation_repository.get_employee_available_days(employee.id, vacation_request.vacation_type_id)
            vacation_request_entity = VacationRequest(**vacation_request.model_dump())
            vacation_request_entity.employee_id = employee.id

            if employee_available_vac is None:
                logger.warning("Not found available days for user {}", employee)
                return NotFound(message=_("Not found available days for employee"))


            now = date.today()
            if vacation_request_entity.end_date < now or vacation_request_entity.start_date < now:
                return BadRequest(message=_("Date range is in the past"))

            vacation_range = vacation_request_entity.end_date - vacation_request_entity.start_date
            if vacation_range.days <= 0:
                return BadRequest(message=_("Invalid date range"))

            if employee_available_vac.available_days < vacation_range.days:
                msg = _("Available days limit exceeded. Available days:")
                return BadRequest(message=f"{msg} {employee_available_vac.available_days}")

            if self.vacation_repository.any_vacation_between_start_end_date(
                    employee.id,
                    vacation_request_entity.start_date,
                    vacation_request_entity.end_date
            ):
                return BadRequest(message=_("You already have vacation in selected period"))


            logger.info("Add new vacation request {}", vacation_request_entity)
            employee_available_vac.available_days -= vacation_range.days
            vacation_request_entity = self.vacation_repository.add_vacation_request(vacation_request_entity, employee_available_vac)

            return Response(vacation_request_entity)
        except Exception as e:
            logger.exception("Add new request error",e)
            raise e





VacationServiceDep = Annotated[VacationService, Depends(VacationService)]