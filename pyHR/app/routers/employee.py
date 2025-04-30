from typing import Annotated
from fastapi import APIRouter, Query


from app.database.db import SessionDep
from app.database.models.employee_model import Employee
from app.security.security import TokenDep

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    responses={404: {"description": "Employee not found"}},
)



@router.get("/token")
def token(user_token: TokenDep):
    return {"token": user_token}

@router.get("/all")
def get_employees(session: SessionDep,
                  offset: int = 0,
                  limit: Annotated[int, Query(le=100)] = 100
                  ) -> list[Employee]:
    employees = session.query(Employee).offset(offset).limit(limit).all()
    return employees