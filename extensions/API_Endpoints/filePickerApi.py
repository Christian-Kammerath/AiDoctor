from fastapi import APIRouter
from pydantic import BaseModel
from extensions.plugins.filePicker import fileHandler
import os

# creates a router for the end points
router = APIRouter()


class GetFiles(BaseModel):
    path: str


# returns the home basic path
@router.get('/extensions/basePath')
def get_base_path():
    return os.path.expanduser("~")


# list files from the given path and returns a list of the files
@router.post('/extensions/getFiles')
def get_files(request: GetFiles):
    return os.listdir(request.path)


# returns a list with lots of information with path to matching icon intended to create divs for the planned file
# picker to represent the files and folders
@router.post('/extensions/getFilesDivs')
async def get_files(request: GetFiles):
    return {'result': fileHandler.generate_div_info_list(request.path)}
