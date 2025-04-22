"""Seed test user

Revision ID: e745bc2b55b9
Revises: 15c7603ebceb
Create Date: 2025-04-19 12:25:51.367223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e745bc2b55b9'
down_revision: Union[str, None] = '15c7603ebceb'
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
)
# -- test123 ($2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW)

def upgrade() -> None:
    from datetime import datetime
    op.bulk_insert(users_table, [
        {
            'id': 1,
            'username': 'test_emp',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name':'Test',
            'last_name':'Testowy',
            'email': 'emp1@example.com',
            'employment_date': datetime(2025, 1, 1)
        }
    ])


def downgrade() -> None:
    op.execute("DELETE FROM employee WHERE id=1")
