from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account_model import AccountModel
from app.features.account.create.create_account_io import AccountData, _to_account_data


async def list_accounts(session: AsyncSession) -> list[AccountData]:
    result = await session.execute(select(AccountModel).order_by(AccountModel.id))
    accounts = result.scalars().all()
    return [_to_account_data(account) for account in accounts]
