from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = 'sqlite:///./finance.db'
# engine - движок для подключения к БД. Он хранит все настройки подключения и соединения с нашей БД
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создадим session. session - сессия работы с БД, то есть в это время мы сможем делать все наши
# операции с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Теперь нужно объявить какие модели будут использоваться при работе с SQLAlchemy
class Base(DeclarativeBase):
    pass
