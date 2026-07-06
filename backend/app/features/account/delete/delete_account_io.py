from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account_model import AccountModel
from app.features.common.errors import NotFoundError


async def delete_account(session: AsyncSession, account_id: int) -> None:
    result = await session.execute(
        delete(AccountModel).where(AccountModel.id == account_id).returning(AccountModel.id)
    )
    deleted_id = result.scalar_one_or_none()
    if deleted_id is None:
        raise NotFoundError(f'口座 id={account_id} が見つかりません')
    await session.commit()
