"""Seed basic vacation request types

Revision ID: aa1726d9c0fc
Revises: 25930cf0bc12
Create Date: 2025-04-24 14:04:40.603249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa1726d9c0fc'
down_revision: Union[str, None] = '25930cf0bc12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



vacation_type = sa.table(
    'vacation_type',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
)

available_employee_days = sa.table(
    'employee_vacation_type_available_days',
    sa.column('employee_id', sa.Integer),
    sa.column('vacation_type_id', sa.Integer),
    sa.column('available_days', sa.Integer),
)

def upgrade() -> None:
    op.bulk_insert(vacation_type, [
        {
            "id": 1,
            "name": "urlop wypoczynkowy"
        },
        {
            "id": 2,
            "name": "urlop okolicznościowy"
        },
        {
            "id": 3,
            "name": "urlop na żądanie"
        },
        {
            "id": 4,
            "name": "urlop bezpłatny"
        },
        {
            "id": 5,
            "name": "opieka nad dzieckiem"
        },
        {
            "id": 6,
            "name": "urlop macierzyński"
        }
    ])

    op.bulk_insert(available_employee_days, [
        {
            "employee_id": 1,
            "vacation_type_id": 1,
            "available_days": 26,
        },
        {
            "employee_id": 1,
            "vacation_type_id": 3,
            "available_days": 4,
        }
    ])


def downgrade() -> None:
    op.execute("DELETE FROM employee_vacation_type_available_days where employee_id = 1")
    op.execute("DELETE FROM vacation_request_type where vacation_type_id <= 6")
