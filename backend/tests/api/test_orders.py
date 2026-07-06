from fastapi.testclient import TestClient


def test_market_order_flow(client: TestClient) -> None:
    create_response = client.post(
        '/accounts',
        json={
            'name': 'order-flow',
            'account_tag': 'human',
            'initial_jpy_balance': 1_000_000,
        },
    )
    account_id = create_response.json()['id']

    order_response = client.post(
        f'/accounts/{account_id}/orders',
        json={'side': 'buy', 'quantity': '0.001'},
    )
    assert order_response.status_code == 201
    order_data = order_response.json()
    assert order_data['execution_price_jpy'] == 10_000_000
    assert order_data['new_jpy_balance'] == 990_000

    orders_response = client.get(f'/accounts/{account_id}/orders')
    assert orders_response.status_code == 200
    orders = orders_response.json()
    assert len(orders) >= 1
    assert orders[0]['status'] == 'filled'

    executions_response = client.get(f'/accounts/{account_id}/executions')
    assert executions_response.status_code == 200
    executions = executions_response.json()
    assert len(executions) >= 1
    assert executions[0]['price'] == 10_000_000

    accounts_response = client.get('/accounts')
    account = next(a for a in accounts_response.json() if a['id'] == account_id)
    assert account['jpy_balance'] == 990_000
