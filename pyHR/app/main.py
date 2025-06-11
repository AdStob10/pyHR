from fastapi import FastAPI, Request

from .i18n import set_locale
from .logger import setup_logging
from .routers import employee, login, vacation_requests

setup_logging()

app = FastAPI()

app.include_router(login.router)
app.include_router(employee.router)
app.include_router(vacation_requests.router)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    await set_locale(request)
    response = await call_next(request)
    return response

