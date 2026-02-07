from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.exceptions import OrderNotFound
from src.orders.schemas import OrderItemCreate
from src.products.crud import decrease_product_quantity, get_product
from src.products.exceptions import InsufficientProductQuantity


async def is_order_exist(order_id: int, session: AsyncSession) -> bool:
    query = "SELECT id \
             FROM orders \
             WHERE id = :order_id"
    result = await session.execute(text(query), {"order_id": order_id})
    order = result.scalar_one_or_none()
    if order:
        return True
    return False


async def create_order_item(data: OrderItemCreate, session: AsyncSession):
    # проверка на существование заказа
    if not await is_order_exist(order_id=data.order_id, session=session):
        raise OrderNotFound("Order not found")

    # проверка на количество товара
    product = await get_product(product_id=data.product_id, session=session)
    if product["quantity"] < data.quantity:
        raise InsufficientProductQuantity(
            f"Available: {product.quantity}, requested: {data.quantity}"
        )

    # проверка есть ли уже товар в заказе
    query = "SELECT id \
             FROM order_items \
             WHERE order_id = :order_id AND product_id = :product_id"
    result = await session.execute(
        text(query), {"order_id": data.order_id, "product_id": data.product_id}
    )
    order_item = result.scalar_one_or_none()
    if order_item:
        # если есть товар в заказе, то увеличиваем количество товара
        query = "UPDATE order_items \
                 SET quantity = quantity + :quantity \
                 WHERE order_id = :order_id AND product_id = :product_id \
                 RETURNING *"
        result = await session.execute(
            text(query),
            {
                "quantity": data.quantity,
                "order_id": data.order_id,
                "product_id": data.product_id,
            },
        )
    else:
        # если товара в заказе нет, то добавляем
        query = "INSERT INTO order_items (order_id, product_id, quantity, price_at_order) \
                 VALUES (:order_id, :product_id, :quantity, :price_at_order) \
                 RETURNING *"
        result = await session.execute(
            text(query),
            {
                "order_id": data.order_id,
                "product_id": data.product_id,
                "quantity": data.quantity,
                "price_at_order": product["price"],
            },
        )

    # уменьшаем количество товара на складе
    await decrease_product_quantity(
        product_id=data.product_id, quantity=data.quantity, session=session
    )

    await session.commit()

    raw = result.fetchone()
    created_order_item = {
        "order_item_id": raw[0],
        "order_id": raw[1],
        "product_id": raw[2],
        "quantity": raw[3],
        "price_at_order": raw[4],
    }
    return created_order_item
