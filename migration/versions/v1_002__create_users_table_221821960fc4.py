"""V1_002__create_users_table

Revision ID: 221821960fc4
Revises: e298eaaa8fad
Create Date: 2023-02-19 15:06:41.148106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "221821960fc4"
down_revision = "e298eaaa8fad"
branch_labels = None
depends_on = None
table_name = "users"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(64), nullable=False, unique=True),
        sa.Column("rating", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name)
