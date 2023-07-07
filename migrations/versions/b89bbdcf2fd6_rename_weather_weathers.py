"""rename weather -> weathers

Revision ID: b89bbdcf2fd6
Revises: 73007c6784bd
Create Date: 2023-07-08 00:17:18.860909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b89bbdcf2fd6'
down_revision = '73007c6784bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weathers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('pressure', sa.Float(), nullable=False),
    sa.Column('humidity', sa.Integer(), nullable=False),
    sa.Column('wind_speed', sa.Float(), nullable=False),
    sa.Column('wind_deg', sa.Integer(), nullable=False),
    sa.Column('cloudiness', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('weather')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('city_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('temperature', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('pressure', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('humidity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('wind_speed', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('wind_deg', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('cloudiness', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], name='weather_city_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='weather_pkey')
    )
    op.drop_table('weathers')
    # ### end Alembic commands ###
