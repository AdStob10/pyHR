import enum

from pydantic import Field

from app.database.models.vacation_request_model import VacationRequestStatus
from app.dependencies.deps import BaseListParams
from datetime import date

class SortType(str, enum.Enum):
    ASCENDING = "ASC"
    DESCENDING = "DESC"


class VacationRequestListParams(BaseListParams):
    status: VacationRequestStatus | None = Field(title="Vacation Request Status", default=None)
    reason: str | None = Field(title="Vacation Request Reason", default=None)
    start_date_eq: date | None = Field(title="Start date equal", default=None)
    start_date_ge: date | None = Field(title="Start date greater or equal than", default=None)
    start_date_le: date | None = Field(title="Start date less or equal than", default=None)
    end_date_eq: date | None = Field(title="End date equal", default=None)
    end_date_ge: date | None = Field(title="End date greater or equal than", default=None)
    end_date_le: date | None = Field(title="End date less or equal than", default=None)
    vacation_type_id: int | None = Field(title="Vacation Request Type", default=None)

    sort_start_date: SortType | None = Field(title="Sort Start Date", default=None)
    sort_end_date: SortType | None = Field(title="Sort End Date", default=None)

