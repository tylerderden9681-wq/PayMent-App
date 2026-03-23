from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


# Создаем приложение на FastAPI (Создаем экземпляр класса):
app = FastAPI()

# Словарь для хранения балансов кошельков:
# Ключ - название кошелька, значение - баланс

BALANCE = {'apple': 100}


# Объявим модель Pydantic для разделения операций доход и расхода:
class OperationSchema(BaseModel):
    # Ограничим ввод некоторых данных с помощью валидации данных в Pydantic:
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None,  max_length=255)

    # Чтобы ограничить поле amount используем функцию field_validator как декоратор:
    # Это валидатор, что сумма положительная
    @field_validator('amount')
    def amount_must_be_positive(cls, value: float) -> float:
        # Логика такая: нам нужно проверить, что amount >= 0 и возвратить значение если всё ок
        if value < 0:
            raise HTTPException(status_code=400, detail='Amount must be positive or null')
        
        return value
    
    # Нам также важно, чтобы пользователь не передавал только пробелы, иначе это будет некорректно
    # Так что обработаем и это с помощью валидатора:
    @field_validator('wallet_name')
    def wallet_name_is_not_empty(cls, name: str) -> str:
        # Убираем пробелы по краям с помощью .strip() и проверяем, не пуста ли строка:
        clean_str = name.strip()

        if not clean_str:
            raise HTTPException(status_code=400, detail='У кошелька должно быть свое имя, а не пробелы!!!')

    

# Здесь мы указываем body-запросы, то есть, если мы заходим написать это в браузере,
# то это будем выглядеть так: localhost:8000/balance?wallet_name=...
@app.get('/balance')
def get_balance(wallet_name: str | None = None):
    # Логика такая:
    # Если имя кошелька не указано, то будет отображаться общий баланс
    if wallet_name is None:
        return {'total': sum(BALANCE.values())}

    # Если имя указано, то проверяем, существует ли этот кошелёк
    # Если его не существует, то возвращать ошибку
    if wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail='Кошелек с таким именем не найден!')

    # Если кошелек существует, то будем просто возвращать баланс этого кошелька
    return {'wallet': wallet_name, 'balance': BALANCE[wallet_name]}


class CreateWalletSchema(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float

    # Чтобы ограничить поле amount используем функцию field_validator как декоратор:
    # Нам также важно, чтобы пользователь не передавал только пробелы, иначе это будет некорректно
    # Так что обработаем и это с помощью валидатора:
    @field_validator('name')
    def wallet_name_is_not_empty(cls, name: str) -> str:
        # Убираем пробелы по краям с помощью .strip() и проверяем, не пуста ли строка:
        clean_str = name.strip()

        if not clean_str:
            raise HTTPException(status_code=400, detail='У кошелька должно быть свое имя, а не пробелы!!!')

    # Это валидатор, что сумма положительная
    @field_validator('initial_balance')
    def amount_must_be_positive(cls, value: float) -> float:
        # Логика такая: нам нужно проверить, что amount >= 0 и возвратить значение если всё ок
        if value < 0:
            raise ValueError("Initial balanse shouldn't be negative")
        
        return value


# Так как мы уже написала body-запросы, самое время - написать ту же самую ручку с помощью path-запроса:
@app.post('/wallets')
def create_wallet(wallet: CreateWalletSchema):
    """Суть такая:
    1) Будем проверять, существует ли уже такой кошелёк
    1.1) Если да, то возвращаем код 400 (что-то пошло не так) с пояснением
    1.2) Если нет, то создаем его с переданным балансом
    2) В конце концов, возвращаем, что создание кошелька прошло успешно"""

    if wallet.name in BALANCE:
        raise HTTPException(status_code=400,
                            detail='Такой кошелёк уже есть')
    
    BALANCE[wallet.name] = wallet.initial_balance

    return {'ok': True,
            'details': {
                'msg': 'Операция создания кошелька прошла успешно!',
                'balance': f'Текущий баланс на вашем счёте - {BALANCE[wallet.name]}'
            }}
    

# Сделаем 2 ручки: доход и расход

# 1) Доход:
@app.post('/operations/income')
def income_money(operation: OperationSchema):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная
    3) Добавляем доход к балансу кошелька
    4) Возвращаем сообщение об успешной транзакции"""

    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} not found in DB')
    
    BALANCE[operation.wallet_name] += operation.amount

    return {'ok': True,
            'msg': 'The transaction was successful'}


# 2) Расход:
@app.post('/operations/expense')
def expense_money(operation: OperationSchema):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная (вычитаемое)
    3) Проверяем, достаточно ли средств в кошельке
    4) Убавляем переданную сумму из баланса кошелька
    5) Возвращаем сообщение об успешной транзакции"""

    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} is not defined')
    
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(status_code=400, 
                            detail=f'Недостаточно средств. Доступные деньги: {BALANCE[operation.wallet_name]}')
    
    BALANCE[operation.wallet_name] -= operation.amount

    return {'ok': True, 'msg': 'The traksaktion is successfully'}