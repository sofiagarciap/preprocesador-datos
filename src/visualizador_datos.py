import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class VisualizadorDatos:
    def __init__(self, datos_originales, datos_preprocesados, columnas_seleccionadas, columnas_numericas, columnas_categoricas):
        self.datos_originales = datos_originales
        self.datos_preprocesados = datos_preprocesados
        self.columnas_seleccionadas = columnas_seleccionadas
        self.columnas_numericas = columnas_numericas
        self.columnas_categoricas = columnas_categoricas

    def menu_visualizacion(self):
        while True:
            print("\n" + "=" * 30)
            print("Visualización de Datos")
            print("=" * 30)
            print("Seleccione qué tipo de visualización desea generar:")
            print("  [1] Resumen estadístico de las variables seleccionadas")
            print("  [2] Histogramas de variables numéricas")
            print("  [3] Gráficos de dispersión antes y después de la normalización")
            print("  [4] Heatmap de correlación de variables numéricas")
            print("  [5] Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.visualizar_resumen_estadistico()
            elif opcion == "2":
                self.visualizar_histogramas()
            elif opcion == "3":
                self.visualizar_dispersion()
            elif opcion == "4":
                self.visualizar_heatmap()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def visualizar_resumen_estadistico(self):
        print("\nResumen estadístico de las variables seleccionadas:")
        print("-" * 50)
        if self.columnas_numericas:
            print("\nVariables numéricas:")
            print(self.datos_preprocesados[self.columnas_numericas].describe(percentiles=[.25, .5, .75]))
        if self.columnas_categoricas:
            print("\nDistribución de variables categóricas:")
            for col in self.columnas_categoricas:
                print(f"\n{col}:\n{self.datos_preprocesados[col].value_counts()}")

    def visualizar_histogramas(self):
        for columna in self.columnas_numericas:
            plt.figure(figsize=(8, 4))
            sns.histplot(self.datos_preprocesados[columna], bins=20, kde=True)
            plt.title(f"Histograma de {columna} (Después del preprocesado)")
            plt.xlabel(columna)
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.show()

    def visualizar_dispersion(self):
        if len(self.columnas_numericas) < 2:
            print("Se necesitan al menos dos variables numéricas para generar gráficos de dispersión.")
            return
        for i in range(len(self.columnas_numericas)-1):
            x = self.columnas_numericas[i]
            y = self.columnas_numericas[i+1]

            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            axes[0].scatter(self.datos_originales[x], self.datos_originales[y], alpha=0.5, color='orange')
            axes[0].set_title(f"Antes de normalizar: {x} vs {y}")
            axes[1].scatter(self.datos_preprocesados[x], self.datos_preprocesados[y], alpha=0.5, color='blue')
            axes[1].set_title(f"Después de normalizar: {x} vs {y}")
            for ax in axes:
                ax.set_xlabel(x)
                ax.set_ylabel(y)
            plt.tight_layout()
            plt.show()

    def visualizar_heatmap(self):
        correlaciones = self.datos_preprocesados[self.columnas_numericas].corr()
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlaciones, annot=True, cmap="coolwarm", linewidths=0.5)
        plt.title("Heatmap de correlación entre variables numéricas")
        plt.tight_layout()
        plt.show()