# AiDoctor
    1. pip install fastapi
    2. https://www.tensorflow.org/install/pip | Install appropriate package for system
    

## predefined API endpoints
    
   ### /addTable (POST)
   #### creates a new table, if the database does not exist it is automatically created as a .db sqlLite3 file
    data_base_name: str
    table_name: str
    values: str
    _____________
    {
    "data_base_name": "dataBaseName",
    "table_name": "tabelName",
    "values": "ValueOne TEXT, ValueTwo TEXT"
    }

   ### /insert (POST)
   #### Insert values into the table
      data_base_name: str
      table_name: str
      values: str
      ___________
      {
     "data_base_name": "dataBaseName",
     "table_name": "tabelName",
     "values": "('ValueOne' , 'ValueTwo')"
      }
   
   ### /dbQuery (POST)
   #### enables an individual query the result is always fetched, if the operation is successful without a result being expected an empty list is returned
      data_base_name: str
      query: str
      --------------
      {
     "data_base_name": "test1",
     "query": exampel "CREATE TABLE IF NOT EXISTS test2 (a TEXT, b TEXT)"
      }
   
   ### /getTableValue/{db_name}/{tabel_name} (GET)
   #### returns all contents of an existing table as list
      /getTableValue/(Data Base Name)/(Table Name)
      example:  http://0.0.0.0:8000/getTableValue/dataBaseOne/tableOne