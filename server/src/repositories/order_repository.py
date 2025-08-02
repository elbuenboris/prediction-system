from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time, date
from typing import List
from ..models.order_model import Order
from typing import Optional
from datetime import date, time



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

    # @staticmethod
    # def get_orders(db: Session, limit: int = 20, status: str = "on_time") -> List[Order]:
    #     try:
    #         orders = db.query(Order).filter(Order.status == status).limit(limit).all()

    #         return orders
    #     except Exception as e:
    #         print(f"Error retrieving orders: {e}")
    #         raise


    # @staticmethod
    # def get_orders(
    #     db: Session,
    #     limit: int = 20,
    #     status: str = "on_time",
    #     start_date: Optional[date] = None,
    #     end_date: Optional[date] = None
    # ) -> List[Order]:
    #     try:
    #         query = db.query(Order).filter(Order.status == status)

    #         if start_date:
    #             start_datetime = datetime.combine(start_date, time.min)  # 00:00:00
    #             query = query.filter(Order.required_ship_date >= start_datetime)

    #         if end_date:
    #             end_datetime = datetime.combine(end_date, time.max)  # 23:59:59.999999
    #             query = query.filter(Order.required_ship_date <= end_datetime)

    #         query = query.order_by(Order.required_ship_date.asc())
            
    #         orders = query.limit(limit).all()
    #         return orders
    #     except Exception as e:
    #         print(f"Error retrieving orders: {e}")
    #         raise

    @staticmethod
    def get_orders(
        db: Session,
        limit: int = 100,
        status: str = "on_time",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        region: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Order]:
        try:
            query = db.query(Order).filter(Order.status == status)
            print("Filtered by status:", query.count())

            if region:
                query = query.filter(func.lower(Order.region) == region.lower())
                print("Filtered by region:", query.count())
                
            query = query.filter(Order.profit_margin_percentage > 30)
            print("Filtered by margin < 50:", query.count())
            
            if category:
                query = query.filter(func.lower(Order.category) == category.lower())
                print("Filtered by category", query.count())

            # query = query.filter(Order.actual_delivery_date != None)
            # query = query.filter(
            #     func.strftime('%m', Order.actual_delivery_date) == "07",
            #     func.strftime('%Y', Order.actual_delivery_date) == "2023"
            # )
            # print("Filtered by delivery date (Jul 2024):", query.count())
            query = query.filter(Order.actual_delivery_date != None)

            if start_date:
                start_datetime = datetime.combine(start_date, time.min)
                query = query.filter(Order.actual_delivery_date >= start_datetime)
                print("Filtered by start_date:", query.count())

            if end_date:
                end_datetime = datetime.combine(end_date, time.max)
                query = query.filter(Order.actual_delivery_date <= end_datetime)
                print("Filtered by end_date:", query.count())

            query = query.order_by(Order.actual_delivery_date.asc())\
            
            return query.limit(limit).all()
            #return query.all() 

        except Exception as e:
            print(f"Error retrieving orders: {e}")
            raise
        
        #     if start_date:
        #         start_datetime = datetime.combine(start_date, time.min)
        #         query = query.filter(Order.required_ship_date >= start_datetime)

        #     if end_date:
        #         end_datetime = datetime.combine(end_date, time.max)
        #         query = query.filter(Order.required_ship_date <= end_datetime)
            
        #     if region:
        #         query = query.filter(Order.region == region)

        #     # Margen de ganancia < 50
        #     query = query.filter(Order.profit_margin_percentage < 50)

        #     # Fecha de entrega real: julio 2024 (compat. con SQLite)
        #     query = query.filter(
        #         func.strftime('%m', Order.actual_delivery_date) == "07",
        #         func.strftime('%Y', Order.actual_delivery_date) == "2024"
        #     )

        #     # Ordenar por fecha de entrega requerida
        #     query = query.order_by(Order.actual_delivery_date.asc())

        #     orders = query.limit(limit).all()
        #     return orders

        # except Exception as e:
        #     print(f"Error retrieving orders: {e}")
        #     raise


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
