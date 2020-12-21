# -*- coding: utf-8 -*-


"""Models used by the code finder app."""


import typing
from pydantic import BaseModel


class SourceCodeString(BaseModel):
    language: str
    code: typing.List[str]
