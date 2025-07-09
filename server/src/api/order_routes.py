from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from src.models.order_model import Order
from src.database import get_db_session
from src.repositories.order_repository import OrderRepository

router = APIRouter()
# {"sku": true}


@router.post("/order")
def create_order(data: Dict[str, Any]):
    db = get_db_session()

    try:
        order = OrderRepository.create_order(
            db=db,
            order_data={
                "id": data.get("id"),
                "sku": data.get("sku"),
                "part_number": data.get("part_number"),
                "manufacturer": data.get("manufacturer"),
                "category": data.get("category"),
                "region": data.get("region"),
                "customer_id": data.get("customer_id"),
                "required_ship_date": datetime.strptime(data.get("required_ship_date"), "%Y-%m-%d").date(),
                "expected_delivery_date": datetime.strptime(data.get("expected_delivery_date"), "%Y-%m-%d").date(),
                "quantity": data.get("quantity"),
                "unit_price": data.get("unit_price"),
                "sale_price": data.get("sale_price"),
                "purchase_cost": data.get("purchase_cost"),
                "profit_margin_percentage": data.get("profit_margin_percentage"),
                "status": data.get("status"),
                "actual_delivery_date": (
                    datetime.strptime(data.get("actual_delivery_date"), "%Y-%m-%d").date()
                    if data.get("actual_delivery_date")
                    else None
                ),
            },
        )
        return {"message": "Order created successfully", "order": order.to_dict()}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@router.get("/order/{order_id}")
def get_order_by_id(order_id: str):
    db = get_db_session()

    print(f"Order id: {order_id}")

    try:
        order = OrderRepository.get_order_by_id(db, order_id)
        if order:
            return {"message": "Order filtered succesfully", "order": order.to_dict()}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@router.get("/order")
def get_orders():
    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db)
        return {
                "message": "Orders retrieved successfully",
                "orders": [order.to_dict() for order in orders]
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()