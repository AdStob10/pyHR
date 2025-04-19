from fastapi import FastAPI
from .routers import employee

app = FastAPI()

app.include_router(employee.router)



@app.get("/")
async def root():
    return {"message": "Hello XD"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
