from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..models.order_model import Order


class OrderRepository:
    @staticmethod
    def create_order(db: Session, order_data: dict) -> Order:
        try:
            # Crear una nueva orden
            order = Order(
                id=order_data.get("id"),
                sku=order_data.get("sku"),
                part_number=order_data.get("part_number"),
                manufacturer=order_data.get("manufacturer"),
                category=order_data.get("category"),
                region=order_data.get("region"),
                customer_id=order_data.get("customer_id"),
                order_date=datetime.now(),
                required_ship_date=order_data.get("required_ship_date"),
                expected_delivery_date=order_data.get("expected_delivery_date"),
                actual_delivery_date=order_data.get("actual_delivery_date"),
                quantity=order_data.get("quantity"),
                unit_price=order_data.get("unit_price"),
                sale_price=order_data.get("sale_price"),
                purchase_cost=order_data.get("purchase_cost"),
                profit_margin_percentage=order_data.get("profit_margin_percentage"),
                status=order_data.get("status"),
            )
            db.add(order)
            db.commit()
            db.refresh(order)

            return order
        except Exception as e:
            db.rollback()
            print(f"Error creating order: {e}")
            raise

    @staticmethod
    def get_orders(db: Session, limit: int = 20, status: str = "on_time") -> List[Order]:
        try:
            orders = db.query(Order).filter(Order.status == status).limit(limit).all()

            return orders
        except Exception as e:
            print(f"Error retrieving orders: {e}")
            raise

    @staticmethod
    def get_order_by_id(db: Session, order_id: str) -> Order:
        try:
            # Obtener una orden por su ID
            order = db.query(Order).filter(Order.id == order_id).first()
            print(f"order: {order}")
            return order
        except Exception as e:
            print(f"Error retrieving order by ID: {e}")
            raise

    @staticmethod
    def create_many_orders(db: Session, orders_data: List[dict]):
        try:
            orders = [Order(**order_data) for order_data in orders_data]

            db.add_all(orders)
            db.commit()

            return orders
        except Exception as e:
            db.rollback()
            print(f"Error bulk writing orders: {e}")
            raise
