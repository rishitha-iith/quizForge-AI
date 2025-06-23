"""Add difficulty column to quiz

Revision ID: dc8cfc959488
Revises: 
Create Date: 2025-06-23 19:19:02.851441
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dc8cfc959488'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('quiz', sa.Column('difficulty', sa.String(), nullable=False, server_default='medium'))
    op.add_column('quiz', sa.Column('duration_minutes', sa.Integer(), nullable=True))

    # Optional: Remove server_default after adding (to keep it clean)
    op.alter_column('quiz', 'difficulty', server_default=None)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('quiz', 'duration_minutes')
    op.drop_column('quiz', 'difficulty')
