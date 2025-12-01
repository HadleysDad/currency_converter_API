from fastapi import Header, HTTPException, status
from typing import Optional

from app.core.logger import logger

def api_key_dependency(
    rapidapi_key: Optional[str] = Header(None, alias="X-RapidAPI-Key")
):
    """
    Accept ONLY RapidAPI authentication.
    Internal API keys (X-API-Key) are disabled.
    """
    
    if not rapidapi_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
    
    # You can add logging here if desired
    logger.info(f"RapidAPI key used: {rapidapi_key[:6]}...")

    return {"key": rapidapi_key, "source": "rapidapi"}
