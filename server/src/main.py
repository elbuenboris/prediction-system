from fastapi import FastAPI
from .api.order_routes import router as order_router
from .database import init_db, get_db_session
from .repositories.order_repository import OrderRepository
from datetime import datetime

init_db()
db = get_db_session()

try:
    orders = OrderRepository.get_orders(db=db)
    print(f"Orders number: {len(orders)}")
    for order in orders:
        print(f"{order}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()


app = FastAPI(title="prediction-system API")

# Montar rutas
app.include_router(order_router, prefix="/api/v1", tags=["orders"])
