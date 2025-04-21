import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import psycopg2
import psycopg2.extras

app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Configuración directa de la conexión PostgreSQL (datos de Render)
DB_HOST = "dpg-d034rpbe5dus73cbr0n0-a.oregon-postgres.render.com"
DB_NAME = "app_final_db"
DB_USER = "admin_app"
DB_PASSWORD = "w95Ec0BeVbhRZrPNx7D0Ae1fWzWpSvVV"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
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

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if tipo == 'admin':
        cursor.execute("SELECT * FROM Administradores WHERE correo = %s AND contrasena = %s", (correo, contrasena))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return jsonify({'success': True, 'mensaje': 'Bienvenido administrador', 'redireccion': '/panel_admin'})
        else:
            return jsonify({'success': False, 'mensaje': 'Credenciales incorrectas para administrador'})

    elif tipo == 'trabajador':
        cursor.execute("SELECT * FROM Trabajadores WHERE correo = %s AND contrasena = %s", (correo, contrasena))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return jsonify({'success': True, 'mensaje': 'Bienvenido trabajador', 'redireccion': '/panel_trabajador'})
        else:
            return jsonify({'success': False, 'mensaje': 'No hay trabajadores registrados con estas credenciales'})

    conn.close()
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

# Si estás probando localmente puedes descomentar esto:
# if __name__ == '__main__':
#     app.run(debug=True)
