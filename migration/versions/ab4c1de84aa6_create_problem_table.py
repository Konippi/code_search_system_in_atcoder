"""create problem table

Revision ID: ab4c1de84aa6
Revises: 
Create Date: 2023-01-25 23:00:35.106507

"""
from alembic import op
import sqlalchemy as sa

revision = "ab4c1de84aa6"
down_revision = None
branch_labels = None
depends_on = None
table_name = "problem"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("contest", sa.Integer),
        sa.Column("diff", sa.String(2)),
        sa.Column("title", sa.String(128)),
    )


def downgrade() -> None:
    op.drop_table(table_name)