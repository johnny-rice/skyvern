"""Add RESIDENTIAL_IE to ProxyLocation enum

Revision ID: c5ed5a3a14eb
Revises: 94bc3829eed6
Create Date: 2024-07-31 09:32:03.548241+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5ed5a3a14eb"
down_revision: Union[str, None] = "94bc3829eed6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE proxylocation ADD VALUE 'RESIDENTIAL_IE'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
