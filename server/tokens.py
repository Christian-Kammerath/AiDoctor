import uuid
import jwt
import datetime
from fastapi import HTTPException
from loadSettings import get_settings
from server.dataBase import DataBase
import secrets


# creates random SECRET_KEY that is valid as long as the server is running

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = get_settings.select('security', 'token', 'token_exp_in_min')
token_blacklist = set()


def check_is_user_in_database(user_name):
    user_name_from_db = DataBase('userDb').select('user', 'userName', 'userName = ?', (user_name,))[0][0]
    return user_name == user_name_from_db


def get_is_user_admin_in_database(user_name):
    return DataBase('userDb').select('user', 'isAdmin', 'userName = ?', (user_name,))[0][0]


def create_jwt(user_name: str) -> str:
    is_admin = get_is_user_admin_in_database(user_name)

    payload = {
        'sub': user_name,
        'isa': is_admin,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        'jti': str(uuid.uuid4())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# Token Verifizierung
def verify_token(token: str):
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token is blacklisted")
    try:
        payload = decode_token(token)
        user_name = payload.get("sub")
        if user_name and check_is_user_in_database(user_name):
            return True
        return False
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def is_token_owner_admin(token: str):
    try:
        payload = decode_token(token)
        user_name = payload.get("sub")
        is_admin_in_token = payload.get("isa")
        is_admin_in_db = get_is_user_admin_in_database(user_name)
        return bool(is_admin_in_db) == is_admin_in_token
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def blacklist_token(token: str):
    token_blacklist.add(token)
