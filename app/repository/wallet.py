from sqlalchemy.orm import Session

from app.models import Wallet
from decimal import Decimal


def is_wallet_exist(db: Session, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None

def add_income(db: Session, wallet_name: str, amount: float) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    amount_decimal = Decimal(amount)
    wallet.balance += amount_decimal
    return wallet

def get_wallet_balance_by_name(db: Session, wallet_name: str) -> float:
    return db.query(Wallet).filter(Wallet.name == wallet_name).first()
    
    
def add_extend(db: Session, wallet_name: str, amount: float) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.balance -= amount
    return wallet


def get_all_wallets(db: Session) -> dict[str, float]:
    return db.query(Wallet).all()


def create_new_wallet1(db: Session, wallet_name: str, amount: float) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount)
    db.add(wallet)
    return wallet
