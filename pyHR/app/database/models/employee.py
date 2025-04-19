from datetime import datetime
from typing import Annotated
from sqlmodel import Field, SQLModel

class Employee(SQLModel, table=True):
    __tablename__ = "employee"
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    password: str
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    employment_date: datetime
    email: str = Field(max_length=150)

    def __repr__(self):
        return f"<Employee id:{self.id}, {self.username}>"