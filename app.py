from flask import Flask, render_template, request, session, redirect, url_for
#from config import CONNECTION_STRING
import pyodbc
import config
from datetime import datetime

server = 'prueba-arsis-bd.database.windows.net'
database = 'ASP_SP_2'
username = 'AdminArs'
password = 'Arsis2004'
driver= '{ODBC Driver 17 for SQL Server}'

# Construir la cadena de conexión
CONNECTION_STRING = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET'])
def home():
    return render_template('Index.html')



@app.route('/login', methods=['POST'])
def login():
    

    email = request.form['email']
    password = request.form['password']
    
    # Conectar a la base de datos
    conn = pyodbc.connect(CONNECTION_STRING)
    # Crear un cursor
    cur = conn.cursor()
    #cur.execute("SELECT * FROM Usuarios2 WHERE email = %s AND contraseña = %s", (email, password))
    #cursor.execute("{CALL Eliminar (?)}", (parametro2))
    cur.execute("SELECT * FROM Usuarios2 WHERE email = (?) AND contraseña = (?)", (email,password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is not None:
        session['email'] = user[3]
        session['name'] = user[1]
        session['surnames'] = user[2]
        #return render_template('index.html', message="Las credenciales son correctas - email: " + user[3] + ", nombre: " + user[1] + ", apellido: " + user[2])
        return redirect(url_for('tasks'))
    else:
        return render_template('index.html', message="Las credenciales no son correctas")
    
@app.route('/tasks', methods=['GET'])
def tasks():
    email = session['email']
    # Conectar a la base de datos
    conn = pyodbc.connect(CONNECTION_STRING)
    # Crear un cursor
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE email = (?)", (email))
    tasks = cur.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in tasks:
        insertObject.append(dict(zip(columnNames, record)))
    
    cur.close()
    conn.close()
    
    return render_template('tasks.html', tasks = insertObject)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/new-task', methods=['POST'])
def newTask():
    title = request.form['title']
    description = request.form['description']
    email = session['email']
    dateTask = datetime.now()

    if title and description and email:
        # Conectar a la base de datos
        conn = pyodbc.connect(CONNECTION_STRING)
        # Crear un cursor
        cur = conn.cursor()
        sql = "INSERT INTO tasks (email, titulo, descripcion, fecha_tasks) VALUES (?,?,?,?)"
        data = (email, title, description, dateTask)
        cur.execute(sql, data)
        #cur.execute("INSERT INTO tasks (descripcion) VALUES (?)", (description))
        # Confirmar los cambios si el procedimiento almacenado realiza alguna operación de escritura
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('tasks'))

@app.route('/new-user', methods=['POST'])
def newUser():
    name = request.form['name']
    surnames = request.form['surnames']
    email = request.form['email']
    password = request.form['password']

    if name and surnames and email and password:
        # Conectar a la base de datos
        conn = pyodbc.connect(CONNECTION_STRING)
        # Crear un cursor
        cur = conn.cursor()
        sql = "INSERT INTO Usuarios2 (nombre, apellido, email, contraseña) VALUES (?,?,?,?)"
        data = (name, surnames, email, password)
        cur.execute(sql, data)
        # Confirmar los cambios si el procedimiento almacenado realiza alguna operación de escritura
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('tasks'))

@app.route("/delete-task", methods=["POST"])
def deleteTask():
    # Conectar a la base de datos
    conn = pyodbc.connect(CONNECTION_STRING)
    # Crear un cursor
    cur = conn.cursor()
    id = request.form['id']
    sql = "DELETE FROM tasks WHERE id = (?)"
    data = (id)
    cur.execute(sql, data)
    # Confirmar los cambios si el procedimiento almacenado realiza alguna operación de escritura
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)