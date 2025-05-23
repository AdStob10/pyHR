from datetime import date

from sqlalchemy.orm import joinedload
from sqlmodel import select, or_, and_, func

from .base_repository import BaseRepository
from ..db import SessionDep
from ..filter_utils import FilterTransfomer
from ..model_utils import PaginatedList
from ..models.employee_model import Employee
from ..models.subordinate_request_model import SubordinateRequestPublic
from ..models.vacation_request_model import VacationRequest, VacationRequestPublic, EmployeeVacationTypeAvailableDays, \
    EmployeeAvailableDaysPublic, VacationRequestStatus, VacationType
from ..utils import apply_filters_and_sort
from ...dependencies.query_params import VacationRequestListParams, SubordinateRequestListParams


class VacationRepository(BaseRepository):

    def get_employee_requests(self, employee_id: int, filter_params: VacationRequestListParams) -> PaginatedList[VacationRequestPublic]:
        stmt = select(VacationRequest)
        filtered_and_sorted_stmt = (apply_filters_and_sort(stmt, filter_params, "id")
                                    .where(VacationRequest.employee_id == employee_id))

        cnt_stmt = select(func.count()).select_from(filtered_and_sorted_stmt)
        row_count = self.session.exec(cnt_stmt).first()

        stmt = (filtered_and_sorted_stmt
                .offset(filter_params.offset)
                .limit(filter_params.limit).options(joinedload(VacationRequest.vacation_type, innerjoin=True)))

        data = self.session.exec(stmt).all()

        return PaginatedList[VacationRequestPublic](data=data, row_count=row_count)

    def get_employee_request_by_id(self, employee_id: int, vacation_id: int) -> VacationRequestPublic:
        stmt = (select(VacationRequest)
                .where(VacationRequest.employee_id == employee_id)
                .where(VacationRequest.id == vacation_id)
                .options(joinedload(VacationRequest.vacation_type, innerjoin=True),
                         joinedload(VacationRequest.employee, innerjoin=True))
                )

        return self.session.exec(stmt).first()

    def get_subordinates_requests(self, manager_id: int, filter_params: SubordinateRequestListParams) -> PaginatedList[SubordinateRequestPublic]:
        stmt = (select(VacationRequest)
                .join(VacationRequest.employee)
                .add_columns(Employee)
                .options(joinedload(VacationRequest.vacation_type, innerjoin=True),
                                      joinedload(VacationRequest.employee, innerjoin=True)))
        filtered_and_sorted_stmt = (apply_filters_and_sort(stmt, filter_params, "id")
                                    .where(VacationRequest.manager_id == manager_id))

        cnt_stmt = select(func.count()).select_from(filtered_and_sorted_stmt)
        row_count = self.session.exec(cnt_stmt).first()

        stmt = (filtered_and_sorted_stmt
                .offset(filter_params.offset)
                .limit(filter_params.limit))

        data = self.session.exec(stmt).all()
        return PaginatedList[SubordinateRequestPublic](data=data, row_count=row_count)

    def get_subordinate_request_by_id(self, manager_id: int, vacation_id: int) -> SubordinateRequestPublic:
        stmt = (select(VacationRequest)
                .where(VacationRequest.manager_id == manager_id)
                .where(VacationRequest.id == vacation_id)
                .options(joinedload(VacationRequest.vacation_type, innerjoin=True),
                         joinedload(VacationRequest.employee, innerjoin=True)))


        return self.session.exec(stmt).first()


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
        return self.session.get(VacationRequest, vacation_id)

    def get_available_vacation_types(self):
        stmt = select(VacationType)
        return self.session.exec(stmt).all()

    def save_vacation_request_and_avail_days(self, request: VacationRequest, available_days: EmployeeVacationTypeAvailableDays) -> VacationRequest:
        self.session.add(request)
        self.session.add(available_days)
        self.session.commit()
        self.session.refresh(request)
        return request

    def any_vacation_between_start_end_date(self, employee_id: int, start_date: date, end_date: date):
        stmt = (select(func.count())
                .select_from(VacationRequest)
                .where(and_(VacationRequest.employee_id == employee_id, VacationRequest.status != VacationRequestStatus.REJECTED)
                       , or_(and_(VacationRequest.start_date <= start_date, VacationRequest.end_date >= start_date)
                       , and_(VacationRequest.start_date <= end_date, VacationRequest.end_date >= end_date))
                ))
        return True if self.session.exec(stmt).first() > 0 else False