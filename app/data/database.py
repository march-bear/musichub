from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings
from app.data.models import Base

engine = create_engine(settings.DATABASE_URL)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
