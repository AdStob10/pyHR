import enum
from datetime import date

from pydantic import Field

from app.database.models.vacation_request_model import VacationRequestStatus
from app.dependencies.deps import BaseListParams


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

    sort_id: SortType | None = Field(title="Sort Type", default=None)
    sort_start_date: SortType | None = Field(title="Sort Start Date", default=None)
    sort_end_date: SortType | None = Field(title="Sort End Date", default=None)


class SubordinateRequestListParams(BaseListParams):
    status: VacationRequestStatus | None = Field(title="Vacation Request Status", default=None)
    first_name: str | None = Field(title="Employee First Name", default=None)
    last_name: str | None = Field(title="Employee Last Name", default=None)
    reason: str | None = Field(title="Vacation Request Reason", default=None)
    start_date_eq: date | None = Field(title="Start date equal", default=None)
    start_date_ge: date | None = Field(title="Start date greater or equal than", default=None)
    start_date_le: date | None = Field(title="Start date less or equal than", default=None)
    end_date_eq: date | None = Field(title="End date equal", default=None)
    end_date_ge: date | None = Field(title="End date greater or equal than", default=None)
    end_date_le: date | None = Field(title="End date less or equal than", default=None)
    vacation_type_id: int | None = Field(title="Vacation Request Type", default=None)

    sort_id: SortType | None = Field(title="Sort Id", default=None)
    sort_full_name: SortType | None = Field(title="Sort Employee Full Name", default=None)
    sort_start_date: SortType | None = Field(title="Sort Start Date", default=None)
    sort_end_date: SortType | None = Field(title="Sort End Date", default=None)


class SubordinatesListParams(BaseListParams):
    first_name: str | None = Field(title="First Name", default=None)
    last_name: str | None = Field(title="Last Name", default=None)
    job_title: str | None = Field(title="Job Title", default=None)
    department: str | None = Field(title="Department", default=None)
    employment_date_eq: date | None = Field(title="Employment date equal", default=None)
    employment_date_ge: date | None = Field(title="Employment date greater or equal than", default=None)
    employment_date_le: date | None = Field(title="Employment date less or equal than", default=None)

    sort_id: SortType | None = Field(title="Sort Id", default=None)
    sort_full_name: SortType | None = Field(title="Sort Full Name", default=None)
    sort_employment_date: SortType | None = Field(title="Sort Employment Date", default=None)
