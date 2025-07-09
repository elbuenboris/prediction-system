from sqlalchemy import Column, Integer, String, DateTime, Float
from src.database import Base

from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    sku = Column(String(10), nullable=False)
    part_number = Column(String(10), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    required_ship_date = Column(DateTime, nullable=False)
    expected_delivery_date = Column(DateTime, nullable=False)
    actual_delivery_date = Column(DateTime, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    profit_margin_percentage = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return (
            f"<Order(id={self.id}, sku={self.sku}, part_number={self.part_number}, "
            f"manufacturer={self.manufacturer}, category={self.category}, region={self.region}, "
            f"customer_id={self.customer_id}, order_date={self.order_date}, "
            f"required_ship_date={self.required_ship_date}, expected_delivery_date={self.expected_delivery_date}, "
            f"actual_delivery_date={self.actual_delivery_date}, quantity={self.quantity}, "
            f"unit_price={self.unit_price}, sale_price={self.sale_price}, purchase_cost={self.purchase_cost}, "
            f"profit_margin_percentage={self.profit_margin_percentage}, status={self.status})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "part_number": self.part_number,
            "manufacturer": self.manufacturer,
            "category": self.category,
            "region": self.region,
            "customer_id": self.customer_id,
            "order_date": self.order_date.isoformat(),
            "required_ship_date": self.required_ship_date.isoformat(),
            "expected_delivery_date": self.expected_delivery_date.isoformat(),
            "actual_delivery_date": self.actual_delivery_date.isoformat(),
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "sale_price": self.sale_price,
            "purchase_cost": self.purchase_cost,
            "profit_margin_percentage": self.profit_margin_percentage,
            "status": self.status,
        }
