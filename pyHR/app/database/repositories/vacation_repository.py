from datetime import date

from sqlmodel import select, or_, and_, func

from ..db import SessionDep
from ..models.vacation_request_model import VacationRequest, VacationRequestPublic, EmployeeVacationTypeAvailableDays, \
    EmployeeAvailableDaysPublic


class VacationRepository:
    def __init__(self, session: SessionDep):
        self.session: SessionDep  = session

    def get_employee_requests(self, employee_id: int, offset: int, limit: int) -> list[VacationRequestPublic]:
        stmt = (select(VacationRequest)
                .where(VacationRequest.employee_id == employee_id)
                .offset(offset)
                .limit(limit))
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

    def add_vacation_request(self, request: VacationRequest, available_days: EmployeeVacationTypeAvailableDays) -> VacationRequest:
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