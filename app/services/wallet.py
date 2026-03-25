from fastapi import HTTPException
from app.schemas import CreateWalletSchema

from app.repository.wallet import (get_all_wallets,
                                   is_wallet_exist,
                                   get_wallet_balance_by_name,
                                    create_new_wallet1,
                                   )
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User


def get_balance(db: Session, current_user: User, wallet_name: str | None = None):

    # Логика такая:
    # Если имя кошелька не указано, то будет отображаться общий баланс
    if wallet_name is None:
        all_wallets = get_all_wallets(db, current_user.id, current_user.id)
        return {'total': sum(w.balance for w in all_wallets)}

    # Если имя указано, то проверяем, существует ли этот кошелёк
    # Если его не существует, то возвращать ошибку
    if not is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(status_code=404, detail='Кошелек с таким именем не найден!')

    # Если кошелек существует, то будем просто возвращать баланс этого кошелька
    wallet = get_wallet_balance_by_name(db, current_user.id, wallet_name)
    return {'wallet': wallet_name, 'balance': wallet.balance}


def create_new_wallet(db: Session, current_user: User, wallet: CreateWalletSchema):
    """Суть такая:
    1) Будем проверять, существует ли уже такой кошелёк
    1.1) Если да, то возвращаем код 400 (что-то пошло не так) с пояснением
    1.2) Если нет, то создаем его с переданным балансом
    2) В конце концов, возвращаем, что создание кошелька прошло успешно"""

    if is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(status_code=400,
                            detail='Такой кошелёк уже есть')
    
    wallet_1 = create_new_wallet1(db, current_user.id, wallet.name, wallet.initial_balance)
        
    db.commit()

    return {'ok': True,
            'details': {
                'msg': 'Операция создания кошелька прошла успешно!',
                'balance': f'Текущий баланс на вашем счёте - {wallet_1.balance}',
                'название кошелька': wallet.name if wallet.name else "Не указано",
        }}
    