from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar

from app.database.filter_utils import FilterTransfomer
from app.database.order_utils import OrderByTransfomer
from app.dependencies.deps import BaseListParams



def apply_filters_and_sort(stmt: Select | SelectOfScalar, params: BaseListParams):
    stmt = FilterTransfomer(params, stmt).transform_filters()
    stmt = OrderByTransfomer(params, stmt).transform_orders_by()
    return stmt

