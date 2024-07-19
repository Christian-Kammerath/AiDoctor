from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile
import apiBaseClasses
import dataBase

# creates a router for the end points
router = APIRouter()


@router.get('/',response_class=HTMLResponse)
def root():
    with open('static/HTML/index.html') as file:
        return file.read()


# creates a new table, if the database does not exist it is automatically created as a .db sqlLite3 file
@router.post('/addTable')
def add_table(new_table: apiBaseClasses.DbBase):
    return (dataBase
            .DataBase(new_table.data_base_name)
            .create_table(new_table.table_name,new_table.values))


# Insert values into the table
@router.post('/insert')
def insert_to_tabel(insert: apiBaseClasses.DbBase):
    return (dataBase
            .DataBase(insert.data_base_name)
            .insert(insert.table_name, insert.values))

# enables an individual query the result is always fetched, if the operation is successful without a result being
# expected an empty list is returned
@router.post('/dbQuery')
def db_query(query: apiBaseClasses.DbQuery):
    return (dataBase
            .DataBase(query.data_base_name)
            .individual_query(query.query))

# returns all contents of an existing table
@router.get('/getTableValue/{db_name}/{tabel_name}')
def get_tabel_value(db_name: str, tabel_name: str):
    return (dataBase
            .DataBase(db_name)
            .get_all_table_values(tabel_name))