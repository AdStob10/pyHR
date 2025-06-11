from typing import Generic, Any

from pydantic.fields import FieldInfo
from sqlalchemy import ColumnElement
from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar
from typing_extensions import TypeVar

from app.dependencies.deps import BaseListParams
from app.dependencies.query_params import SortType

T = TypeVar('T', bound=BaseListParams)

class OrderByTransfomer(Generic[T]):
    def __init__(self, filter_params: T, stmt: Select | SelectOfScalar, default_sort_col: str | None):
        self.filters = filter_params
        self.stmt = stmt
        self.cols = stmt.selected_columns
        self.default_sort_col = default_sort_col

    def transform_orders_by(self) -> Select | SelectOfScalar:
        model_dumped = self.filters.model_dump()
        order_params = {k: v for k, v in model_dumped.items() if k.startswith('sort') and v is not None}

        if len(order_params) == 0 and self.default_sort_col:
            col: ColumnElement = self.cols[self.default_sort_col]
            self.stmt = self.stmt.order_by(col)
            return self.stmt

        for k, v in order_params.items():
            self._transform_single_order_by(k, v)

        return self.stmt



    def _transform_single_order_by(self, name: str, value: SortType):
        _, col_name =  name.split(sep="_", maxsplit=1)
        col: ColumnElement = self.cols[col_name]

        match value:
            case SortType.DESCENDING:
                self.stmt = self.stmt.order_by(col.desc())
            case SortType.ASCENDING:
                self.stmt = self.stmt.order_by(col)
