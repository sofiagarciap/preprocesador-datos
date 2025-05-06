import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

class PreprocesadoDatos:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.dataset_modificado = data_loader.dataset.copy() 
        self.features = []
        self.columnas_numericas = []
        self.target = None
        self.columnas_seleccionadas = []
        self.columnas_categoricas = []

    def seleccionar_columnas(self, features_input, target_input):
        features_input = [int(x.strip()) for x in features_input.split(",")]
        columnas = list(self.data_loader.dataset.columns)

        self.features = [columnas[i - 1] for i in features_input]
        self.target = columnas[target_input - 1]
        df = self.dataset_modificado


        self.columnas_seleccionadas = self.features + [self.target]
        # Guardamos solo las columnas numéricas originales (antes de cualquier transformación)
        self.columnas_numericas = [
            col for col in self.columnas_seleccionadas
            if pd.api.types.is_numeric_dtype(df[col])
            ]
        self.columnas_categoricas = [
            col for col in self.columnas_seleccionadas
            if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col])
        ]

    def valores_faltantes(self):
        df = self.dataset_modificado
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
                self.dataset_modificado = df.dropna(subset=columnas_a_revisar)
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
                        print(mediana)
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


    def datos_categoricos(self):
        df = self.dataset_modificado
        columnas_categoricas = [
            col for col in self.features
            if col in self.columnas_categoricas
        ]

        print("=============================")
        print("Transformación de Datos Categóricos")
        print("=============================")

        if not columnas_categoricas:
            print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna transformación.")
            self.categoricos_transformados = True
            return True

        print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
        for col in columnas_categoricas:
            print(f"  - {col}")

        while True:
            print("\nSeleccione una estrategia de transformación:")
            print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
            print("  [2] Label Encoding (convierte categorías a números enteros)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                df_transformado = pd.get_dummies(df, columns=columnas_categoricas)
                columnas_dummies = [col for col in df_transformado.columns if df_transformado[col].dtype == 'bool']
                df_transformado[columnas_dummies] = df_transformado[columnas_dummies].astype(int)
                self.dataset_modificado = df_transformado
                
                nuevas_columnas = list(df_transformado.columns)
                nuevas_features = []

                for f in self.features:
                    if f == self.target:
                        continue
                    elif f in nuevas_columnas:
                        nuevas_features.append(f)  
                    elif f in columnas_categoricas:
                          nuevas_features.extend([col for col in nuevas_columnas if col.startswith(f + "_") or col == f])

                self.features = nuevas_features
                self.columnas_categoricas = [
                    col for col in nuevas_features
                    if any(orig + "_" in col for orig in columnas_categoricas)
                ]
                print("Transformación completada con One-Hot Encoding.")
                self.categoricos_transformados = True
                return True

            elif opcion == "2":
                for col in columnas_categoricas:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                print("Transformación completada con Label Encoding Encoding.")
                self.categoricos_transformados = True
                return True

            elif opcion == "3":
                return False
            else:
                print("Opción no válida. Intente nuevamente.")

    def normalizar_escalar_datos(self):
        df = self.dataset_modificado
        columnas_numericas_entrada = [
            col for col in self.features
            if col in self.columnas_numericas
        ]

        print("=============================")
        print("Normalización y Escalado")
        print("=============================")

        if not columnas_numericas_entrada:
            print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna normalización.")
            self.normalizacion_completada = True
            return True

        print("Se han detectado columnas numéricas en las variables de entrada seleccionadas:")
        for col in columnas_numericas_entrada:
            print(f"  - {col}")

        while True:
            print("\nSeleccione una estrategia de normalización:")
            print("  [1] Min-Max Scaling (escala valores entre 0 y 1)")
            print("  [2] Z-score Normalization (media 0, desviación estándar 1)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                scaler = MinMaxScaler()
                df[columnas_numericas_entrada] = scaler.fit_transform(df[columnas_numericas_entrada])
                print("Normalización completada con Min-Max Scaling.")
                self.normalizacion_completada = True
                
                return True

            elif opcion == "2":
                scaler = StandardScaler()
                df[columnas_numericas_entrada] = scaler.fit_transform(df[columnas_numericas_entrada])
                print("Normalización completada con Z-score Normalization.")
                self.normalizacion_completada = True
                return True

            elif opcion == "3":
                return False
            else:
                print("Opción no válida. Intente nuevamente.")

    def valores_atipicos(self):
        df = self.dataset_modificado
        columnas_numericas = self.columnas_numericas

        print("=============================")
        print("Detección y Manejo de Valores Atípicos")
        print("=============================")

        if not columnas_numericas:
            print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.outliers_gestionados = True
            return True

        valores_atipicos_por_columna = {}
        for col in columnas_numericas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
            if not outliers.empty:
                valores_atipicos_por_columna[col] = outliers.shape[0]

        if not valores_atipicos_por_columna:
            print("No se han detectado valores atípicos en las columnas seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.outliers_gestionados = True
            return True

        print("Se han detectado valores atípicos en las siguientes columnas numéricas seleccionadas:")
        for col, count in valores_atipicos_por_columna.items():
            print(f"  - {col}: {count} valores atípicos detectados")

        while True:
            print("\nSeleccione una estrategia para manejar los valores atípicos:")
            print("  [1] Eliminar filas con valores atípicos")
            print("  [2] Reemplazar valores atípicos con la mediana de la columna")
            print("  [3] Mantener valores atípicos sin cambios")
            print("  [4] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                for col in valores_atipicos_por_columna:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    df = df[(df[col] >= (Q1 - 1.5 * IQR)) & (df[col] <= (Q3 + 1.5 * IQR))]
                self.dataset_modificado = df
                print(df.head())
                print("Filas con valores atípicos eliminadas.")
                self.outliers_gestionados = True
                return True

            elif opcion == "2":
                for col in valores_atipicos_por_columna:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    mediana = df[col].median()
                    df[col] = df[col].apply(lambda x: mediana if x < lower_bound or x > upper_bound else x)
                self.dataset_modificado = df
                print(df.head())
                print("Valores atípicos reemplazados con la mediana de cada columna.")
                self.outliers_gestionados = True
                return True

            elif opcion == "3":
                print("Valores atípicos mantenidos sin cambios.")
                self.outliers_gestionados = True
                return True

            elif opcion == "4":
                return False

            else:
                print("Opción no válida. Intente nuevamente.")

