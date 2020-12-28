# -*- coding: utf-8 -*-

from tortoise import Tortoise


async def init():
    """Connect to the database."""
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={'models': ['app.models']},
    )
    await Tortoise.generate_schemas(safe=True)
