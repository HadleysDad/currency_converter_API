from fastapi import Header, HTTPException, status
from app.core.config import settings
from app.db.crud import get_api_key, increment_usage
from app.core.logger import logger

def api_key_dependency(x_api_key: str | None = Header(None, alias="X-API-Key")):
    """Dependency to validate X-API-Key header and increment usage."""
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing API Key")

    key = get_api_key(x_api_key)
    if key is None or not key.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid API Key")

    try:
        increment_usage(key)
    except Exception:
        logger.exception("Failed to increment usage for key: %s", getattr(key, 'key', None))

    return key
