from typing import Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from webvisualization_plots import plot_reported_cases_per_million, get_countries, get_start_date, get_end_date, get_all_countries

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/static",
    StaticFiles(
        # the directory the files are in
        directory="static/",
        html=True,
    ),
    # an internal name for FastAPI
    name="static",
)


@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """

    return templates.TemplateResponse(
        "plot_reported_cases_per_million_mod.html",
        {
            "request": request,
            # further template inputs here
            'top_countries': get_countries(),
            'countries': get_all_countries(),
            'start': get_start_date(),
            'end': get_end_date(),
        },
    )


@app.get("/plot_reported_cases_per_million.json")
def plot_reported_cases_per_million_json(countries: Optional[str]=None, start: Optional[str]=None, end: Optional[str]=None):
    """Return json chart from altair"""
    if countries:
        countries = countries.split(",")
    fig = plot_reported_cases_per_million(countries, start, end)
    return fig.to_dict()



def main():
    """Called when run as a script
    Should launch your web app
    """
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == "__main__":
    main()