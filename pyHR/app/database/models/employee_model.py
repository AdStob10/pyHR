from datetime import datetime
from typing import Annotated, Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

from app.database.models.vacation_request_model import EmployeeVacationTypeAvailableDays

if TYPE_CHECKING:
    from vacation_request_model import VacationRequest


class User(SQLModel):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field()
    email: Optional[str] = Field(max_length=150)


    def __repr__(self):
        return f"<User id:{self.id}, username:{self.username}>"


class UserPublic(BaseModel):
    id: int
    username: str
    email: Optional[str]



class Employee(User, table=True):
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    employment_date: datetime

    vacation_type_available_days : list["EmployeeVacationTypeAvailableDays"] = Relationship(back_populates="employee")
    vacation_requests: list["VacationRequest"] = Relationship(back_populates="employee", cascade_delete=True)



