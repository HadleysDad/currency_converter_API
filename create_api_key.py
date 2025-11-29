from sqlmodel import Session
from app.db.session import engine
from app.db.models import APIKey
import secrets

def create_key(owner: str):
    key = secrets.token_hex(16)
    with Session(engine) as session:
        api_key = APIKey(key=key, owner=owner)
        session.add(api_key)
        session.commit()
        session.refresh(api_key)
        print("Created API key:", api_key.key)

if __name__ == "__main__":
    owner_name = input("Enter owner name: ")
    create_key(owner_name)