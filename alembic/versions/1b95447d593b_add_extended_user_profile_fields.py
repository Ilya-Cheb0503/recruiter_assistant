"""Add extended user profile fields

Revision ID: 1b95447d593b
Revises: f6352590ad32
Create Date: 2025-06-12 11:57:02.220650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b95447d593b'
down_revision: Union[str, None] = 'f6352590ad32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Создаем новую временную таблицу с нужной структурой
    op.create_table(
        'users_new',
        sa.Column('tg_id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('position', sa.String(), nullable=True),
        sa.Column('experience', sa.String(), nullable=True),
        sa.Column('education', sa.String(), nullable=True)
    )

    # Копируем данные из старой таблицы
    op.execute("""
        INSERT INTO users_new (tg_id, name, phone)
        SELECT tg_id, name, phone FROM users
    """)

    # Удаляем старую таблицу
    op.drop_table('users')

    # Переименовываем новую таблицу
    op.rename_table('users_new', 'users')
