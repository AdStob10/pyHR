import enum
from datetime import date
from typing import Optional, TYPE_CHECKING


from sqlmodel import SQLModel, Field, Relationship

from ..model_utils import CamelSQLModel

if TYPE_CHECKING:
    from .employee_model import Employee, EmployeePublic


class VacationTypeBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field()

class VacationType(VacationTypeBase, table=True):
    __tablename__ = "vacation_type"

    vacation_requests: list["VacationRequest"] = Relationship(back_populates="vacation_type")
    users_available_days: list["EmployeeVacationTypeAvailableDays"] = Relationship(back_populates="vacation_type")



class EmployeeVacationTypeAvailableDaysBase(CamelSQLModel):
    employee_id: int = Field(foreign_key="employee.id", primary_key=True)
    vacation_type_id: int = Field(foreign_key="vacation_type.id", primary_key=True)
    available_days: int = Field(default=0)

class EmployeeVacationTypeAvailableDays(EmployeeVacationTypeAvailableDaysBase, table=True):
    __tablename__ = "employee_vacation_type_available_days"
    employee: "Employee" = Relationship(back_populates="vacation_type_available_days")
    vacation_type: "VacationType" = Relationship(back_populates="users_available_days")

class EmployeeAvailableDaysPublic(EmployeeVacationTypeAvailableDaysBase):
     vacation_type: VacationTypeBase


class VacationRequestStatus(int, enum.Enum):
    NEW = 0
    ACCEPTED = 1
    REJECTED = 2


class VacationRequest(SQLModel, table=True):
    __tablename__ = "vacation_request"
    id: int | None = Field(primary_key=True)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)
    reason: str | None = Field()
    status: VacationRequestStatus = Field(default=VacationRequestStatus.NEW)

    vacation_type_id: int = Field(foreign_key='vacation_type.id')
    vacation_type: VacationType = Relationship(back_populates="vacation_requests")

    employee_id: int = Field(foreign_key='employee.id', ondelete='CASCADE')
    employee: "Employee" = Relationship(back_populates="vacation_requests", sa_relationship_kwargs={"foreign_keys": "VacationRequest.employee_id"})

    manager_id: int = Field(foreign_key='employee.id', ondelete='SET NULL', nullable=True)
    manager: "Employee" = Relationship(back_populates="employees_requests", sa_relationship_kwargs={"foreign_keys": "VacationRequest.manager_id"})

    def __repr__(self):
        return f"""<VacationRequest {self.id}, 
        employee_id: {self.employee_id},
        request_type_id: {self.request_type_id}, 
        start_date: {self.start_date},
         end_date: {self.end_date}>"""



class VacationRequestPublic(CamelSQLModel):
    id: int
    start_date: date
    end_date: date
    reason: str | None
    vacation_type: VacationType
    status: VacationRequestStatus

class VacationRequestCreate(CamelSQLModel):
    start_date: date = Field()
    end_date: date
    reason: str | None = None
    status: VacationRequestStatus | None = Field(default=VacationRequestStatus.NEW)
    vacation_type_id: int


class VacationDaysInMonth(CamelSQLModel):
    month: int
    accepted_days: int
    new_days: int
    rejected_days: int