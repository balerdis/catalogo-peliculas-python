"""add users table and audit fields

Revision ID: e4a135ce81c7
Revises: 8aacf55acc8d
Create Date: 2025-12-30 22:06:14.943082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e4a135ce81c7'
down_revision: Union[str, Sequence[str], None] = '8aacf55acc8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ---- USERS ----
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255)),
        sa.Column('address', sa.String(length=255)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('password', sa.String(length=255)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('modificated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('habilited', sa.Boolean(), server_default='1'),
        sa.Column('deleted_at', sa.DateTime())
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=False)

    # ---- GENRES: RENOMBRES ----
    op.alter_column(
        'genres',
        'habilitado',
        new_column_name='habilited',
        existing_type=mysql.TINYINT(display_width=1)
    )

    op.alter_column(
        'genres',
        'falta',
        new_column_name='created_at',
        existing_type=mysql.DATETIME()
    )

    op.alter_column(
        'genres',
        'fmodificacion',
        new_column_name='modificated_at',
        existing_type=mysql.DATETIME()
    )

    op.alter_column(
        'genres',
        'feliminado',
        new_column_name='deleted_at',
        existing_type=mysql.DATETIME()
    )   

    # ---- ÍNDICES ----
    op.create_index('ix_genres_active', 'genres', ['habilited', 'deleted_at'])

    op.drop_index(op.f('name'), table_name='genres')
    op.create_index('ix_genres_name', 'genres', ['name'])

    op.create_index(op.f('ix_movies_genre_id'), 'movies', ['genre_id'])


def downgrade() -> None:
    """Downgrade schema."""
     # ---- FK ----
    op.drop_index(op.f('ix_movies_genre_id'), table_name='movies')

    # ---- GENRES ----
    op.drop_index('ix_genres_name', table_name='genres')
    op.drop_index('ix_genres_active', table_name='genres')

    op.alter_column(
        'genres',
        'deleted_at',
        new_column_name='feliminado',
        existing_type=mysql.DATETIME()
    )

    op.alter_column(
        'genres',
        'modificated_at',
        new_column_name='fmodificacion',
        existing_type=mysql.DATETIME()
    )

    op.alter_column(
        'genres',
        'created_at',
        new_column_name='falta',
        existing_type=mysql.DATETIME()
    )

    op.alter_column(
        'genres',
        'habilited',
        new_column_name='habilitado',
        existing_type=mysql.TINYINT(display_width=1)
    )


    op.create_index('ix_genres_active', 'genres', ['habilitado', 'feliminado'])
    op.create_index(op.f('name'), 'genres', ['name'], unique=True)

    # ---- USERS ----
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
