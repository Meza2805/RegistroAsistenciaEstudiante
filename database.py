import sqlite3
import os
from datetime import datetime

DB_NAME = "asistencia_escolar.db"

def obtener_conexion():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_db(recrear=False):
    """
    Inicializa la estructura de la base de datos.
    Si recrear es True, elimina el archivo físico para empezar de cero.
    """
    if recrear and os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            print(">>> Base de datos eliminada y recreada exitosamente.")
        except PermissionError:
            print(">>> Error: No se pudo eliminar la DB. Asegúrate de que la app esté cerrada.")

    conn = obtener_conexion()
    cursor = conn.cursor()

    # --- TABLA: USUARIOS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE,
        p_nombre TEXT,
        p_apellido TEXT,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT
    )''')

    # --- TABLA: ROLES ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Roles (
        id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_rol TEXT UNIQUE NOT NULL,
        descripcion TEXT,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT
    )''')

    # --- TABLA: USUARIO ROLES ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS UsuarioRoles (
        id_usuario_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_rol INTEGER,
        fecha_asignacion TEXT,
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
        FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
    )''')

    # --- TABLA: CENTROS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Centros (
        id_centro INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_centro TEXT NOT NULL,
        universidad_inst TEXT,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario),
        UNIQUE(nombre_centro, universidad_inst)
    )''')

    # --- TABLA: AÑOS LECTIVOS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Anios_Lectivos (
        id_anio INTEGER PRIMARY KEY AUTOINCREMENT,
        etiqueta TEXT UNIQUE NOT NULL,
        activo INTEGER DEFAULT 0,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario)
    )''')

    # --- TABLA: FACULTADES ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Facultades (
        id_facultad INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro INTEGER,
        nombre_facultad TEXT NOT NULL,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (id_centro) REFERENCES Centros(id_centro),
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario)
    )''')

    # --- TABLA: ASIGNATURAS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Asignaturas (
        id_asignatura INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_asignatura TEXT UNIQUE NOT NULL,
        codigo_asignatura TEXT UNIQUE,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario)
    )''')

    # --- TABLA: TURNOS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Turnos (
        id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_turno TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario),
        UNIQUE(nombre_turno, hora_inicio, hora_fin)
    )''')

    # --- SEMILLAS (DATA INICIAL) ---
    # CORRECCIÓN AQUÍ: Cambiado 'dummy' por 'descripcion'
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Admin', 'Acceso total')")
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Docente', 'Gestión de asistencia')")
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Creador', 'Nivel máximo de acceso al sistema')")
    
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT OR IGNORE INTO Usuarios (username, password_hash, email, p_nombre, estado, fecha_creacion) 
                      VALUES ('RafaelTeach', 'Mezapineda1993#$%', 'rafael@teach.com', 'Rafael Meza', 1, ?)''', (fecha_hoy,))
    
    cursor.execute('''INSERT OR IGNORE INTO UsuarioRoles (id_usuario, id_rol, fecha_asignacion)
                      SELECT u.id_usuario, r.id_rol, ? FROM Usuarios u, Roles r 
                      WHERE u.username = 'RafaelTeach' AND r.nombre_rol = 'Creador' ''', (fecha_hoy,))

    conn.commit()
    conn.close()

# --- SEGURIDAD ---
def login_usuario(username, password):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, p_nombre FROM Usuarios WHERE username = ? AND password_hash = ? AND estado = 1", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def obtener_rol_usuario(id_usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''SELECT r.nombre_rol FROM Roles r JOIN UsuarioRoles ur ON r.id_rol = ur.id_rol WHERE ur.id_usuario = ?''', (id_usuario,))
    rol = cursor.fetchone()
    conn.close()
    return rol[0] if rol else "Docente"

