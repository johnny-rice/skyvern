"""Add deleted_at column to debug_sessions table

Revision ID: bddb54c1509b
Revises: f72cf593e1a7
Create Date: 2025-07-30 23:38:32.738095+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bddb54c1509b"
down_revision: Union[str, None] = "f72cf593e1a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("debug_sessions", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("debug_sessions", "deleted_at")
    # ### end Alembic commands ###
