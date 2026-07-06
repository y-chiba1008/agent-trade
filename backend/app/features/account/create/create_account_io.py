from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account_model import AccountModel
from app.features.account.shared.account_status import VALID_ACCOUNT_TAGS
from app.features.common.errors import ValidationError


@dataclass(frozen=True)
class AccountData:
    id: int
    name: str
    account_tag: str
    jpy_balance: int
    btc_balance: Decimal
    created_at: datetime
    updated_at: datetime


def validate_create_account(
    name: str,
    account_tag: str,
    initial_jpy_balance: int,
) -> None:
    if not name or len(name) > 100:
        raise ValidationError('口座名は1文字以上100文字以下である必要があります')
    if account_tag not in VALID_ACCOUNT_TAGS:
        raise ValidationError(f'account_tag は {sorted(VALID_ACCOUNT_TAGS)} のいずれかである必要があります')
    if initial_jpy_balance < 0:
        raise ValidationError('初期資金は0以上である必要があります')


async def insert_account(
    session: AsyncSession,
    name: str,
    account_tag: str,
    initial_jpy_balance: int,
) -> AccountData:
    account = AccountModel(
        name=name,
        account_tag=account_tag,
        jpy_balance=initial_jpy_balance,
        btc_balance=Decimal('0'),
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return _to_account_data(account)


def _to_account_data(account: AccountModel) -> AccountData:
    return AccountData(
        id=account.id,
        name=account.name,
        account_tag=account.account_tag,
        jpy_balance=account.jpy_balance,
        btc_balance=account.btc_balance,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )
