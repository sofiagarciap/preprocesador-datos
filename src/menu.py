class Menu:
    def __init__(self):
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
        print(self.opcion_estado("1. Cargar datos", True))
        print(self.opcion_estado("2. Preprocesado de datos", self.estado["cargar_datos"]))
        print(self.opcion_estado("3. Visualización de datos", self.estado["preprocesar_datos"]))
        print(self.opcion_estado("4. Exportar datos", self.estado["preprocesar_datos"]))
        print("[✓] 5. Salir")
        
    def opcion_estado(self, texto, habilitado):
        if habilitado:
            return f"[-] {texto}"
        elif self.estado.get(texto.split(". ")[1].replace(" ", "_"), False):
            return f"[✓] {texto}"
        else:
            return f"[✗] {texto}"
    
    def opciones(self, opcion):
        if opcion == "1":
            pass
            #self.estado["cargar_datos"] = True
        elif opcion == "2" and self.estado["cargar_datos"]:
            print("Preprocesando datos...")
            self.estado["preprocesar_datos"] = True
        elif opcion == "3" and self.estado["preprocesar_datos"]:
            print("Mostrando visualización de datos...")
            self.estado["visualizar_datos"] = True
        elif opcion == "4" and self.estado["preprocesar_datos"]:
            print("Exportando datos...")
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
    
    def iniciar(self):
        while True:
            self.menu()
            opcion = input("Seleccione una opción: ")
            if not self.opciones(opcion):
                break

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar()