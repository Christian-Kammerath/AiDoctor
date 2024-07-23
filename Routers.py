import importlib.util
import os


# reads all api endpoints from one of the python files in a directory and adds them to the app. The only condition is
# that you use "router = APIRouter()" in your file and bind to router e.g. "@router.get()"

def include_routers(app, directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "router"):
                app.include_router(module.router)
