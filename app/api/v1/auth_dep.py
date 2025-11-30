from fastapi import Header, HTTPException, status
from typing import Optional

from app.core.config import settings
from app.db.crud import get_api_key, increment_usage
from app.core.logger import logger

def api_key_dependency(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    rapidapi_key: Optional[str] = Header(None, alias="x-rapidapi-key")
):
    """
    Dependency to validate API keys.
    Accepts BOTH:
    - X-API-Key       (normal usage)
    - x-rapidapi-key  (RapidAPI)
    """

    # Prefer normal X-API-Key but fallback to x-rapidapi-key
    api_key_value = x_api_key or rapidapi_key

    if not api_key_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )

    key = get_api_key(api_key_value)

    if key is None or not key.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )

    # Increment usage counter safely
    try:
        increment_usage(key)
    except Exception:
        logger.exception("Failed to increment usage for key: %s", getattr(key, 'key', None))

    return key
