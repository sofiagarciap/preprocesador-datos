import pandas as pd

class PreprocesadoDatos:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.features = []
        self.target = None

    def seleccionar_columnas(self, features_input, target_input):
        features_input = [int(x.strip()) for x in features_input.split(",")]
        columnas = list(self.data_loader.dataset.columns)

        self.features = [columnas[i - 1] for i in features_input]
        self.target = columnas[target_input - 1]

    def manejo_valores_faltantes(self):
        df = self.data_loader.dataset
        columnas_a_revisar = self.features + [self.target]

        faltantes = df[columnas_a_revisar].isnull().sum()
        columnas_con_faltantes = faltantes[faltantes > 0]

        print("=============================")
        print("Manejo de Valores Faltantes")
        print("=============================")

        if columnas_con_faltantes.empty:
            print("No se han detectado valores faltantes en las columnas seleccionadas.")
            return True

        print("Se han detectado valores faltantes en las siguientes columnas seleccionadas:")
        for col, count in columnas_con_faltantes.items():
            print(f"  - {col}: {count} valores faltantes")

        while True:
            print("\nSeleccione una estrategia para manejar los valores faltantes:")
            print("  [1] Eliminar filas con valores faltantes")
            print("  [2] Rellenar con la media de la columna")
            print("  [3] Rellenar con la mediana de la columna")
            print("  [4] Rellenar con la moda de la columna")
            print("  [5] Rellenar con un valor constante")
            print("  [6] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.data_loader.dataset = df.dropna(subset=columnas_a_revisar)
                print("Filas con valores faltantes eliminadas.")
                return True

            elif opcion == "2":
                for col in columnas_con_faltantes.index:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        media = df[col].mean()
                        df[col] = df[col].fillna(media)
                    else:
                        print(f"⚠ No se puede calcular la media para la columna '{col}' (no numérica).")
                print("Valores faltantes rellenados con la media de cada columna numérica.")
                return True

            elif opcion == "3":
                for col in columnas_con_faltantes.index:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        mediana = df[col].median()
                        df[col] = df[col].fillna(mediana)
                    else:
                        print(f"⚠ No se puede calcular la mediana para la columna '{col}' (no numérica).")
                print("Valores faltantes rellenados con la mediana de cada columna numérica.")
                return True

            elif opcion == "4":
                for col in columnas_con_faltantes.index:
                    moda = df[col].mode()
                    if not moda.empty:
                        df[col] = df[col].fillna(moda[0])
                print("Valores faltantes rellenados con la moda de cada columna.")
                return True

            elif opcion == "5":
                try:
                    constante = input("Seleccione un valor para reemplazar los valores faltantes: ")
                    for col in columnas_con_faltantes.index:
                        df[col] = df[col].fillna(constante)
                    print(f"Valores faltantes reemplazados con el valor '{constante}'.")
                    return True
                except Exception as e:
                    print(f"⚠ Error: {e}")
            elif opcion == "6":
                return False
            else:
                print("Opción no válida. Intente nuevamente.")
