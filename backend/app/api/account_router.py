from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.features.account.create.create_account_usecase import create_account
from app.features.account.delete.delete_account_usecase import delete_account
from app.features.account.list.list_accounts_usecase import list_accounts

router = APIRouter(prefix='/accounts', tags=['accounts'])


class CreateAccountRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    account_tag: str
    initial_jpy_balance: int = Field(ge=0)


class AccountResponse(BaseModel):
    id: int
    name: str
    account_tag: str
    jpy_balance: int
    btc_balance: Decimal
    created_at: datetime
    updated_at: datetime


@router.post('', response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account_endpoint(
    body: CreateAccountRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AccountResponse:
    account = await create_account(
        session,
        name=body.name,
        account_tag=body.account_tag,
        initial_jpy_balance=body.initial_jpy_balance,
    )
    return AccountResponse(
        id=account.id,
        name=account.name,
        account_tag=account.account_tag,
        jpy_balance=account.jpy_balance,
        btc_balance=account.btc_balance,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@router.get('', response_model=list[AccountResponse])
async def list_accounts_endpoint(
    session: AsyncSession = Depends(get_db_session),
) -> list[AccountResponse]:
    accounts = await list_accounts(session)
    return [
        AccountResponse(
            id=account.id,
            name=account.name,
            account_tag=account.account_tag,
            jpy_balance=account.jpy_balance,
            btc_balance=account.btc_balance,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )
        for account in accounts
    ]


@router.delete('/{account_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account_endpoint(
    account_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await delete_account(session, account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
