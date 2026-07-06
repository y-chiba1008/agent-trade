from fastapi.testclient import TestClient


def test_create_and_list_accounts(client: TestClient) -> None:
    response = client.post(
        '/accounts',
        json={
            'name': 'api-test',
            'account_tag': 'human',
            'initial_jpy_balance': 1_000_000,
        },
    )
    assert response.status_code == 201
    created = response.json()
    assert created['name'] == 'api-test'
    assert created['jpy_balance'] == 1_000_000

    list_response = client.get('/accounts')
    assert list_response.status_code == 200
    accounts = list_response.json()
    assert any(a['id'] == created['id'] for a in accounts)


def test_delete_account(client: TestClient) -> None:
    create_response = client.post(
        '/accounts',
        json={
            'name': 'to-delete',
            'account_tag': 'ai',
            'initial_jpy_balance': 100_000,
        },
    )
    account_id = create_response.json()['id']

    delete_response = client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 204

    list_response = client.get('/accounts')
    accounts = list_response.json()
    assert all(a['id'] != account_id for a in accounts)
