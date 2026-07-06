from sqlalchemy.ext.asyncio import AsyncSession

from app.features.account.create.create_account_io import AccountData, insert_account, validate_create_account


async def create_account(
    session: AsyncSession,
    name: str,
    account_tag: str,
    initial_jpy_balance: int,
) -> AccountData:
    validate_create_account(name, account_tag, initial_jpy_balance)
    return await insert_account(session, name, account_tag, initial_jpy_balance)
