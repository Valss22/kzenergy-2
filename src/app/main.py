# type: ignore
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from src.app.routers import api_router
import os

from src.app.settings import APP_MODELS

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

register_tortoise(
    app,
    db_url=f'postgres:'
           f'//{os.getenv("USER")}:'
           f'{os.getenv("PASSWORD")}@'
           f'{os.getenv("HOST")}/'
           f'{os.getenv("DATABASE")}',
    # db_url=os.getenv("DATABASE_URL"),
    modules={"models": APP_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors():
        print(exc.errors())

    # if exc.errors()[0]["type"] == "IntegrityError":
    #     return JSONResponse(
    #         {"detail": "This email already exists"},
    #         status.HTTP_400_BAD_REQUEST
    #     )


if __name__ == '__main__':
    status_output: tuple[int, str] = subprocess.getstatusoutput("mypy .")
    if status_output[0]:
        print(status_output[1])
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)

