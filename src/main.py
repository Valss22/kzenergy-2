import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.routers import api_router

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

    modules={"models": [
        "src.user.model",
        "src.user_profile.model",
        "src.competence.model",
        "src.discipline.model",
        "src.test.model",
    ]},
    generate_schemas=True,
    add_exception_handlers=True,
)
