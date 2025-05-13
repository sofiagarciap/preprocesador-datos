import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

class PreprocesadoDatos:
    """
    Clase encargada de realizar el preprocesamiento de un conjunto de datos
    cargado previamente mediante el objeto DataLoader.
    """
    def __init__(self, data_loader):
        """
        Inicializa el objeto PreprocesadoDatos con el dataset cargado.

        Parámetros:
        data_loader (DataLoader): Objeto que contiene el dataset original cargado.
        """
        self.data_loader = data_loader
        self.dataset_modificado = data_loader.dataset.copy() # Se trabaja sobre una copia del dataset original
        self.features = [] # Columnas de entrada seleccionadas
        self.columnas_numericas = [] # Subconjunto de columnas de entrada que son numéricas
        self.target = None # Columna objetivo (variable a predecir)
        self.columnas_seleccionadas = [] # Todas las columnas seleccionadas (features + target)
        self.columnas_categoricas = [] # Columnas categóricas detectadas entre las seleccionadas

    def seleccionar_columnas(self):
        """
        Permite al usuario seleccionar columnas del dataset para definir:
        - Variables de entrada (features)
        - Variable de salida (target)

        Clasifica las columnas seleccionadas en numéricas o categóricas.

        Retorna:
        bool: True si la selección fue válida, False en caso de error.
        """
        print("=============================")
        print("Selección de Columnas")
        print("=============================")
        
        columnas = list(self.data_loader.dataset.columns)
        # Muestra al usuario las columnas disponibles con su número correspondiente
        print("Columnas disponibles en los datos:")
        for i, columna in enumerate(columnas, 1):
            print(f"  [{i}] {columna}")

        try:
            # Entrada de columnas de entrada y de salida
            features_input = input("Ingrese los números de las columnas de entrada (features), separados por comas: ")
            target_input = int(input("Ingrese el número de la columna de salida (target): "))
            # Convierte la entrada de texto a índices enteros
            features_idx = [int(x.strip()) for x in features_input.split(",")]
            target_idx = int(target_input)
            # Asigna los nombres de columnas según los índices seleccionados
            self.features = [columnas[i - 1] for i in features_idx]
            self.target = columnas[target_idx - 1]
            df = self.dataset_modificado
            # Verifica que la columna target no esté dentro de las features
            if self.target in self.features:
                print("⚠ Error: La columna de salida no puede ser una feature.")
                self.features = []
                self.target = None
                return False
            else:
                # Guarda la selección total y clasifica por tipo de dato
                df = self.dataset_modificado
                self.columnas_seleccionadas = self.features + [self.target]
                # Indentifica las columnas numéricas
                self.columnas_numericas = [
                    col for col in self.columnas_seleccionadas
                    if pd.api.types.is_numeric_dtype(df[col])
                    ]
                # Identifica las columnas categóricas
                self.columnas_categoricas = [
                    col for col in self.columnas_seleccionadas
                    if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col])
                ]

                print(f"Selección guardada: Features = {self.features}, Target = {self.target}")
                return True
            
        # Gestión de entradas inválidas
        except (ValueError, IndexError):
            print("⚠ Error: Debe seleccionar columnas válidas. Intente nuevamente.")
            return False
    
    def valores_faltantes(self):
        """
        Detecta y permite tratar valores faltantes en las columnas seleccionadas (features y target)
        utilizando diferentes estrategias de imputación o eliminación.

        Retorna:
            bool: True si se aplicó alguna estrategia, False si el usuario elige salir.
        """
        df = self.dataset_modificado
        columnas_a_revisar = self.features + [self.target]
        # Cuenta los valores faltantes por columna
        faltantes = df[columnas_a_revisar].isnull().sum()
        columnas_con_faltantes = faltantes[faltantes > 0]

        print("=============================")
        print("Manejo de Valores Faltantes")
        print("=============================")

        # Si no hay valores faltantes, se informa y se termina la función
        if columnas_con_faltantes.empty:
            print("No se han detectado valores faltantes en las columnas seleccionadas.")
            return True
        
        # Muestra columnas que contienen valores faltantes y la cantidad en cada una
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

            # Opción 1: elimina cualquier fila que tenga valores faltantes en las columnas seleccionadas
            if opcion == "1":
                self.dataset_modificado = df.dropna(subset=columnas_a_revisar)
                print("Filas con valores faltantes eliminadas.")
                return True

            # Opción 2: rellena valores faltantes con la media de cada columna (solo numéricas)
            elif opcion == "2":
                for col in columnas_con_faltantes.index:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        media = df[col].mean()
                        df[col] = df[col].fillna(media)
                    else:
                        print(f"⚠ No se puede calcular la media para la columna '{col}' (no numérica).")
                print("Valores faltantes rellenados con la media de cada columna numérica.")
                return True

            # Opción 3: rellena valores faltantes con la mediana de cada columna (solo numéricas)
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

            # Opción 4: rellena valores faltantes con la moda de cada columna
            elif opcion == "4":
                for col in columnas_con_faltantes.index:
                    moda = df[col].mode()
                    if not moda.empty:
                        df[col] = df[col].fillna(moda[0])
                print("Valores faltantes rellenados con la moda de cada columna.")
                return True

            # Opción 5: rellena con un valor constante que el usuario ingrese
            elif opcion == "5":
                try:
                    constante = input("Seleccione un valor para reemplazar los valores faltantes: ")
                    for col in columnas_con_faltantes.index:
                        df[col] = df[col].fillna(constante)
                    print(f"Valores faltantes reemplazados con el valor '{constante}'.")
                    return True
                except Exception as e:
                    print(f"⚠ Error: {e}")

            # Opción 6: salir sin aplicar cambios
            elif opcion == "6":
                return False
            
            # Gestión de entradas inválidas
            else:
                print("Opción no válida. Intente nuevamente.")


    def datos_categoricos(self):
        """
        Aplica transformaciones a columnas categóricas seleccionadas como variables de entrada (features),
        utilizando técnicas de codificación como One-Hot Encoding o Label Encoding.

        Retorna:
            bool: True si se aplicó una transformación, False si el usuario eligió regresar al menú.
        """
        df = self.dataset_modificado
        # Identifica las columnas categóricas que están entre las entradas seleccionadas
        columnas_categoricas = [
            col for col in self.features
            if col in self.columnas_categoricas
        ]

        print("=============================")
        print("Transformación de Datos Categóricos")
        print("=============================")

        # Si no hay columnas categóricas, informa al usuario y finaliza
        if not columnas_categoricas:
            print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna transformación.")
            self.categoricos_transformados = True
            return True

        # Muestra al usuario las columnas categóricas encontradas
        print("Se han detectado columnas categóricas en las variables de entrada seleccionadas:")
        for col in columnas_categoricas:
            print(f"  - {col}")

        while True:
            print("\nSeleccione una estrategia de transformación:")
            print("  [1] One-Hot Encoding (genera nuevas columnas binarias)")
            print("  [2] Label Encoding (convierte categorías a números enteros)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            # Opción 1: One-Hot Encoding
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

            # Opción 2: Label Encoding
            elif opcion == "2":
                for col in columnas_categoricas:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                print("Transformación completada con Label Encoding Encoding.")
                self.categoricos_transformados = True
                return True

            # Opción 3: regresar al menú sin aplicar cambios
            elif opcion == "3":
                return False
            
            # Gestión de entradas inválidas
            else:
                print("Opción no válida. Intente nuevamente.")

    def normalizar_escalar_datos(self):
        """
        Aplica técnicas de normalización o escalado a las columnas numéricas seleccionadas como variables de entrada (features).

        Retorna:
            bool: True si se realizó una normalización, False si el usuario decidió volver al menú.
        """
        df = self.dataset_modificado
        # Filtra las columnas numéricas que están en las variables de entrada
        columnas_numericas_entrada = [
            col for col in self.features
            if col in self.columnas_numericas
        ]

        print("=============================")
        print("Normalización y Escalado")
        print("=============================")

        # Si no hay columnas numéricas, no se requiere normalización
        if not columnas_numericas_entrada:
            print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna normalización.")
            self.normalizacion_completada = True
            return True
        
        # Muestra las columnas que serán normalizadas
        print("Se han detectado columnas numéricas en las variables de entrada seleccionadas:")
        for col in columnas_numericas_entrada:
            print(f"  - {col}")

        while True:
            print("\nSeleccione una estrategia de normalización:")
            print("  [1] Min-Max Scaling (escala valores entre 0 y 1)")
            print("  [2] Z-score Normalization (media 0, desviación estándar 1)")
            print("  [3] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            # Opción 1: Min-Max Scaling
            if opcion == "1":
                scaler = MinMaxScaler()
                df[columnas_numericas_entrada] = scaler.fit_transform(df[columnas_numericas_entrada])
                print("Normalización completada con Min-Max Scaling.")
                self.normalizacion_completada = True
                
                return True

            # Opción 2: Z-score Normalization (StandardScaler)
            elif opcion == "2":
                scaler = StandardScaler()
                df[columnas_numericas_entrada] = scaler.fit_transform(df[columnas_numericas_entrada])
                print("Normalización completada con Z-score Normalization.")
                self.normalizacion_completada = True
                return True

            # Opción 3: regresar al menú sin aplicar cambios
            elif opcion == "3":
                return False
            
            # Gestión  de entradas inválidas
            else:
                print("Opción no válida. Intente nuevamente.")

    def valores_atipicos(self):
        """
        Detecta y maneja valores atípicos (outliers) en las columnas numéricas seleccionadas como variables de entrada.
        Utiliza el método del rango intercuartílico (IQR) para identificar los outliers. 

        Retorna:
            bool: True si se ejecutó una estrategia (incluso si no había outliers), False si se vuelve al menú.
        """
        df = self.dataset_modificado
        columnas_numericas = self.columnas_numericas

        print("=============================")
        print("Detección y Manejo de Valores Atípicos")
        print("=============================")

        # Si no hay columnas numéricas, no hay nada que gestionar
        if not columnas_numericas:
            print("No se han detectado columnas numéricas en las variables de entrada seleccionadas.")
            print("No es necesario aplicar ninguna estrategia.")
            self.outliers_gestionados = True
            return True

        # Detectar outliers usando el rango intercuartílico (IQR)
        valores_atipicos_por_columna = {}
        for col in columnas_numericas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
            if not outliers.empty:
                valores_atipicos_por_columna[col] = outliers.shape[0]

        # Si no hay outliers, finalizar
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

            # Opción 1: eliminar filas con outliers
            if opcion == "1":
                for col in valores_atipicos_por_columna:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    df = df[(df[col] >= (Q1 - 1.5 * IQR)) & (df[col] <= (Q3 + 1.5 * IQR))]
                self.dataset_modificado = df
                print("Filas con valores atípicos eliminadas.")
                self.outliers_gestionados = True
                return True

            # Opción 2: reemplazar outliers por la mediana
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
                print("Valores atípicos reemplazados con la mediana de cada columna.")
                self.outliers_gestionados = True
                return True

            # Opción 3: dejar los valores atípicos tal como están
            elif opcion == "3":
                print("Valores atípicos mantenidos sin cambios.")
                self.outliers_gestionados = True
                return True

            # Opción 4: salir sin hacer nada
            elif opcion == "4":
                return False
            
            # Gestión de entradas inválidas
            else:
                print("Opción no válida. Intente nuevamente.")

