from fastapi.testclient import TestClient


def test_get_price(client: TestClient) -> None:
    response = client.get('/price/BTC_JPY')
    assert response.status_code == 200
    data = response.json()
    assert data['product_code'] == 'BTC_JPY'
    assert data['price_jpy'] == 10_000_000
