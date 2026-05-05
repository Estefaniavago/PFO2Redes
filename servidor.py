from flask import Flask, request, jsonify
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

DATABASE = "database.db"


# -----------------------------
# Crear base de datos
# -----------------------------
def crear_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# -----------------------------
# Endpoint: Registro
# -----------------------------
@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    # Hashear contraseña
    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )

        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 400


# -----------------------------
# Endpoint: Login
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT contraseña FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        contraseña_hash = resultado[0]

        if bcrypt.check_password_hash(contraseña_hash, contraseña):
            return jsonify({"mensaje": "Login exitoso"}), 200

    return jsonify({"error": "Credenciales incorrectas"}), 401


# -----------------------------
# Endpoint: Tareas (HTML simple)
# -----------------------------
@app.route('/tareas', methods=['GET'])
def tareas():
    return """
    <h1>Bienvenido al sistema de gestión de tareas</h1>
    <p>Si ves esto, la API está funcionando correctamente 🚀</p>
    """


# -----------------------------
# Main
# -----------------------------
if __name__ == '__main__':
    crear_db()
    app.run(debug=True)