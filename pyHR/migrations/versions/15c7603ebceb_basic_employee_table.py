"""Basic employee table

Revision ID: 15c7603ebceb
Revises: 
Create Date: 2025-04-18 21:40:25.487820

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15c7603ebceb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('employee',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=150), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=150), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=150), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employment_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_username'), 'employee', ['username'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_employee_username'), table_name='employee')
    op.drop_table('employee')
    from sqlalchemy.dialects import postgresql
    employee_role = postgresql.ENUM('BASIC_EMPLOYEE', 'MANAGER', 'ADMIN', name='employeerole')
    employee_role.drop(op.get_bind(), checkfirst=True)
