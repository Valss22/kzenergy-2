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
    cloud_name="dmh0ekjaw",
    api_key="963345615946785",
    api_secret="JqFaq0KIFuk6rx-Z8eJSK-Gfpgc",
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
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT"))
