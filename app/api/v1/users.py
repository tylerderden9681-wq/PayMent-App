# Этот модуль будет отвечать за router с доменом users, т.е. будет предназначен для работы с 
# пользователями

from fastapi import APIRouter, Depends
from app.schemas import UserAddSchema, UserResponceSchema
from app.services import users as users_service 
from app.models import User
from sqlalchemy.orm import Session
from app.dependency import get_db, get_current_user_dep

router = APIRouter()

@router.post('/users', response_model=UserResponceSchema)
def create_user(payload: UserAddSchema, db: Session = Depends(get_db)):
    return users_service.create_user(db, payload.login)


# А теперь добавим endpoint, который будет проверять авторизацию пользователей. 
# Такой endpoint называется 'get_users/me'. /me означает, что авторизация происходит по токену и 
# мы не указываем конкретного пользователя, а берем его из токена
# Задача такого эндпоинта показать, что авторизация работает, и работает корректно
@router.get('/users/me')
def get_current_user(current_user: User = Depends(get_current_user_dep)):
    return UserResponceSchema.model_validate(current_user)