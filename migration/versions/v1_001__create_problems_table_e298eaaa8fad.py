"""V1_001__create_problems_table

Revision ID: e298eaaa8fad
Revises: 
Create Date: 2023-02-19 15:06:02.840890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e298eaaa8fad"
down_revision = None
branch_labels = None
depends_on = None
table_name = "problems"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("contest", sa.Integer, nullable=False),
        sa.Column("diff", sa.String(2), nullable=False),
        sa.Column("title", sa.String(128), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table(table_name)
