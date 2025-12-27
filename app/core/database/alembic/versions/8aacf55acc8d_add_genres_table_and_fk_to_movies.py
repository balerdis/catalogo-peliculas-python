"""add genres table and fk to movies

Revision ID: 8aacf55acc8d
Revises: 8974c06de62a
Create Date: 2025-12-27 13:28:46.746640

"""
from http import server
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8aacf55acc8d'
down_revision: Union[str, Sequence[str], None] = '8974c06de62a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # creat tabla genres
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=True, unique=True),
        sa.Column("falta", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("fmodificacion", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column("habilitado", sa.Boolean(), server_default=sa.text("1"), nullable=True),
        sa.Column("feliminado", sa.DateTime(), nullable=True),
    )

    # Insert generos base (Incluye fallback)
    op.execute("""
        INSERT INTO genres (name) VALUES
        ('Action'),
        ('Adventure'),
        ('Comedy'),
        ('Drama'),
        ('Fantasy'),
        ('Horror'),
        ('Romance'),
        ('Sci-Fi'),
        ('Thriller'),
        ('Documentary'),
        ('No identificado')
    """)    

    # Agregar columna genre_id (nullable)
    op.add_column(
        "movies",
        sa.Column("genre_id", sa.Integer(), nullable=True)
    )    

    # Mapear genres existentes → FK
    op.execute("""
        UPDATE movies m
        JOIN genres g ON LOWER(TRIM(m.genre)) = LOWER(TRIM(g.name))
        SET m.genre_id = g.id
    """)

    # Asignar "No identificado" a los que no matchearon
    op.execute("""
        UPDATE movies
        SET genre_id = (
            SELECT id FROM genres WHERE name = 'No identificado'
        )
        WHERE genre_id IS NULL
    """)

    # Crear FK
    op.create_foreign_key(
        "fk_movies_genre",
        "movies",
        "genres",
        ["genre_id"],
        ["id"],
        ondelete="NO ACTION",
        onupdate="NO ACTION"
    )

    # Forzar NOT NULL
    op.alter_column(
        "movies",
        "genre_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # eliminar columna vieja
    op.drop_column("movies", "genre")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("movies", sa.Column("genre", sa.String(50)))

    op.execute("""
        UPDATE movies m
        JOIN genres g ON m.genre_id = g.id
        SET m.genre = g.name
    """)

    op.drop_constraint("fk_movies_genre", "movies", type_="foreignkey")
    op.drop_column("movies", "genre_id")
    op.drop_table("genres")            