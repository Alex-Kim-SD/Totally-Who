"""create bots conversation_settings debates transcripts tables

Revision ID: a3e212349cf3
Revises: ffdc0a98111c
Create Date: 2023-07-12 01:30:21.600328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Text
from sqlalchemy.dialects import postgresql
import os


# revision identifiers, used by Alembic.
revision = 'a3e212349cf3'
down_revision = 'ffdc0a98111c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('settings', postgresql.JSON(astext_type=Text()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('conversation_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('setting_details', postgresql.JSON(astext_type=Text()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('debates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conversation_setting_id', sa.Integer(), nullable=False),
    sa.Column('initiator_bot_id', sa.Integer(), nullable=False),
    sa.Column('opponent_bot_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('topic', sa.String(length=255), nullable=True),
    sa.Column('result', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['conversation_setting_id'], ['conversation_settings.id'], ),
    sa.ForeignKeyConstraint(['initiator_bot_id'], ['bots.id'], ),
    sa.ForeignKeyConstraint(['opponent_bot_id'], ['bots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transcripts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('bot_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bot_id'], ['bots.id'], ),
    sa.ForeignKeyConstraint(['debate_id'], ['debates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transcripts')
    op.drop_table('debates')
    op.drop_table('conversation_settings')
    op.drop_table('bots')
    # ### end Alembic commands ###
