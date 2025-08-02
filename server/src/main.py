from fastapi import FastAPI
from .api.order_routes import order_router
from .database import get_db_session, init_db
from .repositories.order_repository import OrderRepository
from .api.stats_models_routes import stats_models_router





init_db()

app = FastAPI(title="prediction-system API")
# Montar rutas
app.include_router(order_router, prefix="/api/v1/order", tags=["orders"])
app.include_router(stats_models_router, prefix="/api/v1/stats-models", tags=["stats"])