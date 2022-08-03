from datetime import date
from typing import Union

from pydantic.main import BaseModel


class WasteInfo(BaseModel):
    __root__: dict[str, Union[float, date]]


class WasteName(BaseModel):
    limit: float
    info: list[WasteInfo]


class Lineplot(BaseModel):
    __root__: dict[str, WasteName]
