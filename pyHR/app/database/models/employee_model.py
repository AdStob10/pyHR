import enum
from datetime import datetime
from typing import Annotated, Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import Column, Integer
from sqlmodel import Field, SQLModel, Relationship

from app.database.models.vacation_request_model import EmployeeVacationTypeAvailableDays

if TYPE_CHECKING:
    from vacation_request_model import VacationRequest


class EmployeeRole(enum.Enum):
    BASIC_EMPLOYEE = 0
    MANAGER = 1
    ADMIN = 2

class User(SQLModel):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field()
    role: EmployeeRole = Field(nullable=True, default=0)
    email: Optional[str] = Field(max_length=150)


    def __repr__(self):
        return f"<User id:{self.id}, username:{self.username}>"

    def __str__(self):
        return f"<User id:{self.id}, username:{self.username}>"


class UserPublic(BaseModel):
    id: int
    username: str
    email: Optional[str]


class Employee(User, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True))
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    employment_date: datetime


    manager_id: int = Field(foreign_key='employee.id', nullable=True)
    manager: "Employee" = Relationship(back_populates="employees", sa_relationship_kwargs={"remote_side": lambda: Employee.id})

    vacation_type_available_days : list["EmployeeVacationTypeAvailableDays"] = Relationship(back_populates="employee")
    vacation_requests: list["VacationRequest"] = Relationship(back_populates="employee", cascade_delete=True, sa_relationship_kwargs={"foreign_keys": "VacationRequest.employee_id"})


    employees: list["Employee"] = Relationship(back_populates="manager")
    employees_requests: list["VacationRequest"] = Relationship(back_populates="manager", sa_relationship_kwargs={"foreign_keys": "VacationRequest.manager_id"})


class EmployeePublic(SQLModel):
    id: int
    first_name: str
    last_name: str
    employment_date: datetime


