"""finalidades: muda coluna base legal para enum

Revision ID: 106a8326d371
Revises: cd20314d2d5d
Create Date: 2025-10-14 23:02:26.033740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '106a8326d371'
down_revision: Union[str, Sequence[str], None] = 'cd20314d2d5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type first
    baselegal_enum = sa.Enum(
        'Consentimento',
        'Obrigação Legal', 
        'Execução de Contrato',
        'Proteção da Vida',
        'Legítimo Interesse',
        name='baselegal',
        create_type=True
    )
    baselegal_enum.create(op.get_bind(), checkfirst=True)
    
    # Convert the column with explicit USING clause
    op.execute("""
        ALTER TABLE finalidades 
        ALTER COLUMN base_legal TYPE baselegal 
        USING base_legal::baselegal
    """)
    
    # Set nullable to False
    op.alter_column('finalidades', 'base_legal', nullable=False)
    
    # Other changes
    op.add_column('registros_consentimento', sa.Column('data_registro', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('registros_consentimento', sa.Column('data_revogacao', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('registros_consentimento', 'data_concessao')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('registros_consentimento', sa.Column('data_concessao', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_column('registros_consentimento', 'data_revogacao')
    op.drop_column('registros_consentimento', 'data_registro')
    
    # Convert back to VARCHAR
    op.execute("ALTER TABLE finalidades ALTER COLUMN base_legal TYPE VARCHAR USING base_legal::text")
    
    # Drop the enum type
    sa.Enum(name='baselegal').drop(op.get_bind(), checkfirst=True)
    
    op.alter_column('finalidades', 'base_legal', nullable=True)
