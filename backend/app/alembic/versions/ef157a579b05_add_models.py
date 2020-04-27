"""add models

Revision ID: ef157a579b05
Revises: 
Create Date: 2020-04-27 01:11:02.135055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef157a579b05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deck_id'), 'deck', ['id'], unique=False)
    op.create_index(op.f('ix_deck_title'), 'deck', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('repetition_model', sa.Enum('leitner', 'sm2', 'karl', name='repetition'), nullable=False),
    sa.Column('default_deck_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['default_deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('fact',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('create_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('update_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('answer_lines', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('extra', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    op.create_index(op.f('ix_fact_answer'), 'fact', ['answer'], unique=False)
    op.create_index(op.f('ix_fact_card_id'), 'fact', ['card_id'], unique=False)
    op.create_index(op.f('ix_fact_text'), 'fact', ['text'], unique=False)
    op.create_table('user_deck',
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('permissions', sa.Enum('owner', 'viewer', name='permission'), nullable=False),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('deck_id', 'owner_id')
    )
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fact_id', sa.Integer(), nullable=False),
    sa.Column('log_type', sa.Enum('study', 'suspend', 'delete', 'report', 'unsuspend', 'undo_delete', 'resolve_report', 'undo_study', name='log'), nullable=False),
    sa.Column('repetition_model', sa.Enum('leitner', 'sm2', 'karl', name='repetition'), nullable=False),
    sa.Column('details', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['fact_id'], ['fact.card_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_history_id'), 'history', ['id'], unique=False)
    op.create_table('suspended',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fact_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_suspended', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('type', sa.Enum('delete', 'suspend', 'report', name='suspendtype'), nullable=False),
    sa.ForeignKeyConstraint(['fact_id'], ['fact.card_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_suspended_id'), 'suspended', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_suspended_id'), table_name='suspended')
    op.drop_table('suspended')
    op.drop_index(op.f('ix_history_id'), table_name='history')
    op.drop_table('history')
    op.drop_table('user_deck')
    op.drop_index(op.f('ix_fact_text'), table_name='fact')
    op.drop_index(op.f('ix_fact_card_id'), table_name='fact')
    op.drop_index(op.f('ix_fact_answer'), table_name='fact')
    op.drop_table('fact')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_deck_title'), table_name='deck')
    op.drop_index(op.f('ix_deck_id'), table_name='deck')
    op.drop_table('deck')
    # ### end Alembic commands ###