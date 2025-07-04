"""Initial migration

Revision ID: d7b21e7a3fa0
Revises: 
Create Date: 2025-06-30 08:26:42.917964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd7b21e7a3fa0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('quiz', 'participants_attempted',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('0'))
    # op.drop_constraint(op.f('quiz_quiz_id_unique'), 'quiz', type_='unique')
    op.create_index(op.f('ix_quiz_quiz_id'), 'quiz', ['quiz_id'], unique=True)
    op.drop_constraint(op.f('quiz_creator_id_fkey'), 'quiz', type_='foreignkey')
    op.create_foreign_key(None, 'quiz', 'user', ['creator_id'], ['user_id'])
    op.alter_column('quizresult', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('quizresult', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('user_id_seq'::regclass)"))
    op.alter_column('userbadge', 'scope',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("'overall'::character varying"))
    op.alter_column('userbadge', 'awarded_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('userquiz', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('userquiz', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('userresponse', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('userresponse', 'question_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('userresponse', 'question_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('userresponse', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('userquiz', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('userquiz', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('userbadge', 'awarded_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('userbadge', 'scope',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_server_default=sa.text("'overall'::character varying"))
    op.alter_column('user', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('user_id_seq'::regclass)"))
    op.alter_column('quizresult', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('quizresult', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'quiz', type_='foreignkey')
    op.create_foreign_key(op.f('quiz_creator_id_fkey'), 'quiz', 'user', ['creator_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_quiz_quiz_id'), table_name='quiz')
    op.create_unique_constraint(op.f('quiz_quiz_id_unique'), 'quiz', ['quiz_id'], postgresql_nulls_not_distinct=False)
    op.alter_column('quiz', 'participants_attempted',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('0'))
    op.alter_column('question', 'quiz_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
