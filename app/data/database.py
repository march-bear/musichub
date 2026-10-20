from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data.models import Base
from app.settings import settings

engine = create_engine(settings.DATABASE_URL)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
