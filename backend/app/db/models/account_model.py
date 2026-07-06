from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.order_model import OrderModel


class AccountModel(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_tag: Mapped[str] = mapped_column(String(20), nullable=False)
    jpy_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='0')
    btc_balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        server_default='0',
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    orders: Mapped[list['OrderModel']] = relationship(
        'OrderModel',
        back_populates='account',
        cascade='all, delete-orphan',
    )
