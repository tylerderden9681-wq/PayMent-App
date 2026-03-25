from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.repository import users as users_repository
from app.schemas import UserResponceSchema

def create_user(db: Session, login: str) -> UserResponceSchema:
    if users_repository.get_user(db, login):
        raise HTTPException(status_code=400, detail='Такой пользователь уже зарегистрирован!')


    user = users_repository.create_user(db, login)
    db.commit()
    return UserResponceSchema.model_validate(user)