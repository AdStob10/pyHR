from sqlalchemy.orm import aliased
from sqlmodel import select

from .base_repository import BaseRepository
from ..db import SessionDep
from ..models.employee_model import Employee, EmployeePublic

Manager = aliased(Employee)

class UserRepository(BaseRepository):

    def get_user_by_username(self, username: str) -> Employee | None:
        stmt = select(Employee).where(Employee.username == username)
        user = self.session.exec(stmt).first()
        return user

    def get_user_all_subordinates(self, manager_id: int, offset: int, limit: int) -> list[EmployeePublic]:
        stmt = select(Employee).where(Employee.manager_id == manager_id).offset(offset).limit(limit)
        employees = self.session.exec(stmt).all()
        return employees

    def get_user_manager(self, user_id: int) -> EmployeePublic:
        stmt = (select(Manager).join(Manager, Employee.manager).where(Employee.id == user_id))
        manager = self.session.exec(stmt).first()
        return manager
