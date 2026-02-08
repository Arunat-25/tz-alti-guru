from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.exceptions import ProductNotFound


async def get_product(product_id: int, session: AsyncSession):
    query = "SELECT * \
             FROM products \
             WHERE id = :product_id \
             FOR UPDATE"
    result = await session.execute(text(query), {"product_id": product_id})
    product = result.mappings().fetchone()
    if not product:
        raise ProductNotFound("Product not found")
    return product


async def decrease_product_quantity(product_id: int, quantity: int, session: AsyncSession):
    query = "UPDATE products \
             SET quantity = quantity - :quantity \
             WHERE id = :product_id \
             RETURNING *"
    result = await session.execute(text(query), {"product_id": product_id, "quantity": quantity})
    product = result.mappings().fetchone()
    if not product:
        # Либо товар не найден, либо недостаточно остатка
        return None
    return product
