# -*- coding: utf-8 -*-

"""FastAPI entry file."""

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise import run_async
from lizard import analyze_file  # type: ignore
from models import SourceCodeString
from library import get_filename, get_function_attrs
from database import init


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# run_async(init())

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("start.j2", {"request": request})


@app.post("/analyse")
async def analyse(scs: SourceCodeString):
    code_str: str = '\n'.join(scs.code)
    filename: str = get_filename(scs.language)
    analysis = analyze_file.analyze_source_code(filename, code_str)
    return analysis.__dict__


@app.post("/analyseform", response_class=HTMLResponse)
async def analyseform(request: Request, language: str=Form(...), code: str=Form(...)):
    filename: str = get_filename(language)
    analysis = analyze_file.analyze_source_code(filename, code)
    return templates.TemplateResponse(
        "results.j2",
        {
            "request": request,
            "code": code,
            "rows": {
                "Average Cyclomatic Complexity": analysis.average_cyclomatic_complexity,
                "Lines of Code": analysis.__dict__["nloc"],
                "Average Token Count": analysis.__dict__["token_count"],
            },
            "functions": None if len(analysis.function_list) == 0 else get_function_attrs(analysis.function_list),
        },
    )
