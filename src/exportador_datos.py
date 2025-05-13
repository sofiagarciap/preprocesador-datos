import pandas as pd

class ExportarDatos:
    """
    Clase para exportar un DataFrame a archivos en formato CSV o Excel.

    Atributos:
        dataset (pd.DataFrame): Conjunto de datos que se desea exportar.
    """
    def __init__(self, dataset):
        """
        Inicializa la clase con el DataFrame a exportar.

        Parámetros:
            dataset (pd.DataFrame): Datos a guardar en disco.
        """
        self.dataset = dataset

    def exportar(self):
        """
        Muestra un menú interactivo para exportar el dataset en distintos formatos.

        Retorna:
            bool: True si la exportación fue realizada, False si el usuario eligió volver al menú principal.
        """
        print("=============================")
        print("Exportación de Datos")
        print("=============================")

        while True:
            print("Seleccione el formato de exportación:")
            print("  [1] CSV (.csv)")
            print("  [2] Excel (.xlsx)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            # Exportar como CSV
            if opcion == "1":
                nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
                self.dataset.to_csv(f"{nombre_archivo}.csv", index=False)
                print(f'Datos exportados correctamente como "{nombre_archivo}.csv".\n')
                return True
            
            # Exportar como Excel
            elif opcion == "2":
                nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
                self.dataset.to_excel(f"{nombre_archivo}.xlsx", index=False)
                print(f'Datos exportados correctamente como "{nombre_archivo}.xlsx".\n')
                return True
            
            # Volver al menú principal
            elif opcion == "3":
                return False
            
            #Gestión de entradas inválidas
            else:
                print("Opción no válida. Intente nuevamente.")
