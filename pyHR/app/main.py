from fastapi import FastAPI

from .logger import setup_logging
from .routers import employee, login

setup_logging()

app = FastAPI()

app.include_router(login.router)
app.include_router(employee.router)




@app.get("/")
async def root():
    return {"message": "Hello XD"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
