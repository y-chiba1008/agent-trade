from sqlalchemy.ext.asyncio import AsyncSession

from app.features.account.create.create_account_io import AccountData
from app.features.account.list.list_accounts_io import list_accounts as list_accounts_io


async def list_accounts(session: AsyncSession) -> list[AccountData]:
    return await list_accounts_io(session)
