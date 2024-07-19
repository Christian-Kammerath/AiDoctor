# AiDoctor
    1. pip install fastapi
    2. https://www.tensorflow.org/install/pip | Install appropriate package for system
    

## predefined API endpoints
    
   ### addTable (POST)
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

   ### insert (POST)
   #### # Insert values into the table
      data_base_name: str
      table_name: str
      values: str
      ___________
      {
     "data_base_name": "testDataBase",
     "table_name": "testTable",
     "values": "('ValueOne' , 'ValueTwo')"
      }