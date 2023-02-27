"""V1_003__create_submissions_table

Revision ID: 8b9a3941483d
Revises: 221821960fc4
Create Date: 2023-02-19 15:06:53.549961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b9a3941483d"
down_revision = "221821960fc4"
branch_labels = None
depends_on = None
table_name = "submissions"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        ),
        sa.Column(
            "problem_id",
            sa.Integer,
            sa.ForeignKey("problems.id", onupdate="CASCADE", ondelete="CASCADE"),
        ),
        sa.Column("language", sa.String(32), nullable=False),
        sa.Column("code_len", sa.String(8), nullable=False),
        sa.Column("code", sa.String(10000), nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name)
