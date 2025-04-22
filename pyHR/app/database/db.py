import logging
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import create_engine, Session

load_dotenv(os.path.realpath("./.env"))
DATABASE_URL = os.environ.get("DB_URL")

connect_args = {"check_same_thread": False}

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(DATABASE_URL)




# def create_db():
#     logger.debug("CREATING DATABASE")
#     SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]