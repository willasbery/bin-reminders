from sqlmodel import create_engine, SQLModel, Session

from models import *
from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
    
    
def del_db(session: Session) -> None:
    SQLModel.metadata.drop_all(engine)