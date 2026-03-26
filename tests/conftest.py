# В этом файле хранится вся конфигурация pytest'а. Он нужен, чтобы делиться между разными 
# тестовыми файлами фикстурами и общими компонентами. Pytest сам будет подхватывать эти 
# зависимости и при помощи известного способа внедрения зависимостей внедрять эти зависимости 
# непосредственно в тест. 

# Почему так? Pytest спроектирован таким образом, чтобы тесты были 
# максимально простыми, а файл conftest.py позволяет нам централизовать общие вещи и автоматически 
# подключать их. 
 
# Мы также использовали термин ФИКСТУРА. Объясняю. Фикстура - это функция pytest, 
# которая заранее готовит нужное окружение для теста: данные, объекты, подключение, настройки. 
# Она нужна чтобы не повторять одинаковый подготовительный код в каждом тесте. 
# Pytest сам вызывает фикстуру перед тестом и передает её результат внутрь тестовой функции

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from main import app
from typing import Generator
from app.dependency import get_db
from fastapi.testclient import TestClient
import pytest
from app.database import Base

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, 
                            connect_args={'check_same_thread': False})

TestSessionLocal = sessionmaker(bind=test_engine,
                                autocommit=False,
                                autoflush=False)

def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try: 
        yield db
    finally:
        db.close()

# Меняем функцию для теста
app.dependency_overrides[get_db] = get_test_db

# Создаем тестового клиента, с помощью которого мы будем осуществлять API запрос

# Обязательно нужно объявить pytest, что это фикстура:
@pytest.fixture()
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Пересоздаем все таблицы перед тестом
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try: 
        yield db
    finally:
        db.close()