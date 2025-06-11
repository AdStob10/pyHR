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
down_revision: Union[str, None] = '70edb8071a4b'
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
    sa.column('job_title', sa.String),
    sa.column('department', sa.String),
    sa.column("role", sa.Enum('BASIC_EMPLOYEE', 'MANAGER', 'ADMIN', name='employeerole')),
    sa.column('manager_id', sa.Integer),
)
# -- test123 ($2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW)

def upgrade() -> None:
    from datetime import datetime

    op.bulk_insert(users_table, [
        {
            'id': 1,
            'username': 'admin',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name': 'Jarosław',
            'last_name': 'Prezesowy',
            'email': 'adm@example.com',
            'employment_date': datetime(2023, 1, 1),
            'role': 'ADMIN',
            'job_title': 'Prezes',
            'department': 'Zarzad',
        },
    ])


    op.bulk_insert(users_table, [
        {
            'id': 2,
            'username': 'test_man',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name': 'Jan',
            'last_name': 'Kierownikowy',
            'email': 'manager@example.com',
            'employment_date': datetime(2024, 1, 1),
            'role': 'MANAGER',
            'manager_id': 1,
            'job_title': 'Kierownik',
            'department': 'Dział IT',
        },
    ])


    op.bulk_insert(users_table, [
        {
            'id': 3,
            'username': 'test_emp',
            'password': '$2a$12$wHwdTFpL2MJ2cbqwpi2uDur0TthhKhAPlLi.ZTmSIk18t/QB1YWeW',
            'first_name':'Antoni',
            'last_name':'Testowy',
            'email': 'emp1@example.com',
            'employment_date': datetime(2025, 1, 1),
            'job_title': 'Stażysta',
            'department': 'Dział IT',
            'role': 'BASIC_EMPLOYEE',
            'manager_id': 2,
        }
    ])








def downgrade() -> None:
    op.execute("DELETE FROM employee WHERE id in (1,2,3)")
