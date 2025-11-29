from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CurrencyUnitAPI"
    ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./data.db"
    EXCHANGE_RATE_API_URL: str = "https://api.exchangerate.host/latest"
    EXCHANGE_RATE_CACHE_TTL: int = 600  # seconds
    API_KEY_HEADER_NAME: str = "X-API-Key"
    API_KEY: str = "changeme"
    
    class Config:
        env_file = ".env"

settings = Settings()
