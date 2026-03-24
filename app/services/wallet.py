from fastapi import HTTPException
from app.schemas import CreateWalletSchema

from app.repository.wallet import (get_all_wallets,
                                   is_wallet_exist,
                                   get_wallet_balance_by_name,
                                    create_new_wallet1,
                                   )


def get_balance(wallet_name: str | None = None):
    # Логика такая:
    # Если имя кошелька не указано, то будет отображаться общий баланс
    if wallet_name is None:
        all_wallets = get_all_wallets()
        return {'total': sum(all_wallets.values())}

    # Если имя указано, то проверяем, существует ли этот кошелёк
    # Если его не существует, то возвращать ошибку
    if not is_wallet_exist(wallet_name):
        raise HTTPException(status_code=404, detail='Кошелек с таким именем не найден!')

    # Если кошелек существует, то будем просто возвращать баланс этого кошелька
    current_balance = get_wallet_balance_by_name(wallet_name)
    return {'wallet': wallet_name, 'balance': current_balance}


def create_new_wallet(wallet: CreateWalletSchema):
    """Суть такая:
    1) Будем проверять, существует ли уже такой кошелёк
    1.1) Если да, то возвращаем код 400 (что-то пошло не так) с пояснением
    1.2) Если нет, то создаем его с переданным балансом
    2) В конце концов, возвращаем, что создание кошелька прошло успешно"""

    print(f"Received wallet: {wallet}")  # ← добавить
    print(f"Wallet name: {wallet.name}")  # ← добавить
    print(f"Wallet initial_balance: {wallet.initial_balance}")  # ← добавить


    if is_wallet_exist(wallet.name):
        raise HTTPException(status_code=400,
                            detail='Такой кошелёк уже есть')
    
    balance = create_new_wallet1(wallet.name, wallet.initial_balance)

    return {'ok': True,
            'details': {
                'msg': 'Операция создания кошелька прошла успешно!',
                'balance': f'Текущий баланс на вашем счёте - {balance}',
                'название кошелька': wallet.name if wallet.name else "Не указано",
            }}