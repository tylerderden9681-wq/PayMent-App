from fastapi import APIRouter
from app.schemas import CreateWalletSchema
from app.services.wallet import create_new_wallet, get_balance



router = APIRouter()

@router.get('/balance')
def get_new_balance(wallet_name: str | None = None):
    return get_balance(wallet_name)


@router.post('/wallets')
def create_wallet(wallet: CreateWalletSchema):
    return create_new_wallet(wallet)