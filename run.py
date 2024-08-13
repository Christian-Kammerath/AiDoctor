import getpass
from Docker.docker import build_docker_image, run_docker_container
from Routers import include_routers
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from loadSettings import get_settings


# start server
def start_backend(app, host_ip, port):

    if get_settings.select('Docker', 'extensions_activate'):
        image_name = get_settings.select('Docker', 'extensions', 'image_name')
        port_mapping = get_settings.select('Docker', 'extensions', 'port_mapping')
        dockerfile_path = get_settings.select('Docker', 'extensions', 'dockerfile_path')
        sudo_password = getpass.getpass("Enter your sudo password: ")

        if build_docker_image(image_name, dockerfile_path, sudo_password):
            run_docker_container(image_name, port_mapping, sudo_password)
    else:
        routes_directory = os.path.join(os.path.dirname(__file__), "extensions/API_Endpoints")
        include_routers(app, routes_directory)
        app.mount("/extensions/plugins", StaticFiles(directory="extensions/plugins"), name="plugins")

    routes_directory = os.path.join(os.path.dirname(__file__), "server/API_Endpoints")
    include_routers(app, routes_directory)
    app.mount("server/static", StaticFiles(directory="static"), name="static")
    uvicorn.run(app, host=host_ip, port=port)


# start client
def start_frontend(app, host_ip, port):
    routes_directory = os.path.join(os.path.dirname(__file__), "client/API_Endpoints")
    include_routers(app, routes_directory)
    uvicorn.run(app, host=host_ip, port=port)


# start client and server
def start_full(app, host_ip, port):
    if get_settings.select('Docker', 'extensions_activate'):
        image_name = get_settings.select('Docker', 'extensions', 'image_name')
        port_mapping = get_settings.select('Docker', 'extensions', 'port_mapping')
        dockerfile_path = get_settings.select('Docker', 'extensions', 'dockerfile_path')
        sudo_password = getpass.getpass("Enter your sudo password: ")

        if build_docker_image(image_name, dockerfile_path, sudo_password):
            run_docker_container(image_name, port_mapping, sudo_password)

    else:
        routes_directory = os.path.join(os.path.dirname(__file__), "extensions/API_Endpoints")
        include_routers(app, routes_directory)
        app.mount("/extensions/plugins", StaticFiles(directory="extensions/plugins"), name="plugins")

    routes_directory = os.path.join(os.path.dirname(__file__), "client/API_Endpoints")
    include_routers(app, routes_directory)
    routes_directory = os.path.join(os.path.dirname(__file__), "server/API_Endpoints")
    include_routers(app, routes_directory)
    app.mount("/server/static", StaticFiles(directory="server/static"), name="static")
    uvicorn.run(app, host=host_ip, port=port)
