from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Создаем приложение на FastAPI (Создаем экземпляр класса):
app = FastAPI()

# Словарь для хранения балансов кошельков:
# Ключ - название кошелька, значение - баланс

BALANCE = {'apple': 100}


# Объявим модель Pydantic для разделения операций доход и расхода:
class Operation(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None

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


# Так как мы уже написала body-запросы, самое время - написать ту же самую ручку с помощью path-запроса:
@app.post('/wallets/{name}')
def create_wallet(name: str, amount: float = 0):
    """Суть такая:
    1) Будем проверять, существует ли уже такой кошелёк
    1.1) Если да, то возвращаем код 400 (что-то пошло не так) с пояснением
    1.2) Если нет, то создаем его с переданным балансом
    2) В конце концов, возвращаем, что создание кошелька прошло успешно"""

    if name in BALANCE:
        raise HTTPException(status_code=400,
                            detail='Такой кошелёк уже есть')
    
    BALANCE[name] = amount

    return {'ok': True,
            'details': {
                'msg': 'Операция создания кошелька прошла успешно!',
                'balance': f'Текущий баланс на вашем счёте - {BALANCE[name]}'
            }}
    

# Сделаем 2 ручки: доход и расход

# 1) Доход:
@app.post('/operations/income')
def income_money(operation: Operation):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная
    3) Добавляем доход к балансу кошелька
    4) Возвращаем сообщение об успешной транзакции"""

    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} not found in DB')
    
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail='Balance is must be positive')
    
    BALANCE[operation.wallet_name] += operation.amount

    return {'ok': True,
            'msg': 'The transaction was successful'}


# 2) Расход:
@app.post('/operations/expense')
def expense_money(operation: Operation):
    """Логика такая:
    1) Проверяем, существует ли кошелёк
    2) Проверяем, что сумма положительная (вычитаемое)
    3) Проверяем, достаточно ли средств в кошельке
    4) Убавляем переданную сумму из баланса кошелька
    5) Возвращаем сообщение об успешной транзакции"""

    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f'Wallet {operation.wallet_name} is not defined')
    
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail=f'Balance is must be positive')
    
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(status_code=400, 
                            detail=f'Недостаточно средств. Доступные деньги: {BALANCE[operation.wallet_name]}')
    
    BALANCE[operation.wallet_name] -= operation.amount

    return {'ok': True, 'msg': 'The traksaktion is successfully'}