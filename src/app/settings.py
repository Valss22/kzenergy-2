import os
from dotenv import load_dotenv

load_dotenv()

SALT: bytes = b'$2b$12$nHVrxcliGHquJB5pw0sC8O'
TOKEN_KEY = "ndg5P:,gr6K3?ug3ZdT@dD"
TOKEN_TIME = 604_800

APP_MODELS = [
    "src.app.user.model",
    "src.app.facility.model",
    "src.app.waste.model",
    "src.app.ticket.model",
    "src.app.report.model",
]
DB_URL = f'postgres:'
f'//{os.getenv("USER")}:'
f'{os.getenv("PASSWORD")}@'
f'{os.getenv("HOST")}/'
f'{os.getenv("DATABASE")}'
