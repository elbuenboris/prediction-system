from fastapi import FastAPI
from src.api.routes import router as api_router
from src.api.prediction_routes import router as prediction_router

app = FastAPI(title="prediction-system API")

# Montar rutas
app.include_router(api_router)
app.include_router(prediction_router)
