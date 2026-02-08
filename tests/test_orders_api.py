import pytest


@pytest.mark.anyio
async def test_create_order_item_success_new_product(client):
    """Успешное добавление нового товара в заказ"""
    response = await client.post(
        "/orders/create-item", json={"order_id": 1, "product_id": 2, "quantity": 1}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == 1
    assert data["product_id"] == 2
    assert data["quantity"] == 1
    assert data["price_at_order"] == 75000.00


@pytest.mark.anyio
async def test_create_order_item_update_existing_quantity(client):
    """Обновление существующей позиции: увеличение количества"""
    response = await client.post(
        "/orders/create-item", json={"order_id": 4, "product_id": 5, "quantity": 3}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 2 + 3  # Было 2, добавили 3, стало 5


@pytest.mark.anyio
async def test_create_order_item_nonexistent_order(client):
    """Ошибка: заказ не существует (несуществующий ID)"""
    response = await client.post(
        "/orders/create-item", json={"order_id": 999, "product_id": 1, "quantity": 1}
    )

    assert response.status_code == 404
    data = response.json()
    assert "Order not found" in data["detail"]


@pytest.mark.anyio
async def test_create_order_item_nonexistent_product(client):
    """Ошибка: товар не существует (несуществующий ID)"""
    response = await client.post(
        "/orders/create-item", json={"order_id": 1, "product_id": 999, "quantity": 1}
    )

    assert response.status_code == 404
    data = response.json()
    assert "Product not found" in data["detail"]


@pytest.mark.anyio
async def test_create_order_item_insufficient_stock(client):
    """Ошибка: недостаточно товара на складе"""
    # Ha складе 10 шт. товара 1. Пытаемся заказать 999
    response = await client.post(
        "/orders/create-item", json={"order_id": 1, "product_id": 1, "quantity": 999}
    )

    assert response.status_code == 400
