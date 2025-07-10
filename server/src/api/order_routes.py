from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from ..repositories.order_repository import OrderRepository
from ..database import get_db_session
from ..helpers.order_helper import generate_dummy_orders

order_router = APIRouter()


@order_router.post("/")
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


@order_router.get("/{order_id}")
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


@order_router.get("/")
def get_orders(status: str = None, limit: int = None):
    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db, limit, status)
        return {"message": "Orders retrieved successfully", "orders": [order.to_dict() for order in orders]}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@order_router.post("/preload-database")
def preload_database(status: str, customer_id: str):
    # checar si customer_id existe
    # is_valid = checkIfIdExists(customer_id)
    # if is_valid == false:
    db = get_db_session()

    try:
        dummy_orders = generate_dummy_orders()
        current_db_orders = OrderRepository.get_orders(db)
        message = ""

        if len(current_db_orders) == 0:
            orders = OrderRepository.create_many_orders(db, dummy_orders)
            message = f"✅ {len(orders)} orders added to database."

        else:
            message = "Database already has data."

        return {"message": message}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
