from fastapi import APIRouter
from server import dataBase, apiBaseClasses
from server.securityCheck import SecurityCheck

# creates a router for the end points
router = APIRouter()


# creates a new table, if the database does not exist it is automatically created as a .db sqlLite3 file
@router.post('/addTable')
def add_table(new_table: apiBaseClasses.DbBase):
    if SecurityCheck().is_user_token_valid(new_table.token):
        return (dataBase
                .DataBase(new_table.data_base_name)
                .create_table(new_table.table_name, new_table.values))
    return {'msg': "Access denied"}


# Insert values into the table
@router.post('/insert')
def insert_to_tabel(insert: apiBaseClasses.DbBase):
    if SecurityCheck().is_user_token_valid(insert.token):
        return (dataBase
                .DataBase(insert.data_base_name)
                .insert(insert.table_name, insert.values))
    return {'msg': "Access denied"}


# enables an individual query the result is always fetched, if the operation is successful without a result being
# expected an empty list is returned
@router.post('/dbQuery')
def db_query(query: apiBaseClasses.DbQuery):
    if SecurityCheck().is_user_token_valid(query.token):
        return (dataBase
                .DataBase(query.data_base_name)
                .individual_query(query.query))
    return {'msg': "Access denied"}


# returns all contents of an existing table
@router.get('/getTableValue')
def get_tabel_value(value: apiBaseClasses.GetTabelValue):
    if SecurityCheck().is_user_token_valid(value.token):
        return (dataBase
                .DataBase(value.data_base_name)
                .get_all_table_values(value.tabel_name))
    return {'msg': "Access denied"}
