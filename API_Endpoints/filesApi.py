from fastapi import APIRouter
import apiBaseClasses
import os

import fileHandler

# creates a router for the end points
router = APIRouter()


# returns the home basic path
@router.get('/basePath')
def get_base_path():
    return os.path.expanduser("~")

# list files from the given path and returns a list of the files
@router.post('/getFiles')
def get_files(path: apiBaseClasses.GetFiles):
    return os.listdir(path.path)

# returns a list with lots of information with path to matching icon intended to create divs for the planned file
# picker to represent the files and folders
@router.post('/getFilesDivs')
async def get_files(path: apiBaseClasses.GetFiles):
    return {'result': fileHandler.generate_div_info_list(path.path)}

