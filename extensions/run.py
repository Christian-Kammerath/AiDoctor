import os
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import loadSettings
from Routers import include_routers

app = FastAPI()

routes_directory = os.path.join(os.path.dirname(__file__), "API_Endpoints")
include_routers(app, routes_directory)
app.mount("/extensions/plugins", StaticFiles(directory="extensions/plugins"), name="plugins")

if __name__ == "__main__":
    settings = loadSettings.Settings('extensions/dockerSettings.json').load_settings()

    host_ip = settings.select('Docker', 'address')
    port = settings.select('Docker', 'address_port')

    uvicorn.run(app, host=host_ip, port=port)