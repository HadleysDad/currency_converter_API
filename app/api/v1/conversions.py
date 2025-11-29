from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.v1.auth_dep import api_key_dependency
from app.services.unit_service import convert_unit
from app.services.currency_service import convert_currency
from app.core.logger import logger

router = APIRouter(prefix="/v1/convert", tags=["convert"])

class UnitRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

class CurrencyRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

@router.post("/unit")
async def unit_convert(req: UnitRequest, key=Depends(api_key_dependency)):
    try:
        out = convert_unit(req.value, req.from_unit, req.to_unit)
        logger.info("unit conversion success: %s %s -> %s", req.value, req.from_unit, req.to_unit)
        return {"ok": True, "value": out}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/currency")
async def currency_convert(req: CurrencyRequest, key=Depends(api_key_dependency)):
    try:
        out = convert_currency(req.amount, req.from_currency, req.to_currency)
        logger.info("currency conversion success: %s %s -> %s", req.amount, req.from_currency, req.to_currency)
        return {"ok": True, "value": out}
    except Exception as e:
        logger.exception("currency conversion failed")
        raise HTTPException(status_code=500, detail="rate fetch failed")
