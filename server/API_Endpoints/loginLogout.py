from fastapi import APIRouter, Request
from server.securityCheck import SecurityCheck
from server.apiBaseClasses import Login
from server.tokens import blacklist_token

# creates a router for the end points
router = APIRouter()


# login with username and password, returns token if the user is in the database.
@router.post('/login')
def user_login(user_login_data: Login):
    return SecurityCheck(user_login_data.user_name, user_login_data.password).check_security()


# logs the user out by putting the token on a blacklist. This invalidates it.
@router.get("/logout")
def logout(request: Request):
    blacklist_token(request.cookies.get("access_token"))
    return {'msg': 'token was invalidated'}
