import json
import os.path

from fastapi import APIRouter
from fastapi.responses import FileResponse


# creates a router for the end points
router = APIRouter()


# returns a file as a FileResponse.
# the pad to the file must be specified in the url get_file/{"path","folder","under folder","File"}
@router.get('/get_file/{path}')
def get_files(path: str):
    path = path.replace("'", '"')
    path = os.path.join(*json.loads(path)['path'].split(','))
    return FileResponse(path)
