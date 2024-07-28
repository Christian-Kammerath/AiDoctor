import webbrowser

from fastapi import APIRouter
from starlette.responses import HTMLResponse

from server import apiBaseClasses
from module.filePicker import fileHandler
import os

# creates a router for the end points
router = APIRouter()


# returns the home basic path
@router.get('/client/basePath')
def get_base_path():
    return os.path.expanduser("~")


# list files from the given path and returns a list of the files
@router.post('/client/getFiles')
def get_files(path: apiBaseClasses.GetFiles):
    return os.listdir(path.path)


# returns a list with lots of information with path to matching icon intended to create divs for the planned file
# picker to represent the files and folders
@router.post('/client/getFilesDivs')
async def get_files(path: apiBaseClasses.GetFiles):
    return {'result': fileHandler.generate_div_info_list(path.path)}

# returns html page from module FilePicker
@router.get('/FilePicker', response_class=HTMLResponse)
def get_file_picker():
    with open('module/filePicker/filePicker.html') as file:
        return file.read()

