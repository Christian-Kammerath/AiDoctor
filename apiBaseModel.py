from pydantic import BaseModel

class NewTable(BaseModel):
    data_base_name: str
    table_name: str
    values: str

class InsertValues(BaseModel):
    data_base_name: str
    table_name: str
    values: str