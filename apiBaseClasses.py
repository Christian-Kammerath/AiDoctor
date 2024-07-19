from pydantic import BaseModel


class DbBase(BaseModel):
    data_base_name: str
    table_name: str
    values: str


class DbQuery(BaseModel):
    data_base_name: str
    query: str
