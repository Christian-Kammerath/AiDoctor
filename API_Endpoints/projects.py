import os.path

from fastapi import APIRouter
import dataBase

import apiBaseClasses

# creates a router for the end points
router = APIRouter()


# creates a new project, the plan is that the whole project will be assembled within a folder. Here a folder is
# created in the standard path and a basic entry is created in a database, you get the AUTOINCREMENT id back
@router.post("/addProject")
def add_projects(new_project: apiBaseClasses.Project):
    path = os.path.join('static', 'Projects', new_project.name)

    if not os.path.exists(path):
        os.mkdir(path)

    db = dataBase.DataBase('projectsDb')
    db.create_table('project', ["ID INTEGER PRIMARY KEY AUTOINCREMENT", "name TEXT", "description TEXT", "projectPath TEXT", "date TEXT"])
    project_id = db.insert('project',"name,description,projectPath,date",new_project.name,new_project.description, path, str(new_project.creation_date))
    return project_id


# allows you to create subfolders in the project folder
@router.post('/projectNewFolder')
def add_new_folder(new_folder: apiBaseClasses.NewProjectFolder):

    try:
        project_path = dataBase.DataBase('projectsDb').select('project','projectPath',f'id = {new_folder.project_id}')
        path = os.path.join(project_path,*new_folder.name)

        if not os.path.exists(path):
            os.mkdir(path)

    except FileNotFoundError:
        return {'msg': "FileNotFoundError"}


