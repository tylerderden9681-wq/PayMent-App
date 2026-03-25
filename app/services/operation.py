from fastapi import HTTPException
from app.schemas import OperationSchema
from app.repository.wallet import (is_wallet_exist, 
                                   add_income, 
                                   get_wallet_balance_by_name, 
                                   add_extend)
from app.database import SessionLocal
from sqlalchemy.orm import Session

from app.models import User


def income_money(db: Session, current_user: User, operation: OperationSchema):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная
    3) Добавляем доход к балансу кошелька
    4) Возвращаем сообщение об успешной транзакции"""
    
    if not is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} not found in DB')
    
    wallet = add_income(db, current_user.id, operation.wallet_name, operation.amount)

    db.commit()

    return {'ok': True, 'details': {
        'msg': 'The traksaktion is successfully',
        'income': operation.amount,
        'new_balance': wallet.balance,
        'description': operation.description,
        }
    }


def expense_money(db: Session, current_user: User, operation: OperationSchema):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная (вычитаемое)
    3) Проверяем, достаточно ли средств в кошельке
    4) Убавляем переданную сумму из баланса кошелька
    5) Возвращаем сообщение об успешной транзакции"""

    
    if not is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} is not defined')
    
    wallet = get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)

    if wallet.balance < operation.amount:
        raise HTTPException(status_code=400, 
                            detail=f'Недостаточно средств. Доступные деньги: {wallet.balance}')
    
    new_balance = add_extend(db, current_user.id, operation.wallet_name, operation.amount)

    db.commit()
        
    return {'ok': True, 'details': {
        'msg': 'The traksaktion is successfully',
        'expense': operation.amount,
        'new_balance': new_balance,
        'description': operation.description,
        }
    }