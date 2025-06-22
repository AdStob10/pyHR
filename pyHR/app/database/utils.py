from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar

from app.database.filter_utils import FilterTransfomer
from app.database.order_utils import OrderByTransfomer
from app.dependencies.deps import BaseListParams


def apply_filters_and_sort(stmt: Select | SelectOfScalar, params: BaseListParams, default_sort: str | None):
    """
    Apply filtering and sorting on sql alchemy query
    :param stmt: sql alchemy Select
    :param params: filter and sort parameters
    :param default_sort: default sorting column
    :return: statement with where and order by clauses
    """
    stmt = FilterTransfomer(params, stmt).transform_filters()
    stmt = OrderByTransfomer(params, stmt, default_sort).transform_orders_by()
    return stmt
