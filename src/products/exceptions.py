from fastapi import Request, status
from fastapi.responses import JSONResponse


class ProductNotFound(Exception):
    def __init__(self, message: str = "Product not found"):
        self.message = message
        super().__init__(self.message)


class InsufficientProductQuantity(Exception):
    def __init__(self, message: str = "Insufficient product quantity"):
        self.message = message
        super().__init__(self.message)


async def product_not_found_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message})


async def insufficient_quantity_handler(request: Request, exc: InsufficientProductQuantity):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.message})
