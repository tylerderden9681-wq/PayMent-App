from fastapi import APIRouter, Depends
from app.services.operation import income_money, expense_money
from app.schemas import OperationSchema
from app.dependency import get_db
from sqlalchemy.orm import Session


router = APIRouter()

# 1) Доход:
@router.post('/operations/income')
def income_my_money(operation: OperationSchema, db: Session = Depends(get_db)):
    return income_money(db, operation)

    
# 2) Расход:
@router.post('/operations/expense')
def expense_my_money(operation: OperationSchema, db: Session = Depends(get_db)):
    return expense_money(db, operation)