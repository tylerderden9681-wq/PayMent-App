from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from sqlalchemy import DECIMAL, ForeignKey

# Создадим новый класс для хранения всех пользователей
class User(Base):
    __tablename__ = "user"
    # Будет ещё 2 поля (пока что, потому что в дальнейшем хочется чтобы пользователь проходил через гугл или email)
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)

class Wallet(Base):
    # Пишем название таблицы через __tablename__:
    __tablename__ = "wallet"

    # Задаем остальные параметры таблица:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    # Нам также нужно привязать кошельки к конкретному пользователю, то есть тогда будет так, что у 
    # одного пользователя может быть много кошельков, а у одного кошелька НЕ может быть много 
    # пользователей - для этого используем ForeignKey() с парамертом nullable=False, который 
    # говорит, что кошелёк не может создавать без пользователя
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)