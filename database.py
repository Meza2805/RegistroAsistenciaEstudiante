import sqlite3


def inicializar_db():
    conn = sqlite3.connect("asistencia_escolar.db")
    cursor = conn.cursor()
    
    # IMPORTANTE: Activar soporte para llaves foráneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- CATÁLOGOS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Centros (
        id_centro INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_centro TEXT NOT NULL,
        universidad_inst TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Facultades (
        id_facultad INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro INTEGER,
        nombre_facultad TEXT NOT NULL,
        FOREIGN KEY (id_centro) REFERENCES Centros(id_centro))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Carreras (
        id_carrera INTEGER PRIMARY KEY AUTOINCREMENT,
        id_facultad INTEGER,
        nombre_carrera TEXT NOT NULL,
        FOREIGN KEY (id_facultad) REFERENCES Facultades(id_facultad))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Turnos (
        id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_turno TEXT UNIQUE NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Anios_Lectivos (
        id_anio INTEGER PRIMARY KEY AUTOINCREMENT,
        etiqueta TEXT UNIQUE NOT NULL,
        activo INTEGER DEFAULT 1)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Asignaturas (
        id_asignatura INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_asignatura TEXT NOT NULL)''')

    # --- PERSONAS ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Estudiantes (
        id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
        p_nombre TEXT NOT NULL, s_nombre TEXT,
        p_apellido TEXT NOT NULL, s_apellido TEXT,
        sexo TEXT, telefono TEXT, direccion TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Identidades_Academicas (
        id_identidad INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER, id_centro INTEGER,
        carnet_codigo TEXT NOT NULL,
        FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),
        FOREIGN KEY (id_centro) REFERENCES Centros(id_centro))''')

    # --- ESTRUCTURA ACADÉMICA ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Grupos (
        id_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_carrera INTEGER, nombre_grupo TEXT,
        id_turno INTEGER, id_anio INTEGER,
        FOREIGN KEY (id_carrera) REFERENCES Carreras(id_carrera),
        FOREIGN KEY (id_turno) REFERENCES Turnos(id_turno),
        FOREIGN KEY (id_anio) REFERENCES Anios_Lectivos(id_anio))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Horarios (
        id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_grupo INTEGER, id_asignatura INTEGER,
        dia_semana TEXT, hora_inicio TEXT, hora_fin TEXT, aula TEXT,
        FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo),
        FOREIGN KEY (id_asignatura) REFERENCES Asignaturas(id_asignatura))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Inscripciones (
        id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER, id_grupo INTEGER, fecha_inscripcion TEXT,
        FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),
        FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo))''')

    # --- ASISTENCIA ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS Asistencia (
        id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER, id_horario INTEGER,
        fecha TEXT, estado TEXT, observaciones TEXT,
        FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),
        FOREIGN KEY (id_horario) REFERENCES Horarios(id_horario))''')

    conn.commit()
    conn.close()

def insertar_centro(nombre, universidad):
    conn = sqlite3.connect("asistencia_escolar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Centros (nombre_centro, universidad_inst) VALUES (?, ?)", (nombre, universidad))
    conn.commit()
    conn.close()

def obtener_centros():
    conn = sqlite3.connect("asistencia_escolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Centros")
    datos = cursor.fetchall()
    conn.close()
    return datos

def eliminar_centro(id_centro):
    conn = sqlite3.connect("asistencia_escolar.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Centros WHERE id_centro = ?", (id_centro,))
    conn.commit()
    conn.close()

# Llamamos a la función para asegurar que la DB exista
inicializar_db()