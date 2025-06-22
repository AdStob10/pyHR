from sqlalchemy import func
from sqlalchemy.orm import aliased, joinedload
from sqlmodel import select

from .base_repository import BaseRepository
from ..model_utils import PaginatedList
from ..models.employee_model import Employee, EmployeePublic, EmployeePublicWithManager
from ..models.vacation_request_model import EmployeeVacationTypeAvailableDays
from ..utils import apply_filters_and_sort
from ...dependencies.query_params import SubordinatesListParams

Manager = aliased(Employee)


class UserRepository(BaseRepository):

    def get_user_by_username(self, username: str) -> Employee | None:
        stmt = select(Employee).where(Employee.username == username)
        user = self.session.exec(stmt).first()
        return user

    def get_user_all_subordinates(self, manager_id: int, filter_params: SubordinatesListParams) -> PaginatedList[
        EmployeePublic]:
        stmt = select(Employee)
        filtered_and_sorted_stmt = (apply_filters_and_sort(stmt, filter_params, "id")
                                    .where(Employee.manager_id == manager_id))
        cnt_stmt = select(func.count()).select_from(filtered_and_sorted_stmt)
        row_count = self.session.exec(cnt_stmt).first()

        stmt = (filtered_and_sorted_stmt
                .offset(filter_params.offset)
                .limit(filter_params.limit))
        data = self.session.exec(stmt).all()
        return PaginatedList[EmployeePublic](data=data, row_count=row_count)

    def get_user_manager(self, user_id: int) -> EmployeePublic:
        stmt = (select(Manager).join(Manager, Employee.manager).where(Employee.id == user_id))
        manager = self.session.exec(stmt).first()
        return manager

    def get_user_details(self, user_id: int) -> EmployeePublicWithManager:
        stmt = (select(Employee)
                .where(Employee.id == user_id)
                .options(joinedload(Employee.manager, innerjoin=True))
                )
        employee = self.session.exec(stmt).first()
        return employee

    def get_user_subordinate_details(self, manager_id: int, employee_id: int) -> EmployeePublicWithManager:
        stmt = (select(Employee)
                .where(Employee.id == employee_id)
                .where(Employee.manager_id == manager_id)
                .options(joinedload(Employee.manager, innerjoin=True))
                )
        employee = self.session.exec(stmt).first()
        return employee

    def create_new_user(self, new_user: Employee, available_days: list[EmployeeVacationTypeAvailableDays]):
        self.session.add_all([new_user, *available_days])
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
