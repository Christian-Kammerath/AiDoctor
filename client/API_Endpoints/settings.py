from fastapi import APIRouter
from server import apiBaseClasses
from module.filePicker import fileHandler
import os
from fastapi.responses import JSONResponse


# creates a router for the end points
router = APIRouter()


@router.get("/getSettings")
def get_settings():
    main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(main_dir,"settings.json")) as file:
        return JSONResponse(file.read())