from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

# Объявим модель Pydantic для разделения операций доход и расхода:
class OperationSchema(BaseModel):
    # Ограничим ввод некоторых данных с помощью валидации данных в Pydantic:
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None,  max_length=255)

    # Нам также важно, чтобы пользователь не передавал только пробелы, иначе это будет некорректно
    # Так что обработаем и это с помощью валидатора:
    @field_validator('wallet_name')
    def wallet_name_is_not_empty(cls, name: str) -> str:
        # Убираем пробелы по краям с помощью .strip() и проверяем, не пуста ли строка:
        clean_str = name.strip()

        if not clean_str:
            raise HTTPException(status_code=400, detail='У кошелька должно быть свое имя, а не пробелы!!!')

        return clean_str

    # Чтобы ограничить поле amount используем функцию field_validator как декоратор:
    # Это валидатор, что сумма положительная
    @field_validator('amount')
    def amount_must_be_positive(cls, value: float) -> float:
        # Логика такая: нам нужно проверить, что amount >= 0 и возвратить значение если всё ок
        if value < 0:
            raise HTTPException(status_code=400, detail='Amount must be positive or null')
        
        return value
    

class CreateWalletSchema(BaseModel):
    name: str = Field(max_length=127)
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

        return clean_str

    # Это валидатор, что сумма положительная
    @field_validator('initial_balance')
    def amount_must_be_positive(cls, value: float) -> float:
        # Логика такая: нам нужно проверить, что amount >= 0 и возвратить значение если всё ок
        if value < 0:
            raise ValueError("Initial balanse shouldn't be negative")
        
        return value