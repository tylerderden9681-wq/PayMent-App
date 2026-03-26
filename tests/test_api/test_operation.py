# При теста используется метод трех А - ААА, то есть Arrange (подготовь) - Act (выполни) - Assert
# (выполни)

from app.models import User, Wallet
from decimal import Decimal

# 1. Определяем тестовую функцию, которая будет проверять наш функционал:
def test_add_expense_success(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    print(response.json())
    # Assert:
    assert response.status_code == 200
    assert response.json()["ok"] == True
    assert response.json()["details"]["msg"] == "The traksaktion is successfully"
    assert Decimal(str(response.json()["details"]["expense"])) == Decimal(50)
    assert Decimal(str(response.json()["details"]["new_balance"])) == Decimal(150)
    assert response.json()["details"]["description"] == "Food"


# Проверим, кореектна ли валидация данных:
def test_and_expense_negative_amount(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    # Assert
    assert response.status_code == 422

def test_and_expense_empty_name(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "   ",
            "amount": 100.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    # Assert
    assert response.status_code == 422


def test_and_expense_wallet_not_exists(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.commit()

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    # Assert
    assert response.status_code == 404


def test_and_expense_user_not_authorized(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.commit()

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer notexists"}
    )

    # Assert
    assert response.status_code == 401

def test_add_expense_not_enough_money(db_session, client):
    # Arrange: 

    # Нужно подготовить данные, которые будут использоваться в нашем тесте
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act:
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 250.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    print(response.json())
    # Assert:
    assert response.status_code == 400