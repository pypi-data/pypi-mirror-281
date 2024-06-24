"""Add agent group asset type mapping

Revision ID: 3aa6ae380275
Revises: 5629037e8282
Create Date: 2024-06-13 14:03:10.208862

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3aa6ae380275"
down_revision = "5629037e8282"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "asset_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_asset_type")),
    )
    op.create_table(
        "agent_group_asset_type",
        sa.Column("agent_group_id", sa.Integer(), nullable=False),
        sa.Column("asset_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_group_id"],
            ["agent_group.id"],
            name=op.f("fk_agent_group_asset_type_agent_group_id_agent_group"),
        ),
        sa.ForeignKeyConstraint(
            ["asset_type_id"],
            ["asset_type.id"],
            name=op.f("fk_agent_group_asset_type_asset_type_id_asset_type"),
        ),
        sa.PrimaryKeyConstraint(
            "agent_group_id", "asset_type_id", name=op.f("pk_agent_group_asset_type")
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("agent_group_asset_type")
    op.drop_table("asset_type")
    # ### end Alembic commands ###
