from pydantic import BaseModel, Field
from typing import List, Any
from datetime import datetime


class DbBase(BaseModel):
    data_base_name: str
    table_name: str
    values: List[str]
    token: str


class GetTabelValue(BaseModel):
    data_base_name: str
    tabel_name: str
    token: str


class DbQuery(BaseModel):
    data_base_name: str
    query: str
    token: str


class GetFiles(BaseModel):
    path: str
    token: str


class Cache(BaseModel):
    cache_id: str
    value: List[Any]
    extend: bool
    token: str


class Project(BaseModel):
    name: str
    description: str
    creation_date: datetime = Field(default_factory=datetime.now)
    token: str


class NewProjectFolder(BaseModel):
    add_path: List[str]
    project_id: str
    token: str


class AddUser(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    is_Admin: bool
    password: str
    token: str


class Login(BaseModel):
    user_name: str
    password: str


class CacheId(BaseModel):
    id: str
    token: str


class Token(BaseModel):
    token: str


class Plugin(BaseModel):
    token: str
    method: str
    url_path: str
    request_body: dict
