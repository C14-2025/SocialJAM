"""remove_friend_request_unique_constraint

Revision ID: c06d7c238d3d
Revises: 273b319dc616
Create Date: 2025-11-19 14:17:33.885112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c06d7c238d3d'
down_revision: Union[str, Sequence[str], None] = '273b319dc616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # For SQLite, we need to recreate the table without the unique constraint
    with op.batch_alter_table('friend_requests', schema=None) as batch_op:
        batch_op.drop_constraint('unique_friend_request', type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the unique constraint
    with op.batch_alter_table('friend_requests', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_friend_request', ['sender_id', 'receiver_id'])
