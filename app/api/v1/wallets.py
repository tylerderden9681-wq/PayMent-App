from fastapi import APIRouter, Depends
from app.schemas import CreateWalletSchema
from app.services.wallet import create_new_wallet, get_balance
from sqlalchemy.orm import Session
from app.dependency import get_db
from app.models import User
from app.api.v1.users import get_current_user


router = APIRouter()

@router.get('/balance')
def get_new_balance(wallet_name: str | None = None, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    return get_balance(db, current_user, wallet_name)


@router.post('/wallets')
def create_wallet(wallet: CreateWalletSchema, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return create_new_wallet(db, current_user, wallet)