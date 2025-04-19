from typing import Annotated
from fastapi import APIRouter, Query


from app.database.db import SessionDep
from app.database.entities.employee import Employee

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    responses={404: {"description": "Employee not found"}},
)



@router.get("/")
async def index():
    return {"message": "This is main info about employees"}

@router.get("/all")
def get_employees(session: SessionDep,
                  offset: int = 0,
                  limit: Annotated[int, Query(le=100)] = 100
                  ) -> list[Employee]:
    employees = session.query(Employee).offset(offset).limit(limit).all()
    return employees