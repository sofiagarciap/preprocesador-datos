import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib.pyplot as plt
from visualizador_datos import VisualizadorDatos  

class TestVisualizadorDatos(unittest.TestCase):

    def setUp(self):
        self.datos_originales = pd.DataFrame({
            'num1': [1, 2, 3, 4, 5],
            'num2': [5, 4, 3, 2, 1],
            'cat1': ['A', 'B', 'A', 'B', 'C']
        })

        self.datos_preprocesados = pd.DataFrame({
            'num1': [0.0, 0.25, 0.5, 0.75, 1.0],
            'num2': [1.0, 0.75, 0.5, 0.25, 0.0],
            'cat1': ['A', 'B', 'A', 'B', 'C']
        })

        self.columnas_numericas = ['num1', 'num2']
        self.columnas_categoricas = ['cat1']
        self.columnas_seleccionadas = self.columnas_numericas + self.columnas_categoricas

        self.visualizador = VisualizadorDatos(
            self.datos_originales,
            self.datos_preprocesados,
            self.columnas_seleccionadas,
            self.columnas_numericas,
            self.columnas_categoricas
        )

    @patch('builtins.print')
    def test_visualizar_resumen_estadistico(self, mock_print):
        self.visualizador.visualizar_resumen_estadistico()
        self.assertTrue(mock_print.called)

    @patch('matplotlib.pyplot.show')
    def test_visualizar_histogramas(self, mock_show):
        self.visualizador.visualizar_histogramas()
        self.assertEqual(mock_show.call_count, len(self.columnas_numericas))

    @patch('matplotlib.pyplot.show')
    def test_visualizar_dispersion(self, mock_show):
        self.visualizador.visualizar_dispersion()
        self.assertEqual(mock_show.call_count, len(self.columnas_numericas) - 1)

    @patch('matplotlib.pyplot.show')
    def test_visualizar_heatmap(self, mock_show):
        self.visualizador.visualizar_heatmap()
        mock_show.assert_called_once()

    @patch('builtins.input', side_effect=['5'])
    @patch('builtins.print')
    def test_menu_visualizacion_exit(self, mock_print, mock_input):
        self.visualizador.menu_visualizacion()
        self.assertTrue(mock_input.called)

if __name__ == '__main__':
    unittest.main()
