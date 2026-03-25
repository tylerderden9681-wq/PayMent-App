from fastapi import APIRouter, Depends
from app.services.operation import income_money, expense_money
from app.schemas import OperationSchema
from app.dependency import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.api.v1.users import get_current_user

router = APIRouter()

# 1) Доход:
@router.post('/operations/income')
def income_my_money(operation: OperationSchema, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    return income_money(db, current_user, operation)

    
# 2) Расход:
@router.post('/operations/expense')
def expense_my_money(operation: OperationSchema, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return expense_money(db, current_user, operation)