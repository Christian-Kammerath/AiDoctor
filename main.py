from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
import webbrowser
from threading import Timer
from Routers import include_routers


# initializes api and reads in the points fom file routes
app = FastAPI()


# Assuming your routes are in the "API_Endpoints" directory
routes_directory = os.path.join(os.path.dirname(__file__), "API_Endpoints")
include_routers(app, routes_directory)

# creates a static folder to access files
app.mount("/static", StaticFiles(directory="static"), name="static")


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8000')

if __name__ == "__main__":
    # set a timer to open the browser after the server starts
    Timer(1, open_browser).start()
    # Start the Uvicorn-Server
    uvicorn.run(app, host="127.0.0.1", port=8000)

