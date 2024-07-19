from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
import uvicorn

#initializes api and reads in the points fom file routes
app = FastAPI()
app.include_router(router)

#creates a static folder to access files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    #starts server
    uvicorn.run(app, host="0.0.0.0", port=8000)
