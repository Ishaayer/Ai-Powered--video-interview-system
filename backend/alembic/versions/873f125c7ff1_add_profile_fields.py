"""add_profile_fields

Revision ID: 873f125c7ff1
Revises: a5d9b03c5b1a
Create Date: 2026-08-02 21:39:45.046313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '873f125c7ff1'
down_revision: Union[str, Sequence[str], None] = 'a5d9b03c5b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "candidate_profiles",
        sa.Column("phone", sa.String(length=30), nullable=True),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column("location", sa.String(length=150), nullable=True),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column("linkedin_url", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column("github_url", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("candidate_profiles", "github_url")
    op.drop_column("candidate_profiles", "linkedin_url")
    op.drop_column("candidate_profiles", "location")
    op.drop_column("candidate_profiles", "phone")
