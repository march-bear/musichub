from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.settings import AppSettings

_app_settings = AppSettings() # fix

engine = create_engine(_app_settings.shared.DATABASE_URL)

if not _app_settings.shared.MIGRATIONS_ENABLED:
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
