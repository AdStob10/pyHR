from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel



class User(SQLModel):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field()
    email: Optional[str] = Field(max_length=150)


class Employee(User, table=True):
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    employment_date: datetime

    def __repr__(self):
        return f"<Employee id:{self.id}, {self.username}>"


class UserPublic(BaseModel):
    id: int
    username: str
    email: Optional[str]


class TokenData(BaseModel):
    sub: str

class Token(BaseModel):
    access_token: str
    token_type: str