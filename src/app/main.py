# type: ignore
import subprocess

import cloudinary
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
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

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)

app.include_router(api_router)


register_tortoise(
    app,
    # db_url=f'postgres:'
    #        f'//{os.getenv("USER")}:'
    #        f'{os.getenv("PASSWORD")}@'
    #        f'{os.getenv("HOST")}/'
    #        f'{os.getenv("DATABASE")}',
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": APP_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    status_output: tuple[int, str] = subprocess.getstatusoutput("mypy .")
    if status_output[0]:
        print(status_output[1])
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)
