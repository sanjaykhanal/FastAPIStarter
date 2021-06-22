from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import DATABASE_CONFIG



# SQLALCHEMY_DATABASE_URL = "postgresql://test_fast_api:test_fast_api@localhost:5432/test_fast_api"

SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    DATABASE_CONFIG["DATABASE_ENGINE"],
    DATABASE_CONFIG["DATABASE_USERNAME"],
    DATABASE_CONFIG["DATABASE_PASSWORD"],
    DATABASE_CONFIG["DATABASE_HOST"],
    DATABASE_CONFIG["DATABASE_PORT"],
    DATABASE_CONFIG["DATABASE_NAME"]
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
