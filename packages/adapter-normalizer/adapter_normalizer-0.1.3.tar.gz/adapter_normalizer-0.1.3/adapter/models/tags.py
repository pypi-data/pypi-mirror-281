from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from adapter.models.base import Base


class Tag(Base):
    groups: Mapped[list] = mapped_column(JSONB, server_default="[]", default=[])
    labels: Mapped[list] = mapped_column(JSONB, server_default="[]", default=[])

    def __str__(self) -> str:
        return f"Tag({self.id})"
