import pandas as pd

class ExportarDatos:
    def __init__(self, dataset):
        self.dataset = dataset

    def exportar(self):
        print("=============================")
        print("Exportación de Datos")
        print("=============================")

        while True:
            print("Seleccione el formato de exportación:")
            print("  [1] CSV (.csv)")
            print("  [2] Excel (.xlsx)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
                self.dataset.to_csv(f"{nombre_archivo}.csv", index=False)
                print(f'Datos exportados correctamente como "{nombre_archivo}.csv".\n')
                return
            elif opcion == "2":
                nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
                self.dataset.to_excel(f"{nombre_archivo}.xlsx", index=False)
                print(f'Datos exportados correctamente como "{nombre_archivo}.xlsx".\n')
                return
            elif opcion == "3":
                return
            else:
                print("Opción no válida. Intente nuevamente.")
