from pydantic import BaseModel, Field
from typing import List, Any
from datetime import datetime


class DbBase(BaseModel):
    data_base_name: str
    table_name: str
    values: List[str]


class DbQuery(BaseModel):
    data_base_name: str
    query: str


class GetFiles(BaseModel):
    path: str


class Cache(BaseModel):
    value: List[Any]
    extend: bool


class Project(BaseModel):
    name: str
    description: str
    creation_date: datetime = Field(default_factory=datetime.now)


class NewProjectFolder(BaseModel):
    add_path: List[str]
    project_id: str
