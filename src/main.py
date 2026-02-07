import uvicorn
from fastapi import FastAPI

from src.orders.exceptions import OrderNotFound, order_not_found_handler
from src.orders.routers import router as orders_router
from src.products.exceptions import (
    InsufficientProductQuantity,
    ProductNotFound,
    insufficient_quantity_handler,
    product_not_found_handler,
)

app = FastAPI()


app.add_exception_handler(OrderNotFound, order_not_found_handler)
app.add_exception_handler(ProductNotFound, product_not_found_handler)
app.add_exception_handler(InsufficientProductQuantity, insufficient_quantity_handler)


app.include_router(orders_router)


@app.get("/")
async def say_hello():
    return "Hello, Aiti Guru!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
