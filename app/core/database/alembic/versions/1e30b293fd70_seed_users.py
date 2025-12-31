"""seed users

Revision ID: 1e30b293fd70
Revises: e4a135ce81c7
Create Date: 2025-12-30 22:25:05.650147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e30b293fd70'
down_revision: Union[str, Sequence[str], None] = 'e4a135ce81c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    INSERT INTO users (name, address, email, password) VALUES
    ('admin', 'admin', 'admin@admin.com.ar', md5('12345678'));
""")    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM users")
