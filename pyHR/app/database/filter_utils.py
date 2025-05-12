import builtins
import datetime
from typing import TypeVar, Any, get_args, Generic

from pydantic.fields import FieldInfo
from sqlmodel.sql._expression_select_cls import SelectOfScalar
from sqlmodel.sql.expression import ColumnElement, Select

from app.dependencies.deps import BaseListParams

T = TypeVar("T", bound=BaseListParams)

class FilterTransfomer(Generic[T]):
    def __init__(self, filter_params: T, stmt: Select | SelectOfScalar):
        self.filters = filter_params
        self.stmt = stmt
        self.cols = stmt.selected_columns

    def transform_filters(self) -> Select | SelectOfScalar:
        model_dumped = self.filters.model_dump()

        #logger.info("Filters = {}", model_dumped)
        fields: dict[str, FieldInfo] = type(self.filters).model_fields
        #logger.info("Filters FIELDS = {}", fields)
        #logger.info("Columns stmt = {}", self.cols)
        for k, v in model_dumped.items():
            if v is None or k in ["offset", "limit"] or k.startswith("sort"):
                continue
            print(f"{k}: {v}, {fields[k].annotation}")
            self._transform_single_field(k, v, fields[k].annotation)

        return self.stmt

    def _transform_single_field(self, name: str, value: Any,  field_type: type):
        union_type_args = get_args(field_type)
        value_type: type = [x for x in union_type_args if x != type(None)][0]

        match value_type:
            case builtins.int:
                #print(f"{name}: {value} int")
                self._transform_int_type(name, value)
            case builtins.str:
                #print(f"{name}: {value} To jest str")
                self._transform_str_type(name, f"%{value}%")
            case datetime.date:
                #print(f"{name}: {value} To jest date")
                self._transform_date_type(name, value)
            case _:
                #print(f"{name}: {value} to jest default")
                self._transform_default_type(name, value)


    def _transform_int_type(self, name: str, value: int):
        col: ColumnElement[int] = self.cols[name]
        self.stmt = self.stmt.where(col == value)
        #print(f"{name} a kolumna {self.cols[name]}")
        #print(f"Typ {type(self.cols[name])}")

    def _transform_str_type(self, name: str, value: str):
        col: ColumnElement[str] = self.cols[name]
        self.stmt = self.stmt.where(col.ilike(value))

    def _transform_date_type(self, name: str, value: datetime.date):
        col_name, operator = name.rsplit(sep="_", maxsplit=1)
        col: ColumnElement[datetime.date] = self.cols[col_name]
        self._transform_clause_by_operator(col, operator, value)


    def _transform_default_type(self, name: str, value: Any):
        col: ColumnElement = self.cols[name]
        self.stmt = self.stmt.where(col == value)
        #print(f"{name} a kolumna {self.cols[name]}")
        #print(f"Typ {type(self.cols[name])}")


    def _transform_clause_by_operator(self, col: ColumnElement, operator: str, value: Any):
        match operator:
            case "ge":
                self.stmt = self.stmt.where(col >= value)
            case "le":
                self.stmt = self.stmt.where(col <= value)
            case "lt":
                self.stmt = self.stmt.where(col < value)
            case "gt":
                self.stmt = self.stmt.where(col > value)