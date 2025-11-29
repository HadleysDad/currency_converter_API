from sqlmodel import Session, select, SQLModel
from app.db.session import engine
from app.db.models import APIKey
from app.core.logger import logger

def init_db():
    SQLModel.metadata.create_all(engine)
    logger.info("DB tables ensured.")

def get_api_key(key: str) -> APIKey | None:
    with Session(engine) as session:
        stmt = select(APIKey).where(APIKey.key == key)
        result = session.exec(stmt).first()
        return result

def increment_usage(key: APIKey):
    with Session(engine) as session:
        db_key = session.get(APIKey, key.key)
        if not db_key:
            logger.warning("Tried to increment usage for key that doesn't exist: %s", key.key)
            return
        db_key.requests_made += 1
        session.add(db_key)
        session.commit()
