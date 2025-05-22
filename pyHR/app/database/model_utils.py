from typing import Generic

from pydantic import BaseModel
from sqlmodel import SQLModel
from humps import camelize
from typing_extensions import TypeVar


def to_camel(string):
    return camelize(string)


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True



class CamelSQLModel(SQLModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True



T = TypeVar("T")
class PaginatedList(CamelBaseModel, Generic[T]):
    data: list[T]
    row_count: int