"""update multiple tables to use server_default now

Revision ID: 9b5a729106ab
Revises: 54c1aa40775d
Create Date: 2026-04-26 13:15:41.567279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9b5a729106ab'
down_revision: Union[str, Sequence[str], None] = '54c1aa40775d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 1. HAZ UNA LISTA CON LOS NOMBRES DE TUS TABLAS (como están en la BD)
TABLAS_A_ACTUALIZAR = [
    "users", 
    "books", 
]


def upgrade() -> None:
    """Upgrade schema."""
    for tabla in TABLAS_A_ACTUALIZAR:
        # Alteramos created_at
        op.alter_column(
            table_name=tabla,
            column_name='created_at',
            server_default=sa.text('now()')
        )
        
        # OJO AQUÍ: Si "users" no tiene updated_at, esto dará un error.
        # Solo haz esto si TODAS las tablas en la lista tienen la columna updated_at.
        # Si la tabla "users" no lo tiene, sácala de este bucle o haz un bucle separado.
        if tabla == "books":  # <- Por ejemplo, si solo books lo tiene
            op.alter_column(
                table_name=tabla,
                column_name='updated_at',
                server_default=sa.text('now()')
            )

def downgrade() -> None:
    """Downgrade schema."""
    for tabla in TABLAS_A_ACTUALIZAR:
        op.alter_column(
            table_name=tabla,
            column_name='created_at',
            server_default=None
        )
        if tabla == "books":
            op.alter_column(
                table_name=tabla,
                column_name='updated_at',
                server_default=None
            )
