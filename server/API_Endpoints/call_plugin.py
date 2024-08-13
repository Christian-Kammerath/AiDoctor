import json
import os
from fastapi import APIRouter, Request, Response
from fastapi import BackgroundTasks
import pathPermissionCheck
from server import apiBaseClasses, forwardRequest
from server.securityCheck import SecurityCheck

# creates a router for the end points
router = APIRouter()


# Enables the return of files from the extension, checking whether the token owner is authorized to access the file
@router.get("/server/get_file_from_plugin/{path}")
async def get_file(request: Request, response: Response, path: str, background_tasks: BackgroundTasks):
    response.headers["Cache-Control"] = "no-store"
    token = request.cookies.get("access_token")

    processed_path = os.path.join(*json.loads(path.replace("'", '"'))['path'].split(','))

    if pathPermissionCheck.PathPermissionCheck(processed_path, token).check():
        return await (forwardRequest.ForwardRequest('GET', f'http://0.0.0.0:9000/get_file/{path}')
                      .file_response(background_tasks))
    return {"msg": "access denied"}


# forwards a request to extensions api, optionally a body can be specified with a POST request
@router.post('/server/call_plugin_service')
async def call_plugin_post(request: apiBaseClasses.Plugin):
    if SecurityCheck().is_user_token_valid(request.token):

        if request.method == 'POST':
            response = await forwardRequest.ForwardRequest('POST', f'http://0.0.0.0:9000/{request.url_path}',
                                                           request.request_body).request()
            return response.json()
        elif request.method == 'GET':
            response = await forwardRequest.ForwardRequest('GET', f'http://0.0.0.0:9000/{request.url_path}').request()
            return response.json()

    return {'msg': "Access denied"}

