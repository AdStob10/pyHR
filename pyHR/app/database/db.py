import os

from fastapi import Depends
from loguru import logger
from typing import Annotated
from sqlmodel import create_engine, SQLModel, Session, Field
from sqlalchemy import URL
from os import getenv
from dotenv import load_dotenv

load_dotenv(os.path.realpath("./.env"))
DATABASE_URL = os.environ.get("DB_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)




# def create_db():
#     logger.debug("CREATING DATABASE")
#     SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]