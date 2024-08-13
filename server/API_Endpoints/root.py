from fastapi import APIRouter, Request, BackgroundTasks, Response
from starlette.responses import FileResponse
import loadSettings
import pathPermissionCheck
from server import forwardRequest
from server.securityCheck import SecurityCheck

# creates a router for the end points
router = APIRouter()


# returns the content of index.html as an FileResponse. Serves as an overlay template in which future individually
# created work windows are to be loaded into an iframe
@router.get("/")
async def root(request: Request, response: Response, background_tasks: BackgroundTasks):
    response.headers["Cache-Control"] = "no-store"
    if loadSettings.get_settings.select('security', 'token', 'token_enabled'):

        token = request.cookies.get("access_token")
        if SecurityCheck().is_user_token_valid(token):
            if pathPermissionCheck.PathPermissionCheck('server/static/home/index.html', token).check():
                return FileResponse('server/static/home/index.html')
        return await (forwardRequest.ForwardRequest('GET', 'http://0.0.0.0:9000/get_file/{"path":"extensions,plugins,'
                                                           'Login,login.html"}')
                      .file_response(background_tasks))
    return FileResponse('server/static/home/index.html')


