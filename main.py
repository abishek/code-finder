# -*- coding: utf-8 -*-

"""FastAPI entry file."""

import requests
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise import run_async
from github import Github
from lizard import analyze_file  # type: ignore
from models import SourceCodeString, SearchString
from library import get_filename, get_function_attrs
from database import init
from pydantic import BaseSettings


class Settings(BaseSettings):
    ghtoken: str
    staticdir: str = "static"
    templatesdir: str = "templates"

    class Config:
        env_file = ".env"


settings = Settings()
app = FastAPI()
gh = Github(settings.ghtoken)
app.mount("/static", StaticFiles(directory=settings.staticdir), name="static")
templates = Jinja2Templates(directory=settings.templatesdir)

# run_async(init())

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("start.j2", {"request": request})


@app.post("/search-repos")
async def search_repos(st: SearchString):
    # log the search query.
    results = gh.search_repositories(query="{0} language:{1}".format(st.query_text, st.language))
    top10 = results[:10]
    api_results = []
    for result in top10:
        api_results.append({
            "name": result.full_name,
            "description": result.description,
            "forks": result.forks,
            "counts": {
                "forks": result.forks_count,
                "stars": result.stargazers_count,
                "subscribers": result.subscribers_count,
            },
            "language": result.language,
        })
    return {"results": api_results}


@app.post("/search-code")
async def search_code(st: SearchString):
    # log the search query.
    print(settings.ghtoken)
    results = gh.search_code(query="{0} language:{1}".format(st.query_text, st.language))[:10]
    api_results = []
    for result in results:
        api_results.append({
            "name": result.name,
            "license": result.license,
            "repository": {
                "name": result.repository.full_name,
                "description": result.repository.description,
                "forks": result.repository.forks_count,
                "stars": result.repository.stargazers_count,
                "subscribers": result.repository.subscribers_count,
            },
            "snippet": result.decoded_content,
        })
    return {"results": api_results}


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
