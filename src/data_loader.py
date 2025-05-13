import pandas as pd
import sqlite3
import os

class DataLoader:
    """
    Clase responsable de cargar conjuntos de datos desde distintos formatos:
    CSV, Excel y bases de datos SQLite. También proporciona una función para mostrar
    información básica del dataset cargado.
    """
    def __init__(self):
        """
        Inicializa el objeto DataLoader con un dataset vacío.
        """
        self.dataset = None

    def cargar_csv(self, archivo):
        """
        Carga un archivo CSV y lo asigna al atributo `dataset`.

        Parámetros:
        archivo (str): Ruta al archivo CSV.
        """
        if not os.path.exists(archivo):
            print("Archivo no encontrado.")
            return None
        try:
            self.dataset = pd.read_csv(archivo) # Intenta leer el archivo CSV con pandas
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            return None

    def cargar_excel(self, archivo):
        """
        Carga un archivo Excel y lo asigna al atributo `dataset`.

        Parámetros:
        archivo (str): Ruta al archivo Excel.
        """
        if not os.path.exists(archivo):
            print("Archivo no encontrado.")
            return None
        try:
            self.dataset = pd.read_excel(archivo) # Intenta leer el archivo Excel con pandas
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            return None

    def cargar_sqlite(self, archivo):
        """
        Carga datos desde una base de datos SQLite, permitiendo al usuario
        seleccionar una tabla disponible en la base de datos.

        Parámetros:
        archivo (str): Ruta al archivo de base de datos SQLite.
        """
        if not os.path.exists(archivo):
            print("Base de datos no encontrada.")
            return None
        try:
            conn = sqlite3.connect(archivo) # Se establece conexión con la base de datos SQLite
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn) # Consulta para obtener el listado de tablas
            print("Tablas disponibles en la base de datos:")
            for idx, tabla in enumerate(tablas['name'], 1):
                print(f"  [{idx}] {tabla}")
            # Se solicita al usuario que seleccione una tabla
            seleccion = int(input("Seleccione una tabla: ")) - 1
            tabla_seleccionada = tablas.iloc[seleccion]['name']
            # Se consulta y carga el contenido de la tabla seleccionada
            query = f"SELECT * FROM {tabla_seleccionada};"
            self.dataset = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            print(f"Error al cargar la base de datos SQLite: {e}")
            return None
        
    def mostrar_informacion(self):
        """
        Muestra un resumen informativo del dataset cargado:
        - Número de filas
        - Número de columnas
        - Primeras 5 filas del dataset
        """
        if self.dataset is not None:
            print(f"Datos cargados correctamente.")
            print(f"Número de filas: {len(self.dataset)}")
            print(f"Número de columnas: {len(self.dataset.columns)}")
            print("Primeras 5 filas:")
            print(self.dataset.head())
        else:
            print("No se ha cargado ningún conjunto de datos.")
