from sqlalchemy.orm import Session

from app.models import Wallet
from decimal import Decimal

from app.models import User


def is_wallet_exist(db: Session, user_id: int, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first() is not None

def add_income(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    amount_decimal = Decimal(amount)
    wallet.balance += amount_decimal
    return wallet

def get_wallet_balance_by_name(db: Session, user_id: int, wallet_name: str) -> float:
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    
    
def add_extend(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance -= amount
    return wallet


def get_all_wallets(db: Session, user_id: int) -> dict[str, float]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_new_wallet1(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)
    db.add(wallet)
    return wallet
