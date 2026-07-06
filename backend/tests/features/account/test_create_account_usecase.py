import pytest

from app.db.session import get_session_factory
from app.features.account.create.create_account_usecase import create_account
from app.features.account.list.list_accounts_usecase import list_accounts


@pytest.mark.asyncio
async def test_create_account() -> None:
    session_factory = get_session_factory()
    async with session_factory() as session:
        account = await create_account(
            session,
            name='test-human',
            account_tag='human',
            initial_jpy_balance=500_000,
        )
        assert account.id is not None
        assert account.name == 'test-human'
        assert account.jpy_balance == 500_000
        assert account.btc_balance == 0

        accounts = await list_accounts(session)
        assert any(a.id == account.id for a in accounts)
