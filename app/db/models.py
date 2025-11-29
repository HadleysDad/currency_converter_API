from sqlmodel import SQLModel, Field
from datetime import datetime

class APIKey(SQLModel, table=True):
    key: str = Field(primary_key=True)
    owner: str
    active: bool = True
    requests_made: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
