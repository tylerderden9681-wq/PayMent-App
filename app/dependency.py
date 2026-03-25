from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

from app.repository import users as users_repository

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


def get_current_user_dep(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)) -> User:
    login = credentials.credentials

    user = users_repository.get_user(db, login)

    if not user:
        # Здесь мы проверяем, нашелся ли пользователь. Если нет, то по стандартам HTTP 
        # должен прийти 401 код, который говорит, что пользователь не авторизован
        raise HTTPException(status_code=401, detail='Пользователь не авторизован')
    
    # Если пользователь найден, то просто вернём его:
    return user