from data_loader import DataLoader

class Menu:
    def __init__(self):
        self.reiniciar_estado()
        self.data_loader = DataLoader()

    def reiniciar_estado(self):
        self.estado = {
            "cargar_datos": False,
            "preprocesar_datos": False,
            "visualizar_datos": False,
            "exportar_datos": False
        }
    
    def menu(self):
        print("=============================")
        print("Menú Principal")
        print("=============================")
        print(self.habilitado("1. Cargar datos", True))
        print(self.habilitado("2. Preprocesado de datos", self.estado["cargar_datos"]))
        print(self.habilitado("3. Visualización de datos", self.estado["preprocesar_datos"]))
        print(self.habilitado("4. Exportar datos", self.estado["preprocesar_datos"]))
        print("[✓] 5. Salir")
        
    def habilitado(self, texto, hab):
        clave_estado = texto.split(". ")[1].replace(" ", "_").lower() 
        if self.estado.get(clave_estado, False):
            return f"[✓] {texto}"  # 🔹 La opción ya se completó
        elif hab:
            return f"[-] {texto}"  # 🔹 Se habilita solo la opción correcta en el orden correcto
        else:
            return f"[✗] {texto}"  # 🔹 La opción está bloqueada
    
    def opciones(self, opcion):
        if opcion == "1":
            self.cargar_datos()
        elif opcion == "2" and self.estado["cargar_datos"]:
            self.estado["preprocesar_datos"] = True
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

    
    
    def iniciar(self):
        while True:
            self.menu()
            opcion = input("Seleccione una opción: ")
            if not self.opciones(opcion):
                break

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar()