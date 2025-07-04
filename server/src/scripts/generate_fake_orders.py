# server/scripts/generate_fake_orders.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

NUM_ORDERS = 1_000_000
SKUS = [f"SKU{str(i).zfill(4)}" for i in range(50)]
PART_NUMBERS = [f"PN-{i:05d}" for i in range(50)]
REGIONS = ["North America", "Europe", "Asia", "South America"]
CATEGORIES = ["Chip", "Connector", "Sensor", "Transistor", "Memory"]
MANUFACTURERS = ["Intel", "Texas Instruments", "NXP", "Infineon", "STMicroelectronics", "Microchip", "Analog Devices"]

def generate_fake_data(n=NUM_ORDERS):
    data = []
    base_date = datetime(2023, 1, 1)

    for i in range(n):
        order_id = f"ORD{100000 + i}"
        sku = random.choice(SKUS)
        part_number = random.choice(PART_NUMBERS)
        manufacturer = random.choice(MANUFACTURERS)
        category = random.choice(CATEGORIES)
        region = random.choice(REGIONS)
        customer_id = f"CUST{random.randint(1000, 1100)}"

        order_date = base_date + timedelta(days=random.randint(0, 500))
        expected_delivery = order_date + timedelta(days=random.randint(5, 15))
        required_ship_date = expected_delivery - timedelta(days=random.randint(1, 3))  # cliente requiere embarque un poco antes

        # Simular retrasos
        delay_chance = np.random.rand()
        if delay_chance < 0.75:
            actual_delivery = expected_delivery
            status = "on_time"
        elif delay_chance < 0.9:
            actual_delivery = expected_delivery + timedelta(days=random.randint(1, 5))
            status = "late"
        else:
            actual_delivery = expected_delivery + timedelta(days=random.randint(6, 15))
            status = "very_late"

        quantity = random.randint(10, 500)
        unit_price = round(random.uniform(0.5, 50.0), 2)
        sale_price = round(quantity * unit_price, 2)

        purchase_cost_unit = round(unit_price * random.uniform(0.6, 0.9), 2)
        purchase_cost = round(purchase_cost_unit * quantity, 2)

        margin = round(((sale_price - purchase_cost) / sale_price) * 100, 2) if sale_price else 0.0

        data.append({
            "order_id": order_id,
            "sku": sku,
            "part_number": part_number,
            "manufacturer": manufacturer,
            "category": category,
            "region": region,
            "customer_id": customer_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "required_ship_date": required_ship_date.strftime("%Y-%m-%d"),
            "expected_delivery": expected_delivery.strftime("%Y-%m-%d"),
            "actual_delivery": actual_delivery.strftime("%Y-%m-%d"),
            "quantity": quantity,
            "unit_price": unit_price,
            "sale_price": sale_price,
            "purchase_cost": purchase_cost,
            "profit_margin_percent": margin,
            "status": status,
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_fake_data()
    df.to_csv("fake_orders.csv", index=False)
    print("✅ File 'fake_orders.csv' successfuly created")
