import pandas as pd
import sqlite3
import os

class DataLoader:
    def __init__(self):
        self.dataset = None

    def cargar_csv(self, archivo):
        if not os.path.exists(archivo):
            print("Archivo no encontrado.")
            return None
        try:
            self.dataset = pd.read_csv(archivo)
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            return None

    def cargar_excel(self, archivo):
        if not os.path.exists(archivo):
            print("Archivo no encontrado.")
            return None
        try:
            self.dataset = pd.read_excel(archivo)
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            return None

    def cargar_sqlite(self, archivo):
        if not os.path.exists(archivo):
            print("Base de datos no encontrada.")
            return None
        try:
            conn = sqlite3.connect(archivo)
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            print("Tablas disponibles en la base de datos:")
            for idx, tabla in enumerate(tablas['name'], 1):
                print(f"  [{idx}] {tabla}")
            seleccion = int(input("Seleccione una tabla: ")) - 1
            tabla_seleccionada = tablas.iloc[seleccion]['name']
            query = f"SELECT * FROM {tabla_seleccionada};"
            self.dataset = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            print(f"Error al cargar la base de datos SQLite: {e}")
            return None
        
    def mostrar_informacion(self):
        if self.dataset is not None:
            print(f"Datos cargados correctamente.")
            print(f"Número de filas: {len(self.dataset)}")
            print(f"Número de columnas: {len(self.dataset.columns)}")
            print("Primeras 5 filas:")
            print(self.dataset.head())
        else:
            print("No se ha cargado ningún conjunto de datos.")
