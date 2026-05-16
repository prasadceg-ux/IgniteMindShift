"""add_school_districts_and_district_id

Revision ID: b8c97e58b7a3
Revises: 
Create Date: 2026-05-15 18:39:01.674663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8c97e58b7a3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create school_districts table first (FK target must exist before referencing it)
    op.create_table(
        'school_districts',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_school_districts_name', 'school_districts', ['name'])

    # Add district_id to users
    op.add_column('users', sa.Column('district_id', sa.String(length=36), nullable=True))
    op.create_index(op.f('ix_users_district_id'), 'users', ['district_id'], unique=False)
    op.create_foreign_key('fk_users_district_id', 'users', 'school_districts', ['district_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_users_district_id', 'users', type_='foreignkey')
    op.drop_index(op.f('ix_users_district_id'), table_name='users')
    op.drop_column('users', 'district_id')
    op.drop_index('ix_school_districts_name', table_name='school_districts')
    op.drop_table('school_districts')
