from typing import Any

from app.database.db import SessionDep


class BaseRepository:
    def __init__(self, session: SessionDep):
        self.session: SessionDep  = session

    def save_model(self, model: Any):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model