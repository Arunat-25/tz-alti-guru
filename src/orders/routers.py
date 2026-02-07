from fastapi import APIRouter
from fastapi.params import Depends

from src.database.session import get_session
from src.orders import crud
from src.orders.schemas import OrderItemCreate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/create-item")
async def create_order_item(data: OrderItemCreate, session=Depends(get_session)):
    created_order_item = await crud.create_order_item(data=data, session=session)
    return created_order_item
