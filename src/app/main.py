import time

from fastapi import FastAPI, Request

from app.api import data
from app.api import weather
from app.db import engine, database, metadata

metadata.create_all(engine)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(weather.router, tags=["weather"])
app.include_router(data.router, tags=["data"])
