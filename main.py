from fastapi import FastAPI, HTTPException


# Создаем приложение на FastAPI (Создаем экземпляр класса):
app = FastAPI()

# Словарь для хранения балансов кошельков:
# Ключ - название кошелька, значение - баланс

BALANCE = {'apple': 100}

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
def recieve_money(name: str, amount: int):
    # Если кошелька с таким именем нет, то создаем новый кошелёк с таким именем и с балансом 0
    if name not in BALANCE:
        BALANCE[name] = 0
    # Если есть - добавляем amount к балансу указанного кошелька
    BALANCE[name] += amount
    # И обязательно возвращаем информацию о завершении операции
    return {
        'ok': True,
        'msg': 'Транзакция прошла успешно!',
        'details': {
            'detail': f'Added {amount} to {name}',
            'wallet': name,
            'past_balance': BALANCE[name] - amount,
            'new_balance': BALANCE[name]
        }
    }
    