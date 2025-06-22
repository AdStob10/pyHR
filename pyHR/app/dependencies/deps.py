from typing import Any, TypeVar, Generic, Annotated

from fastapi import Query, HTTPException
from pydantic import BaseModel, Field


class BaseListParams(BaseModel):
    """
    Query path arguments to filter data in API
    You can inherit after this class and define additional fields to filter
    """
    offset: int = Field(0, ge=0)
    limit: int = Field(5, ge=0, le=100)


FilterParamsDep = Annotated[BaseListParams, Query()]

T = TypeVar('T')


class Response(Generic[T]):
    """
        Object holding API response data
    """

    def __init__(self, data: T = None, status_code: int = 200, message: str = ""):
        """
        :param data: object to return in api
        :param status_code: http status code
        :param message: error message
        """
        self.data = data
        self.status_code = status_code
        self.error = message

    def get_model(self) -> Any:
        """
        Get model data or raise exception if status code is not 200/201
        Exception is automatically mapped to error response in FastAPI
        :return: data
        """
        match self.status_code:
            case 200 | 201:
                return self.data
            case _:
                raise HTTPException(status_code=self.status_code, detail=self.error)


class BadRequest(Response):
    def __init__(self, message):
        super().__init__(data=None, status_code=400, message=message)


class NotFound(Response):
    def __init__(self, message):
        super().__init__(data=None, status_code=404, message=message)
