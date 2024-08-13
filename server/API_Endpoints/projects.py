import os.path

from fastapi import APIRouter
from server.securityCheck import SecurityCheck
from server import dataBase, apiBaseClasses

# creates a router for the end points
router = APIRouter()


# creates a new project, the plan is that the whole project will be assembled within a folder. Here a folder is
# created in the standard path and a basic entry is created in a database, you get the AUTOINCREMENT id back
@router.post("/addProject")
def add_projects(new_project: apiBaseClasses.Project):
    if SecurityCheck().is_user_token_valid(new_project.token):
        path = os.path.join('server', 'static', 'Projects', new_project.name)

        if not os.path.exists(path):
            os.mkdir(path)

        db = dataBase.DataBase('projectsDb')
        db.create_table('project',
                        ["ID INTEGER PRIMARY KEY AUTOINCREMENT", "name TEXT", "description TEXT", "projectPath TEXT",
                         "date TEXT"])
        project_id = db.insert('project', "name,description,projectPath,date", new_project.name,
                               new_project.description, path, str(new_project.creation_date))
        return project_id
    return {'msg': "Access denied"}


# allows you to create subfolders in the project folder
@router.post('/projectNewFolder')
def add_new_folder(new_folder: apiBaseClasses.NewProjectFolder):
    try:

        if SecurityCheck().is_user_token_valid(new_folder.token):

            project_path = (dataBase.DataBase('projectsDb')
                            .select('project', 'projectPath', f'ID =?', new_folder.project_id))
            project_path = project_path[0][0]
            folder_list = list(new_folder.add_path)

            path = os.path.join(project_path, *folder_list)

            if not os.path.exists(path):
                os.makedirs(path)

            return {'msg': f"created {path}"}
        return {'msg': "Access denied"}

    except FileNotFoundError:
        return {'msg': "FileNotFoundError"}
