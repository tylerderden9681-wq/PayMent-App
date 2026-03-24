from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from sqlalchemy import DECIMAL


class Wallet(Base):
    # Пишем название таблицы через __tablename__:
    __tablename__ = "wallet"

    # Задаем остальные параметры таблица:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))