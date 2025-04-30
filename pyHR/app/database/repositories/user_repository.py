from sqlalchemy.sql.annotation import Annotated
from sqlmodel import select
from loguru import logger

from app.database.db import SessionDep
from app.database.models.employee_model import User, Employee


class UserRepository:
    def __init__(self, session : SessionDep):
        self.session = session

    def get_user_by_username(self, username: str) -> Employee | None:
        stmt = select(Employee).where(Employee.username == username)
        user = self.session.exec(stmt).first()
        return user