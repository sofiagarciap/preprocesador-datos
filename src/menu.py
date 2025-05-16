from data_loader import DataLoader
from preprocesado_datos import PreprocesadoDatos
from visualizador_datos import VisualizadorDatos
from exportador_datos import ExportarDatos


class Menu:
    """
    Clase Menu que gestiona un pipeline interactivo de procesamiento de datos.
    
    Este menú guía al usuario a través de los pasos de:
    1. Carga de datos
    2. Preprocesamiento de datos 
    3. Visualización de datos
    4. Exportación de datos procesados

    Asegura que los pasos se realicen en orden y que cada etapa se habilite
    solo si la etapa anterior ha sido completada correctamente.
    """
    def __init__(self):
        """
        Inicializa el menú y su estado.
        """
        self.reiniciar_estado()
        self.data_loader = DataLoader()
        self.preprocesado_datos = None
        self.visualizador_datos = None
        self.exportador = None

        # Diccionarios que mapean las opciones del menú a las funciones del sistema
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
        """
        Inicializa los estados principales y de subopciones del menu como no hechos cada vez que se ejecuta el programa.
        """
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
        """
        Muestra el menú principal con opciones habilitadas o bloqueadas según el progreso del usuario en el pipeline.
        """
        print("=============================")
        print("Menú Principal")
        print("=============================")

        # Paso 1: Cargar datos siempre está habilitado
        print(self.habilitado("1. Cargar datos", True, "ningún archivo cargado"))

        # Paso 2: Preprocesamiento habilitado solo si se han cargado los datos
        if self.estado["cargar_datos"]:
            if (self.habilitado("2. Preprocesado de datos", True, "requiere carga de datos")):
                # Subopciones del preprocesamiento mostradas según estado
                print(self.habilitado("2. Preprocesado de datos", True, "requiere carga de datos"))
                print("\t" + self.habilitado("2.1 Selección de columnas", not self.estado_subopciones["seleccionar_columnas"], ""))
                print("\t" + self.habilitado("2.2 Manejo de datos faltantes", self.estado_subopciones["seleccionar_columnas"], "requiere selección de columnas"))
                print("\t" + self.habilitado("2.3 Transformación de datos categóricos", self.estado_subopciones["manejo_datos_faltantes"], "requiere manejo de valores faltantes"))
                print("\t" + self.habilitado("2.4 Normalización y escalado", self.estado_subopciones["transformacion_categoricos"], "requiere transformación categórica"))
                print("\t" + self.habilitado("2.5 Detección y manejo de valores atípicos", self.estado_subopciones["normalizacion_escalado"], "requiere normalización"))
        else:
            print(self.habilitado("2. Preprocesado de datos", False, "requiere carga de datos"))

        # Paso 3: Visualización depende de acabar todo el preprocesado
        print(self.habilitado("3. Visualización de datos", self.estado_subopciones["deteccion_atipicos"], "requiere preprocesado completo"))
        # Paso 4: Exportación depende de la visualización
        print(self.habilitado("4. Exportar datos", self.estado["visualizar_datos"], "requiere preprocesado completo"))

        # Salida del sistema
        if self.estado["exportar_datos"]:
            print("[-] 5. Salir")
        else:
            print("[✓] 5. Salir")
        

    def habilitado(self, texto, hab, error):
        """
        Devuelve un string con el texto de la opción del menú indicando si está:
        - Completada ([✓])
        - Disponible para ejecutar ([-])
        - Bloqueada ([✗])
        """
        clave_estado = self.opciones_estado.get(texto, None)  
        if clave_estado is None:  
            clave_estado = self.subopciones_estado.get(texto, None)
        
        if clave_estado is None:
            return texto  

        if self.estado.get(clave_estado, False) or self.estado_subopciones.get(clave_estado, False):
            return f"[✓] {texto} (completado)"  # La opción o subopción ya se completó
        elif hab:
            return f"[-] {texto} (pendiente)"  # Se habilita la opción si está en el estado correcto
        else:
            return f"[✗] {texto} ({error})"  # La opción está bloqueada
    
    def opciones(self, opcion):
        """
        Ejecuta la acción correspondiente a la opción seleccionada del menú.
        Controla la secuencia y validación de cada etapa del pipeline.
        """
        # Paso 1: Cargar datos
        if opcion == "1":
            self.cargar_datos()

        # Paso 2: Entrar al bloque de preprocesamiento
        elif opcion == "2" and self.estado["cargar_datos"]:
            self.estado["preprocesar_datos"] = False
        # 2.1 Selección de columnas (solo si no se han procesado faltantes aún)
        elif opcion == "2.1":
            if self.estado_subopciones["manejo_datos_faltantes"]:
                print("No se puede volver a seleccionar columnas después de comenzar el manejo de datos faltantes.")
            else:
                self.preprocesado_datos = PreprocesadoDatos(self.data_loader)
                desbloquear = self.preprocesado_datos.seleccionar_columnas()
                if desbloquear:
                    self.estado_subopciones["seleccionar_columnas"] = True # Habilita el siguiente paso
        # 2.2 Manejo de valores faltantes
        elif opcion == "2.2" and self.estado_subopciones["seleccionar_columnas"]:
            desbloquear = self.preprocesado_datos.valores_faltantes()
            if desbloquear:
                self.estado_subopciones["manejo_datos_faltantes"] = True # Habilita el siguiente paso
        # 2.3 Transformación de datos categóricos
        elif opcion == "2.3" and self.estado_subopciones["manejo_datos_faltantes"]:
            if self.estado_subopciones["transformacion_categoricos"]:
                print("No se han detectado columnas categóricas en las variables de entrada seleccionadas.")
                print("No es necesario aplicar ninguna transformación.")
            else:
                desbloquear = self.preprocesado_datos.datos_categoricos()
                if desbloquear:
                    self.estado_subopciones["transformacion_categoricos"] = True # Habilita el siguiente paso
        # 2.4 Normalización y escalado
        elif opcion == "2.4" and self.estado_subopciones["transformacion_categoricos"]:
            if self.estado_subopciones["normalizacion_escalado"]:
                print("Ya se ha aplicado la normalización en las columnas numéricas. No es necesario volver a hacerlo")
            else:
                desbloquear = self.preprocesado_datos.normalizar_escalar_datos()
                if desbloquear:
                    self.estado_subopciones["normalizacion_escalado"] = True # Habilita el siguiente paso
        # 2.5 Detección y manejo de valores atípicos
        elif opcion == "2.5" and self.estado_subopciones["normalizacion_escalado"]:
            desbloquear = self.preprocesado_datos.valores_atipicos()
            if desbloquear:
                self.estado_subopciones["deteccion_atipicos"] = True 
                self.estado["preprocesar_datos"] = True # Habilita el siguiente paso
        # Paso 3: Visualización de los datos
        elif opcion == "3" and self.estado["preprocesar_datos"] and self.estado_subopciones["deteccion_atipicos"]:
            self.visualizador_datos = VisualizadorDatos(
                self.data_loader.dataset,  # Datos originales
                self.preprocesado_datos.dataset_modificado,  # Datos preprocesados
                self.preprocesado_datos.columnas_seleccionadas,  # Columnas seleccionadas
                self.preprocesado_datos.columnas_numericas,  # Columnas numéricas
                self.preprocesado_datos.columnas_categoricas  # Columnas categóricas
            )
            self.visualizador_datos.menu_visualizacion()  # Llamar al menú de visualización
            self.estado["visualizar_datos"] = True # Habilita el siguiente paso
        # Paso 4: Exportación de datos
        elif opcion == "4" and self.estado["visualizar_datos"]:
            self.exportador = ExportarDatos(self.preprocesado_datos.dataset_modificado)
            desbloquear = self.exportador.exportar()
            if desbloquear:
                self.estado["exportar_datos"] = True # Habilita el siguiente paso
        # Paso 5: Salir del menú
        elif opcion == "5":
            return self.salir()
        else:
            print("Opción no válida o bloqueada. Intente nuevamente.")
        return True

    
    def salir(self):
        """
        Método que gestiona la confirmación para salir de la aplicación.

        Devuelve False si se confirma la salida (lo que rompe el bucle principal),
        o True si el usuario decide permanecer en la aplicación.
        """
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
                return False # Finaliza el bucle principal en `iniciar()`
            elif opcion == "2":
                print("\n Regresando al menú principal...")
                return True # Regresa al menú principal
            else:
                print("Opción no válida. Intente nuevamente.")

    def cargar_datos(self):
        """
        Método que permite al usuario cargar datos desde diferentes fuentes.

        Ofrece opciones para cargar archivos CSV, Excel o bases de datos SQLite.
        Si la carga es exitosa, actualiza el estado interno y muestra un resumen del dataset.
        """
        if self.estado["cargar_datos"]:
            # Evita recargar si ya se han cargado los datos
            print("Los datos ya han sido cargados. No puedes volver a realizar esta acción.")
            return
        # Menú
        print("=============================")
        print("Carga de Datos")
        print("=============================")
        print("Seleccione el tipo de archivo a cargar:")
        print("  [1] CSV")
        print("  [2] Excel")
        print("  [3] SQLite")
        print("  [4] Volver al menú principal")
        # Lógica de carga según tipo de archivo
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
            return # Vuelve al menú principal sin hacer nada
        else:
            print("Opción no válida. Intente nuevamente.")
            return
        
        # Verifica si el dataset fue cargado exitosamente
        if self.data_loader.dataset is not None:
            self.data_loader.mostrar_informacion()  # Muestra información básica del dataset
            self.estado["cargar_datos"] = True  # Habilita los siguientes pasos del pipeline
        

    def iniciar(self):
        """
        Método principal que inicia el ciclo de ejecución del menú.

        Muestra continuamente el menú principal y espera una opción del usuario.
        Sale del bucle solo si el usuario elige salir y lo confirma.
        """
        while True:
            self.menu() # Muestra las opciones disponibles según el estado
            opcion = input("Seleccione una opción: ")
            if not self.opciones(opcion):
                break # Sale si `opciones()` devuelve False (caso de salir)

# Programa principal
if __name__ == "__main__":
    menu = Menu()
    menu.iniciar()