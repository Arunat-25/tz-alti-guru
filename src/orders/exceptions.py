from fastapi import Request, status
from fastapi.responses import JSONResponse


class OrderNotFound(Exception):
    def __init__(self, message: str = "Order not found"):
        self.message = message
        super().__init__(self.message)


async def order_not_found_handler(request: Request, exc: OrderNotFound):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message})
