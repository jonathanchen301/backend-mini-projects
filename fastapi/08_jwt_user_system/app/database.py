from app.models import UserInDB

users_db: dict[str, UserInDB] = {}

def get_user(username:str) -> UserInDB | None:
    return users_db.get(username)