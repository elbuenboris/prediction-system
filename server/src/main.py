from fastapi import FastAPI
from .api.order_routes import order_router
from .database import get_db_session, init_db
from .repositories.order_repository import OrderRepository

init_db()

app = FastAPI(title="prediction-system API")
# Montar rutas
app.include_router(order_router, prefix="/api/v1/order", tags=["orders"])
