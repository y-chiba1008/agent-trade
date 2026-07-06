from sqlalchemy.ext.asyncio import AsyncSession

from app.features.account.delete.delete_account_io import delete_account as delete_account_io


async def delete_account(session: AsyncSession, account_id: int) -> None:
    await delete_account_io(session, account_id)
