from data_loader import DataLoader

class Menu:
    def __init__(self):
        self.reiniciar_estado()
        self.data_loader = DataLoader()
        self.features = []
        self.target = None

        self.opciones_estado = {
            "1. Cargar datos": "cargar_datos",
            "2. Preprocesado de datos": "preprocesar_datos",
            "3. Visualización de datos": "visualizar_datos",
            "4. Exportar datos": "exportar_datos",
        }

        self.subopciones_estado = {
            "2.1 Selección de columnas": "seleccionar_columnas",
            "2.2 Manejo de datos faltantes": "manejo_datos_faltantes",
            "2.3 Transformación de datos categóricos": "transformacion_categoricos",
            "2.4 Normalización y escalado": "normalizacion_escalado",
            "2.5 Detección y manejo de valores atípicos": "deteccion_atipicos",
        }

    def reiniciar_estado(self):
        self.estado = {
            "cargar_datos": False,
            "preprocesar_datos": False,
            "visualizar_datos": False,
            "exportar_datos": False,
        }

        self.estado_subopciones = {
            "seleccionar_columnas": False,
            "manejo_datos_faltantes": False,
            "transformacion_categoricos": False,
            "normalizacion_escalado": False,
            "deteccion_atipicos": False,
        }

    def menu(self):
        print("=============================")
        print("Menú Principal")
        print("=============================")

        # Mostrar opción de cargar datos
        print(self.habilitado("1. Cargar datos", True))

        if self.estado["cargar_datos"]:
            # Si todas las subopciones están completadas (por ejemplo, detección_atipicos), habilitar Preprocesado
            if all(self.estado_subopciones.values()):
                print(self.habilitado("2. Preprocesado de datos", True))
            else:
                print(self.habilitado("2. Preprocesado de datos", False))

            # Mostrar subopciones de preprocesado siguiendo el flujo de habilitación
            print("    " + self.habilitado("2.1 Selección de columnas", self.estado_subopciones["seleccionar_columnas"]))
            print("    " + self.habilitado("2.2 Manejo de datos faltantes", self.estado_subopciones["manejo_datos_faltantes"]))
            print("    " + self.habilitado("2.3 Transformación de datos categóricos", self.estado_subopciones["transformacion_categoricos"]))
            print("    " + self.habilitado("2.4 Normalización y escalado", self.estado_subopciones["normalizacion_escalado"]))
            print("    " + self.habilitado("2.5 Detección y manejo de valores atípicos", self.estado_subopciones["deteccion_atipicos"]))
        else:
            print(self.habilitado("2. Preprocesado de datos", False))


        # Las opciones de visualización y exportación solo se habilitan cuando se haya completado detección de atípicos
        if self.estado_subopciones["deteccion_atipicos"]:
            print(self.habilitado("3. Visualización de datos", True))
            print(self.habilitado("4. Exportar datos", True))
        else:
            print(self.habilitado("3. Visualización de datos", False))
            print(self.habilitado("4. Exportar datos", False))

        # Mostrar opción de salir
        print("[✓] 5. Salir")

        
    def habilitado(self, texto, hab):
        clave_estado = self.opciones_estado.get(texto, None)  # Buscar clave en el diccionario de opciones
        if clave_estado is None:  # Si es una subopción, buscar en el diccionario de subopciones
            clave_estado = self.subopciones_estado.get(texto, None)
        
        if clave_estado is None:
            return texto  # Si la opción no está en los diccionarios, devolver el texto tal cual

        if self.estado.get(clave_estado, False) or self.estado_subopciones.get(clave_estado, False):
            return f"[✓] {texto}"  # La opción o subopción ya se completó
        elif hab:
            return f"[-] {texto}"  # Se habilita la opción si está en el estado correcto
        else:
            return f"[✗] {texto}"  # La opción está bloqueada
    
    def opciones(self, opcion):
        if opcion == "1":
            self.cargar_datos()
        elif opcion == "2" and self.estado["cargar_datos"]:
            self.seleccionar_columnas()
        elif opcion == "3" and self.estado["preprocesar_datos"]:
            self.estado["visualizar_datos"] = True
        elif opcion == "4" and self.estado["preprocesar_datos"]:
            self.estado["exportar_datos"] = True
        elif opcion == "5":
            return self.salir()
        else:
            print("Opción no válida o bloqueada. Intente nuevamente.")
        return True
    
    def salir(self):
        while True:
            print("=============================")
            print("Salir de la Aplicación")
            print("=============================")
            print("¿Está seguro de que desea salir?")
            print("  [1] Sí")
            print("  [2] No")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print("\n Cerrando la aplicación...")
                return False
            elif opcion == "2":
                print("\n Regresando al menú principal...")
                return True
            else:
                print("Opción no válida. Intente nuevamente.")

    def cargar_datos(self):
        if self.estado["cargar_datos"]:
            print("Los datos ya han sido cargados. No puedes volver a realizar esta acción.")
            return
        print("=============================")
        print("Carga de Datos")
        print("=============================")
        print("Seleccione el tipo de archivo a cargar:")
        print("  [1] CSV")
        print("  [2] Excel")
        print("  [3] SQLite")
        print("  [4] Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            archivo = input("Ingrese la ruta del archivo CSV: ")
            self.data_loader.cargar_csv(archivo)
        elif opcion == "2":
            archivo = input("Ingrese la ruta del archivo Excel: ")
            self.data_loader.cargar_excel(archivo)
        elif opcion == "3":
            archivo = input("Ingrese la ruta de la base de datos SQLite: ")
            self.data_loader.cargar_sqlite(archivo)
        elif opcion == "4":
            return
        else:
            print("Opción no válida. Intente nuevamente.")
            return
        if self.data_loader.dataset is not None:
            self.data_loader.mostrar_informacion()
            self.estado["cargar_datos"] = True

    def seleccionar_columnas(self):
        print("=============================")
        print("Selección de Columnas")
        print("=============================")
        columnas = list(self.data_loader.dataset.columns)
        for i, col in enumerate(columnas, 1):
            print(f"  [{i}] {col}")

        try:
            features_input = input("Ingrese los números de las columnas de entrada (features), separados por comas: ")
            features_idx = list(map(int, features_input.split(',')))
            self.features = [columnas[i - 1] for i in features_idx]

            target_input = input("Ingrese el número de la columna de salida (target): ")
            target_idx = int(target_input)
            self.target = columnas[target_idx - 1]

            if self.target in self.features:
                raise ValueError("El target no puede estar en las features.")

            print(f"Selección guardada: Features = {self.features}, Target = {self.target}")
            self.estado["preprocesar_datos"] = True
            self.estado_subopciones["seleccionar_columnas"] = True
        except (ValueError, IndexError):
            print("⚠ Error: Debe seleccionar al menos una feature y un único target que no esté en las features.")
            self.features = []
            self.target = None

    def iniciar(self):
        while True:
            self.menu()
            opcion = input("Seleccione una opción: ")
            if not self.opciones(opcion):
                break

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar()
