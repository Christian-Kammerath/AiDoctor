from fastapi import APIRouter
from fastapi.responses import HTMLResponse

import loadSettings

# creates a router for the end points
router = APIRouter()


# returns the content of index.html as an HTML response. Serves as an overlay template in which future individually
# created work windows are to be loaded into an iframe
@router.get("/", response_class=HTMLResponse)
def root():
    with open('server/static/HTML/index.html') as file:
        return file.read()


# is used for HTML response of values from .html files within static/HTML/
@router.get('/extend/{html_name}', response_class=HTMLResponse)
def get_html_page(html_name: str):
    with open(f'server/static/HTML/{html_name}.html') as file:
        return file.read()


@router.get('/modulePage/{module_name}/{html_name}', response_class=HTMLResponse)
def get_module_page(html_name: str, module_name: str):
    with open(f'module/{module_name}/{html_name}.html') as file:
        return file.read()
