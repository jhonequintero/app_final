import os
from flask import Flask, render_template, request, jsonify, send_from_directory

import mysql.connector

app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Conexión usando variables de entorno
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "jhoneiderquintero12345@"),
    database=os.environ.get("DB_NAME", "miapp")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data['correo']
    contrasena = data['contrasena']
    tipo = data['tipo']

    cursor = db.cursor(dictionary=True)

    if tipo == 'admin':
        cursor.execute("SELECT * FROM Administradores WHERE correo = %s AND contrasena = %s", (correo, contrasena))
        usuario = cursor.fetchone()
        if usuario:
            return jsonify({'success': True, 'mensaje': 'Bienvenido administrador', 'redireccion': '/panel_admin'})
        else:
            return jsonify({'success': False, 'mensaje': 'Credenciales incorrectas para administrador'})

    elif tipo == 'trabajador':
        cursor.execute("SELECT * FROM Trabajadores WHERE correo = %s AND contrasena = %s", (correo, contrasena))
        usuario = cursor.fetchone()
        if usuario:
            return jsonify({'success': True, 'mensaje': 'Bienvenido trabajador', 'redireccion': '/panel_trabajador'})
        else:
            return jsonify({'success': False, 'mensaje': 'No hay trabajadores registrados con estas credenciales'})

    return jsonify({'success': False, 'mensaje': 'Tipo de usuario no válido'})

@app.route('/panel_admin')
def panel_admin():
    return render_template('panel_admin.html')

@app.route('/panel_trabajador')
def panel_trabajador():
    return render_template('panel_trabajador.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('frontend', path)

# Este bloque no se usa en Render
# if __name__ == '__main__':
#     app.run(debug=True)
