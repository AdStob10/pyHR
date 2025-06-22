import enum
from datetime import date
from typing import Optional, TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, Integer, VARCHAR, Computed
from sqlmodel import Field, SQLModel, Relationship

from app.database.model_utils import CamelSQLModel
from app.database.models.vacation_request_model import EmployeeVacationTypeAvailableDays

if TYPE_CHECKING:
    from vacation_request_model import VacationRequest


class EmployeeRole(enum.Enum):
    BASIC_EMPLOYEE = 0
    MANAGER = 1
    ADMIN = 2


class User(SQLModel):
    id: int = Field(primary_key=True)
    username: str = Field(index=True, max_length=100)
    password: str = Field(max_length=300)
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    full_name: str = Field(sa_column=Column(VARCHAR, Computed("first_name || ' ' || last_name")))
    role: EmployeeRole = Field(nullable=True, default=0)
    email: Optional[str] = Field(max_length=150)

    def __repr__(self):
        return f"<User id:{self.id}, username:{self.username}>"

    def __str__(self):
        return f"<User id:{self.id}, username:{self.username}, role:{self.role}>"


class UserPublic(CamelSQLModel):
    id: int
    username: str
    first_name: str
    last_name: str
    full_name: str
    role: EmployeeRole
    email: Optional[str]


class Employee(User, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True))
    employment_date: date
    job_title: str = Field(max_length=150, nullable=True)
    department: str = Field(max_length=150, nullable=True)

    manager_id: int = Field(foreign_key='employee.id', nullable=True)
    manager: "Employee" = Relationship(back_populates="employees",
                                       sa_relationship_kwargs={"remote_side": lambda: Employee.id})

    vacation_type_available_days: list["EmployeeVacationTypeAvailableDays"] = Relationship(back_populates="employee")
    vacation_requests: list["VacationRequest"] = Relationship(back_populates="employee", cascade_delete=True,
                                                              sa_relationship_kwargs={
                                                                  "foreign_keys": "VacationRequest.employee_id"})

    employees: list["Employee"] = Relationship(back_populates="manager")
    employees_requests: list["VacationRequest"] = Relationship(back_populates="manager", sa_relationship_kwargs={
        "foreign_keys": "VacationRequest.manager_id"})


class EmployeePublic(UserPublic):
    employment_date: date | None
    job_title: str | None
    department: str | None


class EmployeePublicWithManager(EmployeePublic):
    manager: EmployeePublic


class EmployeeCreate(CamelSQLModel):
    username: str = Field(index=True, min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=150, regex= r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]).{8,}$')
    first_name: str = Field(min_length=2, max_length=150)
    last_name: str = Field(min_length=2, max_length=150)
    email: EmailStr | None = Field(max_length=150, nullable=True, default=None)
    employment_date: date | None = None
    job_title: str | None = Field(max_length=150, nullable=True, default=None)
    department: str | None = Field(max_length=150, nullable=True, default=None)
