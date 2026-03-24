from fastapi import APIRouter, Depends
from app.schemas import CreateWalletSchema
from app.services.wallet import create_new_wallet, get_balance
from sqlalchemy.orm import Session
from app.dependency import get_db


router = APIRouter()

@router.get('/balance')
def get_new_balance(wallet_name: str | None = None, db: Session = Depends(get_db)):
    return get_balance(db, wallet_name)


@router.post('/wallets')
def create_wallet(wallet: CreateWalletSchema, db: Session = Depends(get_db)):
    return create_new_wallet(db, wallet)