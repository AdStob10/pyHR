"""Seed manager user

Revision ID: 04f9cb6d3e5a
Revises: 1f6176f2bc14
Create Date: 2025-05-21 15:28:51.337880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04f9cb6d3e5a'
down_revision: Union[str, None] = '1f6176f2bc14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = sa.table(
    'employee',
    sa.column('id', sa.Integer),
    sa.column('username', sa.String),
    sa.column("password", sa.String),
    sa.column('first_name', sa.String),
    sa.column('last_name', sa.String),
    sa.column('email', sa.String),
    sa.column('employment_date', sa.DateTime),
    sa.column("role", sa.Enum('BASIC_EMPLOYEE', 'MANAGER', 'ADMIN', name='employeerole')),
    sa.column('manager_id', sa.Integer),
)
# -- test123 ($2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW)

def upgrade() -> None:
    from datetime import datetime
    op.bulk_insert(users_table, [
        {
            'id': 2,
            'username': 'admin',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name':'Admin',
            'last_name':'Admin',
            'email': 'adm@example.com',
            'employment_date': datetime(2025, 1, 1),
            'role': 'ADMIN'
        },
    ])

    op.bulk_insert(users_table, [
        {
            'id': 3,
            'username': 'test_man',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name':'Jan',
            'last_name':'Kowalski',
            'email': 'manager@example.com',
            'employment_date': datetime(2025, 1, 1),
            'role': 'MANAGER',
            'manager_id': 2
        },
    ])



def downgrade() -> None:
    op.execute("DELETE FROM employee WHERE id=2 or id=3")
