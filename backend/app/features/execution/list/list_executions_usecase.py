from sqlalchemy.ext.asyncio import AsyncSession

from app.features.execution.list.list_executions_io import ExecutionData, list_executions as list_executions_io


async def list_executions(session: AsyncSession, account_id: int) -> list[ExecutionData]:
    return await list_executions_io(session, account_id)
