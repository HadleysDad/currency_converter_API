import httpx
import time
from typing import Tuple
from app.core.config import settings
from app.core.logger import logger

_cached_rates: dict = {}
_cached_at: float = 0.0

def _fetch_rates() -> Tuple[dict, str]:
    url = settings.EXCHANGE_RATE_API_URL
    resp = httpx.get(url, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()
    rates = data.get("rates", {})
    base = data.get("base", "EUR")
    return rates, base

def _get_rates() -> Tuple[dict, str]:
    global _cached_rates, _cached_at
    ttl = settings.EXCHANGE_RATE_CACHE_TTL
    now = time.time()
    if not _cached_rates or (now - _cached_at) > ttl:
        try:
            rates, base = _fetch_rates()
            _cached_rates = {"rates": rates, "base": base}
            _cached_at = now
            logger.info("Fetched fresh exchange rates")
        except Exception:
            logger.exception("Failed to fetch exchange rates; using last cached rates if available")
            if not _cached_rates:
                raise
    return _cached_rates.get("rates", {}), _cached_rates.get("base", "EUR")

def convert_currency(amount: float, from_cur: str, to_cur: str) -> float:
    rates, base = _get_rates()
    f = from_cur.upper()
    t = to_cur.upper()

    if f == t:
        return amount

    # Normalize: convert source -> base -> target
    if f == base:
        intermediate = amount
    else:
        if f not in rates:
            raise ValueError(f"Unsupported currency: {f}")
        intermediate = amount / rates[f]

    if t == base:
        return intermediate

    if t not in rates:
        raise ValueError(f"Unsupported currency: {t}")

    return intermediate * rates[t]
