import jwt
from fastapi import Header
from jwt import InvalidTokenError, ExpiredSignatureError
from starlette import status
from starlette.responses import JSONResponse

from src.app.settings import TOKEN_KEY


def get_jwt(auth_header: str = Header()):
    try:
        jwt.decode(
            auth_header.split(" ")[1],
            TOKEN_KEY, algorithms="HS256"
        )
    except (InvalidTokenError or ExpiredSignatureError) as e:
        if e == InvalidTokenError:
            return JSONResponse(
                {"detail": "token has expired"},
                status.HTTP_400_BAD_REQUEST
            )
        return JSONResponse(
            {"detail": "invalid token"},
            status.HTTP_400_BAD_REQUEST
        )
