from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account_model import AccountModel
from app.db.models.execution_model import ExecutionModel
from app.db.models.order_model import OrderModel
from app.features.common.errors import NotFoundError


@dataclass(frozen=True)
class ExecutionData:
    id: int
    order_id: int
    quantity: Decimal
    price: int
    executed_at: datetime
    updated_at: datetime


async def list_executions(session: AsyncSession, account_id: int) -> list[ExecutionData]:
    account_exists = await session.execute(
        select(AccountModel.id).where(AccountModel.id == account_id)
    )
    if account_exists.scalar_one_or_none() is None:
        raise NotFoundError(f'口座 id={account_id} が見つかりません')

    result = await session.execute(
        select(ExecutionModel)
        .join(OrderModel, ExecutionModel.order_id == OrderModel.id)
        .where(OrderModel.account_id == account_id)
        .order_by(ExecutionModel.id.desc())
    )
    executions = result.scalars().all()
    return [
        ExecutionData(
            id=execution.id,
            order_id=execution.order_id,
            quantity=execution.quantity,
            price=execution.price,
            executed_at=execution.executed_at,
            updated_at=execution.updated_at,
        )
        for execution in executions
    ]
