# -*- coding: utf-8 -*-


"""Models used by the code finder app."""


import typing
from enum import Enum
from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields


class Language(Enum):
    PYTHON = 'python'


class SourceCodeString(BaseModel):
    language: str
    code: typing.List[str]


class SearchString(BaseModel):
    language: str
    query_text: str


class QueryString(Model):
    """This is the database model capturing the user submitted queries."""
    id = fields.IntField(pk=True)
    query = fields.CharField(max_length=1024)
    language = fields.CharEnumField(max_length=0, enum_type=Language)
    results = fields.JSONField(null=True)
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.query
