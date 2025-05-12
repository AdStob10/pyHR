from datetime import date

from sqlalchemy.orm import joinedload
from sqlmodel import select, or_, and_, func

from .base_repository import BaseRepository
from ..db import SessionDep
from ..filter_utils import FilterTransfomer
from ..models.vacation_request_model import VacationRequest, VacationRequestPublic, EmployeeVacationTypeAvailableDays, \
    EmployeeAvailableDaysPublic, SubordinateRequestPublic, VacationRequestStatus
from ..utils import apply_filters_and_sort
from ...dependencies.query_params import VacationRequestListParams


class VacationRepository(BaseRepository):

    def get_employee_requests(self, employee_id: int, filter_params: VacationRequestListParams) -> list[VacationRequestPublic]:
        stmt = select(VacationRequest)
        filtered_and_sorted_stmt = apply_filters_and_sort(stmt, filter_params)
        stmt = (filtered_and_sorted_stmt
                .where(VacationRequest.employee_id == employee_id)
                .offset(filter_params.offset)
                .limit(filter_params.limit).options(joinedload(VacationRequest.vacation_type, innerjoin=True)))
        return self.session.exec(stmt).all()

    def get_subordinates_requests(self, manager_id: int, offset: int, limit: int) -> list[SubordinateRequestPublic]:
        stmt = (select(VacationRequest)
                .where(VacationRequest.manager_id == manager_id)
                .offset(offset)
                .limit(limit).options(joinedload(VacationRequest.vacation_type, VacationRequest.employee, innerjoin=True)))
        return self.session.exec(stmt).all()

    def get_employee_all_available_days(self, employee_id: int, offset: int, limit: int) -> list[EmployeeAvailableDaysPublic]:
        stmt = (select(EmployeeVacationTypeAvailableDays)
                .where(EmployeeVacationTypeAvailableDays.employee_id == employee_id)
                .offset(offset)
                .limit(limit))
        return self.session.exec(stmt).all()

    def get_employee_available_days(self, employee_id: int, vacation_type: int) -> EmployeeVacationTypeAvailableDays:
        stmt = (select(EmployeeVacationTypeAvailableDays)
                .where(EmployeeVacationTypeAvailableDays.employee_id == employee_id)
                .where(EmployeeVacationTypeAvailableDays.vacation_type_id == vacation_type)
                )
        return self.session.exec(stmt).first()

    def get_vacation_request_by_id(self, vacation_id: int) -> VacationRequest:
        return self.session.get(VacationRequest, id=vacation_id)

    def get_available_vacation_types(self):
        pass

    def save_vacation_request_and_avail_days(self, request: VacationRequest, available_days: EmployeeVacationTypeAvailableDays) -> VacationRequest:
        self.session.add(request)
        self.session.add(available_days)
        self.session.commit()
        self.session.refresh(request)
        return request

    def any_vacation_between_start_end_date(self, employee_id: int, start_date: date, end_date: date):
        stmt = (select(func.count())
                .select_from(VacationRequest)
                .where(and_(VacationRequest.employee_id == employee_id)
                       , or_(and_(VacationRequest.start_date <= start_date, VacationRequest.end_date >= start_date)
                       , and_(VacationRequest.start_date <= end_date, VacationRequest.end_date >= end_date))
                ))
        return True if self.session.exec(stmt).first() > 0 else False