# AiDoctor (working title)
   
## Description
   The goal of the project is to create a tool that simplifies working with TensorFlow and other frameworks.
   The plan is to structure everything in a modular way so that, based on the API, anyone can build and reuse their own tools and components.
   The entire project is still in a very early stage and is currently in a phase of experimentation and exploration.

    1. pip install fastapi


## predefined API endpoints (Data Base)
   used to create and communicate with sqlite3 databases
    
   ### /addTable (POST)
   #### creates a new table, if the database does not exist it is automatically created as a .db sqlLite3 file
    data_base_name: str
      table_name: str
      values: List[str]
      ___________
      {
        "data_base_name": "string",
        "table_name": "string",
        "values": [
          "valueOne TEXT","ValueTwo TEXT","22 INT"
        ]
      }

   ### /insert (POST)
   #### Insert values into the table
      data_base_name: str
      table_name: str
      values: List[str]
      ___________
      {
        "data_base_name": "string",
        "table_name": "string",
        "values": [
          "value one","Value two"
        ]
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
   
   
## predefined API endpoints (Cache)
   should be used for caching data, primarily for the planned data picker

   ### /cache/socket/{id} (websocket)
   ####  can use Websocket to return continuously changing data from cache.
      /cache/socket/{id}
      example:  ws://localhost:8000/cache/socket/123
   
   ### /cache/{id} (GET)
   #### returns an entry from cache based on the id
      /cache/{id}
      example: http://0.0.0.0:8000/cache/123

   ### /addValueToCache/{id} (POST)
   #### adds an entry to the cache. If the ID is already taken, the entry is added to the corresponding list, otherwise a
   #### new entry is created with the ID. If "extend" in the request is True, the content of value is added to the existing
   #### list, otherwise the value is added to the entry as a list.
      value: List[Any]
      extend: bool
      ---------------
      {
        "value": [
          "value one", "value two"
        ],
        "extend": true
      }

   ### /removeCacheEntry/{id} (GET)
   #### remove entry of cache based on id
      /removeCacheEntry/{id}
      example: http://0.0.0.0:8000/removeCacheEntry/123

     ### /cacheIdIsAssigned/{cache_id} (GET)
   #### checks whether an id is already occupied
      /cacheIdIsAssigned/{cache_id}
      example: http://0.0.0.0:8000/cacheIdIsAssigned/123
   
   ### /getUnusedId
   #### returns an unused random id from numbers
      /getUnusedId
      example: http://0.0.0.0:8000/getUnusedId

## predefined API endpoints (Files)

   ### /basePath (GET)
   #### returns the home basic path
      /basePath
      example: http://0.0.0.0:8000/basePath

   
   ### /getFilesDivs (POST)
   #### returns a list with lots of information with path to matching icon intended to create divs for the planned file
   #### picker to represent the files and folders
      path: str
      --------------
      {
     "path": "string"
      }

   ### /getFiles (POST)
   #### list files from the given path and returns a list of the files
      path: str
      --------------
      {
     "path": "string"
      }

 
   
## predefined API endpoints (Project)
   
   ### /addProject (POST)
   #### creates a new project, the plan is that the whole project will be assembled within a folder. Here a folder is
   #### created in the standard path and a basic entry is created in a database, you get the AUTOINCREMENT id back 
   
      name: str
      description: str
      creation_date: datetime = Field(default_factory=datetime.now)
      ------------------------------------
      {
     "name": "project name",
     "description": "description",
     "creation_date": is created automatically, nothing needs to be specified
      }
   
   ### /projectNewFolder (POST)
   #### allows you to create subfolders in the project folder
      
      add_path: List[str]
      project_id: str
      -----------------
      {
     "add_path": [
       "subfolder","under subfolder"
     ],
     "project_id": "123"
      }

## predefined API endpoints (root)
   
   ### / (GET)
   #### returns the content of index.html as an HTML response. Serves as an overlay template in which future individually created work windows are to be loaded into an iframe
      http://0.0.0.0:8000/
   
   ### /extend/{html_name} (GET)
   #### is used for HTML response of values from .html files within static/HTML/
      /extend/{html_name}
      example: http://0.0.0.0:8000/extend/test.html
   
      