from typing import Any, TypeVar, Generic, Annotated

from fastapi import Query, HTTPException
from pydantic import BaseModel, Field


# Lokalizacja
# i18n.load_path.append("./translations")
# i18n.set('filename_format', '{locale}.{format}')
# i18n.set('enable_memoization', 'true')
# i18n.set('fallback_locale', 'en')



class FilterParams(BaseModel):
    """Parametry ścieżki do filtrowania danych"""
    offset: int = Field(0, ge=0)
    limit: int = Field(10, ge=0, le=100)

FilterParamsDep = Annotated[FilterParams, Query()]


T = TypeVar('T')

class Response(Generic[T]):
    """Klasa przechowująca odpowiedź do API
    """
    def __init__(self, data: T = None, status_code: int = 200, message: str = ""):
        self.data = data
        self.code = status_code
        self.error = message


    def get_model(self) -> Any:
        match self.code:
            case 200 | 201:
                return self.data
            case _:
                raise HTTPException(status_code=self.code, detail=self.error)


class BadRequest(Response):
    def __init__(self, message):
        super().__init__(data=None, status_code=400, message=message)

class NotFound(Response):
    def __init__(self, message):
        super().__init__(data=None, status_code=404, message=message)


