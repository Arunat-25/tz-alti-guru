from pydantic import BaseModel


class OrderItem(BaseModel):
    pass


class OrderItemCreate(OrderItem):
    order_id: int
    product_id: int
    quantity: int
