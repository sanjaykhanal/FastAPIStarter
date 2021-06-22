## How to use this repository

1. Clone the repository
2. Create a python virtual environment  (Tested in python 3.7.9)
3. Activate the environment
4. Install requirements with "pip install -r requirements.txt"
5. cd to app/
6. Run "python main.py"
7. Navigate to http://localhost:8000/docs to see the available api endpoints


## Understand the Structure:

- entrypoint is app/main.py
- configuration goes into config/config.py
- database connection details goes into database/db.py
- logger configuration goes into logger/logger.py. If you leave it as it is, logs will be automatically created under logs/ folder and it will use the default formatter. You can change the formatter to any format you like in logger/logger.py.
- two middlewares are included by default in the starter project. One is the CORS middleware. cors configurations are defined in config/config.py. enable/disable cors from flags.py by setting flags.enable_cors True or False
- Another middleware is for the user authentication. oauth2 with JWT is implemented for user authentication. Simply use authorization() function in your API endpoint to authorize your API. Example implementation is available in modules/authentication/api/users.py
- modules/ package contains the modular packages that needs to be included in the application. Interesting thing is now you just need to write your endpoints, cruds, schemas inside one of the modules and all the endpoints will be included in the application be default when main.py is executed.
- \_\_init\_\_.py must be in the same format as the one in modules/authentication/\_\_init\_\_.py  module
- If you want to disable authentication in API endpoints, just set flags.enable_authentication in flags.py to False.
