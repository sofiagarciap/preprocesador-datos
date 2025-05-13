import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class VisualizadorDatos:
    """
    Clase para visualizar datos originales y preprocesados.

    Proporciona opciones para visualizar:
        - Estadísticas descriptivas
        - Histogramas
        - Gráficos de dispersión antes y después de la normalización
        - Mapa de calor de correlación

    Atributos:
        datos_originales (pd.DataFrame): Dataset antes del preprocesamiento.
        datos_preprocesados (pd.DataFrame): Dataset después del preprocesamiento.
        columnas_seleccionadas (list): Columnas seleccionadas como variables de entrada.
        columnas_numericas (list): Columnas numéricas identificadas.
        columnas_categoricas (list): Columnas categóricas identificadas.
    """
    def __init__(self, datos_originales, datos_preprocesados, columnas_seleccionadas, columnas_numericas, columnas_categoricas):
        """
        Inicializa el visualizador con los datasets y la información de las columnas.
        """
        self.datos_originales = datos_originales
        self.datos_preprocesados = datos_preprocesados
        self.columnas_seleccionadas = columnas_seleccionadas
        self.columnas_numericas = columnas_numericas
        self.columnas_categoricas = columnas_categoricas

    def menu_visualizacion(self):
        """
        Muestra un menú interactivo para seleccionar el tipo de visualización deseada.
        Ejecuta el método correspondiente según la opción elegida.
        """
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
        """
        Muestra un resumen estadístico de las variables seleccionadas.
        Incluye medidas para variables numéricas y frecuencias para categóricas.
        """
        print("\nResumen estadístico de las variables seleccionadas:")
        print("-" * 50)
        # Muestra estadísticas de columnas numéricas
        if self.columnas_numericas:
            print("\nVariables numéricas:")
            print(self.datos_preprocesados[self.columnas_numericas].describe(percentiles=[.25, .5, .75]))
        # Muestra conteo de categorías para cada columna categórica
        if self.columnas_categoricas:
            print("\nDistribución de variables categóricas:")
            for col in self.columnas_categoricas:
                print(f"\n{col}:\n{self.datos_preprocesados[col].value_counts()}")

    def visualizar_histogramas(self):
        """
        Genera histogramas con KDE (estimación de densidad) para las variables numéricas preprocesadas.
        """
        for columna in self.columnas_numericas:
            plt.figure(figsize=(8, 4))
            sns.histplot(self.datos_preprocesados[columna], bins=20, kde=True)
            plt.title(f"Histograma de {columna} (Después del preprocesado)")
            plt.xlabel(columna)
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.show()

    def visualizar_dispersion(self):
        """
        Muestra gráficos de dispersión para pares de variables numéricas:
        - Comparación entre los datos originales y los normalizados.
        """
        if len(self.columnas_numericas) < 2:
            print("Se necesitan al menos dos variables numéricas para generar gráficos de dispersión.")
            return
        # Crea gráficos para cada par consecutivo de columnas numéricas
        for i in range(len(self.columnas_numericas)-1):
            x = self.columnas_numericas[i]
            y = self.columnas_numericas[i+1]

            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            # Dispersión antes del preprocesamiento
            axes[0].scatter(self.datos_originales[x], self.datos_originales[y], alpha=0.5, color='orange')
            axes[0].set_title(f"Antes de normalizar: {x} vs {y}")
            # Dispersión después del preprocesamiento
            axes[1].scatter(self.datos_preprocesados[x], self.datos_preprocesados[y], alpha=0.5, color='blue')
            axes[1].set_title(f"Después de normalizar: {x} vs {y}")
            for ax in axes:
                ax.set_xlabel(x)
                ax.set_ylabel(y)
            plt.tight_layout()
            plt.show()

    def visualizar_heatmap(self):
        """
        Genera un mapa de calor (heatmap) con la matriz de correlación de las variables numéricas.
        """
        correlaciones = self.datos_preprocesados[self.columnas_numericas].corr()
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlaciones, annot=True, cmap="coolwarm", linewidths=0.5)
        plt.title("Heatmap de correlación entre variables numéricas")
        plt.tight_layout()
        plt.show()