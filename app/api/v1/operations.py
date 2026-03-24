from fastapi import APIRouter
from app.services.operation import income_money, expense_money
from app.schemas import OperationSchema


router = APIRouter()

# 1) Доход:
@router.post('/operations/income')
def income_my_money(operation: OperationSchema):
    return income_money(operation)

    
# 2) Расход:
@router.post('/operations/expense')
def expense_my_money(operation: OperationSchema):
    return expense_money(operation)