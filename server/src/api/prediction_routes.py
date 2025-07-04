from fastapi import APIRouter

router = APIRouter()

@router.get("/prediction/order")
def order():
    return {"message": "order"}

@router.get("/prediction/receipt")
def receipt():
    return {"message": "receipt"}

