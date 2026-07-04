from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class SystemStatusModel(Base):
    __tablename__ = 'system_status'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_heartbeat_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
