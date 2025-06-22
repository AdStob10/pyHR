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
down_revision: Union[str, None] = 'e745bc2b55b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



vacation_type = sa.table(
    'vacation_type',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
    sa.column('default_available_days', sa.Integer),
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
            "name": "urlop wypoczynkowy",
            "default_available_days": 20
        },
        {
            "id": 2,
            "name": "urlop okolicznościowy",
            "default_available_days": None
        },
        {
            "id": 3,
            "name": "urlop na żądanie",
            "default_available_days": 4
        },
        {
            "id": 4,
            "name": "urlop bezpłatny",
            "default_available_days": None
        },
        {
            "id": 5,
            "name": "opieka nad dzieckiem",
            "default_available_days": None
        },
        {
            "id": 6,
            "name": "urlop macierzyński",
            "default_available_days": None
        }
    ])

    op.bulk_insert(available_employee_days, [
        {
            "employee_id": 3,
            "vacation_type_id": 1,
            "available_days": 26,
        },
        {
            "employee_id": 3,
            "vacation_type_id": 3,
            "available_days": 4,
        },
        {
            "employee_id": 1,
            "vacation_type_id": 1,
            "available_days": 26,
        },
        {
            "employee_id": 1,
            "vacation_type_id": 3,
            "available_days": 4,
        },
        {
            "employee_id": 2,
            "vacation_type_id": 1,
            "available_days": 26,
        },
        {
            "employee_id": 2,
            "vacation_type_id": 3,
            "available_days": 4,
        }
    ])


def downgrade() -> None:
    op.execute("DELETE FROM employee_vacation_type_available_days where employee_id in (1,2,3)")
    op.execute("DELETE FROM vacation_type where id <= 6")
