from fastapi import APIRouter, Request, BackgroundTasks
from server import dataBase, tokens, hashPassword, apiBaseClasses, securityCheck, forwardRequest
import json

# creates a router for the end points
router = APIRouter()


# returns the admin page, access is limited to admin users by default
@router.get('/admin')
async def get_admin_page(request: Request, background_tasks: BackgroundTasks):
    token = request.cookies.get("access_token")

    if securityCheck.SecurityCheck().is_admin_token_valid(token):
        return await forwardRequest.ForwardRequest('GET',
                                                   'http://0.0.0.0:9000/get_file/{"path":"extensions,plugins,Admin,'
                                                   'admin.html"}').file_response(background_tasks)
    return {'msg': 'access denied'}


# returns the menu points for the admin page,
@router.get("/admin/menu")
def get_admin_menu():
    with open("extensions/Admin/menu/menuSettings.json", 'r') as file:
        settings = json.load(file)
        return settings['entries']

# returns a list of standard user
@router.get("/admin/get_user")
def get_user(request: Request):
    token = request.cookies.get("access_token")

    if securityCheck.SecurityCheck().is_admin_token_valid(token):
        return dataBase.DataBase('userDb').select('user', 'userName', 'isAdmin = ?', (0,))
    return {'msg': 'access denied'}

# returns a list of admin
@router.get("/admin/get_admin")
def get_user(request: Request):
    token = request.cookies.get("access_token")

    if securityCheck.SecurityCheck().is_admin_token_valid(token):
        return dataBase.DataBase('userDb').select('user', 'userName', 'isAdmin = ?', (1,))
    return {'msg': 'access denied'}

# allows you to add new users
@router.post("/admin/add_user")
def add_user(user_info: apiBaseClasses.AddUser):
    if tokens.verify_token(user_info.token):
        if tokens.is_token_owner_admin(user_info.token):
            password_hash = hashPassword.hashes_password(user_info.password)
            db = dataBase.DataBase('userDb')
            db.create_table('user', ["ID INTEGER PRIMARY KEY AUTOINCREMENT",
                                     'firstName TEXT',
                                     'lastName TEXT',
                                     'userName TEXT UNIQUE',
                                     'isAdmin BOOLEAN'
                                     'passwordHash TEXT'])

            last_id = db.insert('user', 'firstName,lastName,userName,passwordHash',
                                user_info.first_name, user_info.last_name, user_info.user_name,
                                password_hash)

            return {'msg': f'{last_id}'}
        return {'msg': 'user is not admin'}
    return {'msg': 'access denied'}
