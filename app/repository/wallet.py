BALANCE = {'apple': 200}


def is_wallet_exist(wallet_name: str) -> bool:
    return wallet_name in BALANCE

def add_income(wallet_name: str, amount: float) -> float:
    BALANCE[wallet_name] += amount 
    return BALANCE[wallet_name]

def get_wallet_balance_by_name(wallet_name: str) -> float:
    return BALANCE[wallet_name]
    
def add_extend(wallet_name: str, amount: float) -> float:
    BALANCE[wallet_name] -= amount 
    return BALANCE[wallet_name]

def get_all_wallets() -> dict[str, float]:
    return BALANCE.copy() 

def create_new_wallet1(name: str, amount: float) -> float:
    BALANCE[name] = amount
    return BALANCE[name]