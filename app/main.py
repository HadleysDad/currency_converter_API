from fastapi import FastAPI
from app.api.v1.conversions import router as conv_router
from app.db.crud import init_db
from app.core.logger import logger


app = FastAPI(title="Currency & Unit Conversion API", version="1.0.0")
app.include_router(conv_router)

@app.on_event("startup")
def on_startup():
    # Initialize DB (creates tables if not present)
    init_db()
    logger.info("DB initialized and application startup complete")

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}
