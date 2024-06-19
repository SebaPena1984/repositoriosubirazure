import pyodbc

server = 'prueba-arsis-bd.database.windows.net'
database = 'ASP_SP_2'
username = 'AdminArs'
password = 'Arsis2004'
driver= '{ODBC Driver 17 for SQL Server}'

# Construir la cadena de conexión
CONNECTION_STRING = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'