# --- CRUD CENTROS ---
def insertar_centro(nombre, universidad, id_usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Centros (nombre_centro, universidad_inst, usuario_crea, fecha_creacion) VALUES (?, ?, ?, ?)', (nombre, universidad, id_usuario, ahora))
    conn.commit()
    conn.close()

def actualizar_centro(id_centro, nombre, universidad, id_usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Centros SET nombre_centro=?, universidad_inst=?, usuario_modifica=?, fecha_modificacion=? WHERE id_centro=?', (nombre, universidad, id_usuario, ahora, id_centro))
    conn.commit()
    conn.close()

def obtener_todos_centros():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT c.id_centro, c.nombre_centro, c.universidad_inst, c.estado, c.fecha_creacion, u1.username, c.fecha_modificacion, u2.username FROM Centros c LEFT JOIN Usuarios u1 ON c.usuario_crea = u1.id_usuario LEFT JOIN Usuarios u2 ON c.usuario_modifica = u2.id_usuario')
    datos = cursor.fetchall()
    conn.close()
    return datos

def desactivar_centro(id_c, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Centros SET estado=0, usuario_modifica=?, fecha_modificacion=? WHERE id_centro=?', (id_u, ahora, id_c))
    conn.commit()
    conn.close()

def activar_centro(id_c, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Centros SET estado=1, usuario_modifica=?, fecha_modificacion=? WHERE id_centro=?', (id_u, ahora, id_c))
    conn.commit()
    conn.close()

def verificar_duplicado_centro(nombre, uni, excluir_id=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    if excluir_id:
        cursor.execute('SELECT COUNT(*) FROM Centros WHERE nombre_centro=? AND universidad_inst=? AND id_centro!=?', (nombre, uni, excluir_id))
    else:
        cursor.execute('SELECT COUNT(*) FROM Centros WHERE nombre_centro=? AND universidad_inst=?', (nombre, uni))
    existe = cursor.fetchone()[0] > 0
    conn.close()
    return existe

# --- CRUD AÑOS LECTIVOS ---
def obtener_todos_anios():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT a.id_anio, a.etiqueta, a.activo, a.estado, a.fecha_creacion, u1.username, a.fecha_modificacion, u2.username FROM Anios_Lectivos a LEFT JOIN Usuarios u1 ON a.usuario_crea = u1.id_usuario LEFT JOIN Usuarios u2 ON a.usuario_modifica = u2.id_usuario')
    datos = cursor.fetchall()
    conn.close()
    return datos

def insertar_anio(etiq, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Anios_Lectivos (etiqueta, usuario_crea, fecha_creacion, estado) VALUES (?, ?, ?, 1)', (etiq, id_u, ahora))
    conn.commit()
    conn.close()

def actualizar_anio(id_a, etiq, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Anios_Lectivos SET etiqueta=?, usuario_modifica=?, fecha_modificacion=? WHERE id_anio=?', (etiq, id_u, ahora, id_a))
    conn.commit()
    conn.close()

def desactivar_anio(id_a, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Anios_Lectivos SET estado=0, usuario_modifica=?, fecha_modificacion=? WHERE id_anio=?', (id_u, ahora, id_a))
    conn.commit()
    conn.close()

def activar_anio(id_a, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Anios_Lectivos SET estado=1, usuario_modifica=?, fecha_modificacion=? WHERE id_anio=?', (id_u, ahora, id_a))
    conn.commit()
    conn.close()

def establecer_anio_actual(id_a, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Anios_Lectivos SET activo = 0')
    cursor.execute('UPDATE Anios_Lectivos SET activo = 1, usuario_modifica=?, fecha_modificacion=? WHERE id_anio=?', (id_u, ahora, id_a))
    conn.commit()
    conn.close()

def verificar_duplicado_anio(etiq, excluir_id=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    if excluir_id:
        cursor.execute('SELECT COUNT(*) FROM Anios_Lectivos WHERE etiqueta=? AND id_anio!=?', (etiq, excluir_id))
    else:
        cursor.execute('SELECT COUNT(*) FROM Anios_Lectivos WHERE etiqueta=?', (etiq,))
    res = cursor.fetchone()[0] > 0
    conn.close()
    return res

# --- CRUD ASIGNATURAS ---
def obtener_todas_asignaturas():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''SELECT a.id_asignatura, a.nombre_asignatura, a.codigo_asignatura, a.estado, 
                             a.fecha_creacion, u1.username, a.fecha_modificacion, u2.username 
                      FROM Asignaturas a 
                      LEFT JOIN Usuarios u1 ON a.usuario_crea = u1.id_usuario 
                      LEFT JOIN Usuarios u2 ON a.usuario_modifica = u2.id_usuario''')
    datos = cursor.fetchall()
    conn.close()
    return datos

def insertar_asignatura(nom, cod, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Asignaturas (nombre_asignatura, codigo_asignatura, usuario_crea, fecha_creacion) VALUES (?, ?, ?, ?)', (nom, cod, id_u, ahora))
    conn.commit()
    conn.close()

def actualizar_asignatura(id_as, nom, cod, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Asignaturas SET nombre_asignatura=?, codigo_asignatura=?, usuario_modifica=?, fecha_modificacion=? WHERE id_asignatura=?', (nom, cod, id_u, ahora, id_as))
    conn.commit()
    conn.close()

def desactivar_asignatura(id_as, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Asignaturas SET estado=0, usuario_modifica=?, fecha_modificacion=? WHERE id_asignatura=?', (id_u, ahora, id_as))
    conn.commit()
    conn.close()

def activar_asignatura(id_as, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Asignaturas SET estado=1, usuario_modifica=?, fecha_modificacion=? WHERE id_asignatura=?', (id_u, ahora, id_as))
    conn.commit()
    conn.close()

def verificar_duplicado_asignatura(nom, cod, excluir_id=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    if excluir_id:
        cursor.execute('SELECT COUNT(*) FROM Asignaturas WHERE (nombre_asignatura=? OR codigo_asignatura=?) AND id_asignatura!=?', (nom, cod, excluir_id))
    else:
        cursor.execute('SELECT COUNT(*) FROM Asignaturas WHERE nombre_asignatura=? OR codigo_asignatura=?', (nom, cod))
    res = cursor.fetchone()[0] > 0
    conn.close()
    return res

# --- CRUD TURNOS ---
def obtener_todos_turnos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, t.estado, 
                             t.fecha_creacion, u1.username, t.fecha_modificacion, u2.username 
                      FROM Turnos t 
                      LEFT JOIN Usuarios u1 ON t.usuario_crea = u1.id_usuario 
                      LEFT JOIN Usuarios u2 ON t.usuario_modifica = u2.id_usuario''')
    datos = cursor.fetchall()
    conn.close()
    return datos

def insertar_turno(nom, ini, fin, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Turnos (nombre_turno, hora_inicio, hora_fin, usuario_crea, fecha_creacion) VALUES (?, ?, ?, ?, ?)', (nom, ini, fin, id_u, ahora))
    conn.commit()
    conn.close()

def actualizar_turno(id_t, nom, ini, fin, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Turnos SET nombre_turno=?, hora_inicio=?, hora_fin=?, usuario_modifica=?, fecha_modificacion=? WHERE id_turno=?', (nom, ini, fin, id_u, ahora, id_t))
    conn.commit()
    conn.close()

def desactivar_turno(id_t, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Turnos SET estado=0, usuario_modifica=?, fecha_modificacion=? WHERE id_turno=?', (id_u, ahora, id_t))
    conn.commit()
    conn.close()

def activar_turno(id_t, id_u):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE Turnos SET estado=1, usuario_modifica=?, fecha_modificacion=? WHERE id_turno=?', (id_u, ahora, id_t))
    conn.commit()
    conn.close()

def verificar_duplicado_turno(nom, ini, fin, excluir_id=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    if excluir_id:
        cursor.execute('''SELECT COUNT(*) FROM Turnos 
                          WHERE nombre_turno=? AND hora_inicio=? AND hora_fin=? AND id_turno!=?''', 
                       (nom, ini, fin, excluir_id))
    else:
        cursor.execute('''SELECT COUNT(*) FROM Turnos 
                          WHERE nombre_turno=? AND hora_inicio=? AND hora_fin=?''', 
                       (nom, ini, fin))
    res = cursor.fetchone()[0] > 0
    conn.close()
    return res

# =============================================================================
# CONTROL DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    # Si ejecutas "py database.py", se borra y recrea TODO.
    inicializar_db(recrear=True)
else:
    # Si lo importa main.py, solo asegura que las tablas existan (sin borrar nada).
    inicializar_db(recrear=False)