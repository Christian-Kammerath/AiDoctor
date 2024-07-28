from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
import webbrowser
import loadSettings
from Routers import include_routers
import argparse

# initializes api and reads in the points fom file routes
app = FastAPI()

# start server
def start_backend(host_ip, port):
    routes_directory = os.path.join(os.path.dirname(__file__), "server/API_Endpoints")
    include_routers(app, routes_directory)
    app.mount("server/static", StaticFiles(directory="static"), name="static")
    app.mount("/module", StaticFiles(directory="module"), name="module")
    uvicorn.run(app, host=host_ip, port=port)


# start client
def start_frontend(host_ip, port):
    routes_directory = os.path.join(os.path.dirname(__file__), "client/API_Endpoints")
    include_routers(app, routes_directory)
    app.mount("/module", StaticFiles(directory="module"), name="module")
    uvicorn.run(app, host=host_ip, port=port)


# start client and server
def start_full(host_ip, port):
    routes_directory = os.path.join(os.path.dirname(__file__), "client/API_Endpoints")
    include_routers(app, routes_directory)
    routes_directory = os.path.join(os.path.dirname(__file__), "server/API_Endpoints")
    include_routers(app, routes_directory)
    app.mount("/server/static", StaticFiles(directory="server/static"), name="static")
    app.mount("/module", StaticFiles(directory="module"), name="module")
    uvicorn.run(app, host=host_ip, port=port)


if __name__ == "__main__":

    # read and parse start arguments
    parser = argparse.ArgumentParser(description="Start FastAPI server with different modes")
    parser.add_argument('--mode', type=str, choices=['backend', 'frontend', 'full'], required=True,
                        help="Mode to run the server in")
    args = parser.parse_args()

    # loaded settings and copy ip and port settings in client and server settings json file
    settings = loadSettings.Settings('settings.json')
    loaded_settings = settings.load_settings()
    settings.copy_setting_entry_to_other_file("server/publicSettings.json", 'connect')
    settings.copy_setting_entry_to_other_file("module/publicSettings.json", 'connect')

    # Starts Client Server or both, depending on the startup
    if args.mode == "backend":
        start_backend(loaded_settings['connect']['server_ip'], loaded_settings['connect']['server_port'])
    elif args.mode == "frontend":
        start_frontend(loaded_settings['connect']['client_ip'], loaded_settings['connect']['client_port'])
    elif args.mode == "full":
        start_full(loaded_settings['connect']['client_ip'], loaded_settings['connect']['client_port'])
