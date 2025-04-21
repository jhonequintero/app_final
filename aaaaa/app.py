from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import mysql.connector
import os

# Crear la app y especificar el directorio de templates
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Configurar conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jhoneiderquintero12345@", 
    database="miapp"
)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Leer los datos enviados como JSON
    correo = data['correo']
    contrasena = data['contrasena']
    tipo = data['tipo']  # 'admin' o 'trabajador'

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



# Ruta para el panel de administrador
@app.route('/panel_admin')
def panel_admin():
    return render_template('panel_admin.html')

# Ruta para el panel de trabajador
@app.route('/panel_trabajador')
def panel_trabajador():
    return render_template('panel_trabajador.html')

# Servir archivos estáticos como CSS, JS, imágenes
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('frontend', path)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
