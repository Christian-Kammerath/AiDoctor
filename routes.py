from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile
import apiBaseModel
import dataBase

#creates a router for the end points
router = APIRouter()


@router.get('/',response_class=HTMLResponse)
def root():
    with open('static/HTML/index.html') as file:
        return file.read()


#creates a new table, if the database does not exist it is automatically created as a .db sqlLite3 file
@router.post('/addTable')
def add_table(new_table: apiBaseModel.NewTable):
    return (dataBase
            .DataBase(new_table.data_base_name)
            .create_table(new_table.table_name,new_table.values))

@router.post('/insert')
def insert_to_tabel(insert: apiBaseModel.InsertValues):
    return (dataBase
            .DataBase(insert.data_base_name)
            .insert(insert.table_name, insert.values))