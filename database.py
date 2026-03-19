import sqlite3
from datetime import datetime

DB_NAME = "asistencia_escolar.db"

def obtener_conexion():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_db():
    conn = obtener_conexion()
    cursor = conn.cursor()

    # --- USUARIOS (OK) ---
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

    # --- ROLES (CORREGIDO: Agregada Auditoría) ---
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

    # --- USUARIO ROLES (OK) ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS UsuarioRoles (
        id_usuario_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_rol INTEGER,
        fecha_asignacion TEXT,
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
        FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
    )''')

    # --- CENTROS (CORREGIDO: Nombres de columnas unificados con el Grid) ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Centros (
        id_centro INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_centro TEXT NOT NULL,
        universidad_inst TEXT,
        estado INTEGER DEFAULT 1,
        usuario_crea INTEGER,
        fecha_creacion TEXT,
        usuario_modifica INTEGER,
        fecha_modificacion TEXT,
        FOREIGN KEY (usuario_crea) REFERENCES Usuarios(id_usuario)
    )''')
    # 1. Aseguramos que los roles existan
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Admin', 'Acceso total')")
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Docente', 'Gestión de asistencia')")
    cursor.execute("INSERT OR IGNORE INTO Roles (nombre_rol, descripcion) VALUES ('Creador', 'Nivel máximo de acceso al sistema')")
    
    # 2. Insertamos tu usuario: RafaelTeach
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT OR IGNORE INTO Usuarios (username, password_hash, email, p_nombre, estado, fecha_creacion) 
                      VALUES ('RafaelTeach', 'Mezapineda1993#$%', 'rafael@teach.com', 'Rafael Meza', 1, ?)''', (fecha_hoy,))
    
    # 3. Asignamos el rol 'Creador' a 'RafaelTeach'
    cursor.execute('''INSERT OR IGNORE INTO UsuarioRoles (id_usuario, id_rol, fecha_asignacion)
                      SELECT u.id_usuario, r.id_rol, ? FROM Usuarios u, Roles r 
                      WHERE u.username = 'RafaelTeach' AND r.nombre_rol = 'Creador' ''', (fecha_hoy,))
    # ... resto de inserciones (Roles y Usuarios iniciales) ...
    conn.commit()
    conn.close()
# --- FUNCIONES GENÉRICAS DE AUDITORÍA ---

def ejecutar_query(query, parametros=(), identity_id=None, es_insercion=True):
    """
    Simula el 'SaveChanges' de EF agregando automáticamente los datos de auditoría.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convertimos a lista para poder mutar los parámetros
    params = list(parametros)
    params.append(identity_id)
    params.append(ahora)

    cursor.execute(query, params)
    conn.commit()
    conn.close()

# --- CRUD PARA CENTROS ---

def insertar_centro(nombre, universidad, id_usuario_activo):
    query = '''INSERT INTO Centros (nombre_centro, universidad_inst, usuario_crea, fecha_creacion, estado) 
               VALUES (?, ?, ?, ?, 1)'''
    ejecutar_query(query, (nombre, universidad), id_usuario_activo)

def actualizar_centro(id_centro, nombre, universidad, id_usuario_activo):
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''UPDATE Centros 
                      SET nombre_centro = ?, universidad_inst = ?, usuario_modifica = ?, fecha_modificacion = ?
                      WHERE id_centro = ?''', 
                   (nombre, universidad, id_usuario_activo, ahora, id_centro))
    conn.commit()
    conn.close()

def obtener_centros_activos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_centro, nombre_centro, universidad_inst FROM Centros WHERE estado = 1")
    datos = cursor.fetchall()
    conn.close()
    return datos

def desactivar_centro(id_centro, id_usuario_activo):
    """Soft Delete: Solo cambia el estado y registra quién lo hizo."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''UPDATE Centros 
                      SET estado = 0, usuario_modifica = ?, fecha_modificacion = ?
                      WHERE id_centro = ?''', 
                   (id_usuario_activo, ahora, id_centro))
    conn.commit()
    conn.close()

def login_usuario(username, password):
    """Retorna el id_usuario si las credenciales son válidas."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, p_nombre FROM Usuarios WHERE username = ? AND password_hash = ? AND estado = 1", 
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    return user # Retorna (id, nombre) o None
def verificar_duplicado_centro(nombre, universidad, excluir_id=None):
    """
    Verifica si ya existe un centro con ese nombre e institución.
    Si se pasa excluir_id, ignora ese ID (útil para cuando estamos editando).
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Si excluir_id tiene valor (estamos editando), buscamos duplicados que NO sean el mismo registro
    if excluir_id is not None:
        cursor.execute('''SELECT COUNT(*) FROM Centros 
                          WHERE nombre_centro = ? AND universidad_inst = ? AND estado = 1 AND id_centro != ?''', 
                       (nombre, universidad, excluir_id))
    else:
        # Si es un registro nuevo
        cursor.execute('''SELECT COUNT(*) FROM Centros 
                          WHERE nombre_centro = ? AND universidad_inst = ? AND estado = 1''', 
                       (nombre, universidad))
    
    existe = cursor.fetchone()[0] > 0
    conn.close()
    return existe

def obtener_todos_centros():
    """Retorna todos los centros con los NOMBRES de los usuarios de auditoría"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Usamos LEFT JOIN para que, si no hay modificador (es NULL), el registro siempre aparezca
    query = """
        SELECT 
            c.id_centro, 
            c.nombre_centro, 
            c.universidad_inst, 
            c.estado, 
            c.fecha_creacion, 
            u1.username as creado_por, 
            c.fecha_modificacion, 
            u2.username as modificado_por
        FROM Centros c
        LEFT JOIN Usuarios u1 ON c.usuario_crea = u1.id_usuario
        LEFT JOIN Usuarios u2 ON c.usuario_modifica = u2.id_usuario
    """
    cursor.execute(query)
    filas = cursor.fetchall()
    conn.close()
    return filas
def activar_centro(id_centro, usuario_id):
    """Cambia el estado de un centro a 1 (Activo)"""
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE centros SET estado = 1, modificado_por = ? WHERE id = ?"
    cursor.execute(query, (usuario_id, id_centro))
    conn.commit()
    conn.close()
def obtener_rol_usuario(id_usuario):
    """Busca el rol del usuario en la tabla UsuarioRoles"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT r.nombre_rol FROM Roles r
        JOIN UsuarioRoles ur ON r.id_rol = ur.id_rol
        WHERE ur.id_usuario = ?
    """
    cursor.execute(query, (id_usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Docente"
# Inicializar al importar
inicializar_db()