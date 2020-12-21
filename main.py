# -*- coding: utf-8 -*-

"""FastAPI entry file."""

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from lizard import analyze_file  # type: ignore
from models import SourceCodeString
from library import get_filename, setup_html, generate_analysis_results, generate_start_page

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return HTMLResponse(content=generate_start_page(), status_code=200)


@app.post("/analyse")
async def analyse(scs: SourceCodeString):
    code_str: str = '\n'.join(scs.code)
    filename: str = get_filename(scs.language)
    analysis = analyze_file.analyze_source_code(filename, code_str)
    return analysis.__dict__


@app.post("/analyseform")
async def analyseform(language: str=Form(...), code: str=Form(...)):
    filename: str = get_filename(language)
    analysis = analyze_file.analyze_source_code(filename, code)
    return HTMLResponse(content=generate_analysis_results(analysis, code), status_code=200)
