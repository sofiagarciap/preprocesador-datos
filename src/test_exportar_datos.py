import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from io import StringIO
import builtins

from exportador_datos import ExportarDatos


class TestExportarDatos(unittest.TestCase):

    def setUp(self):
        data = {'col1': [1, 2], 'col2': [3, 4]}
        self.df = pd.DataFrame(data)
        self.exportador = ExportarDatos(self.df)

    @patch("builtins.input", side_effect=["1", "archivo_csv"])
    @patch("pandas.DataFrame.to_csv")
    def test_exportar_csv(self, mock_to_csv, mock_input):
        self.exportador.exportar()
        mock_to_csv.assert_called_once_with("archivo_csv.csv", index=False)

    @patch("builtins.input", side_effect=["2", "archivo_excel"])
    @patch("pandas.DataFrame.to_excel")
    def test_exportar_excel(self, mock_to_excel, mock_input):
        self.exportador.exportar()
        mock_to_excel.assert_called_once_with("archivo_excel.xlsx", index=False)

    @patch("builtins.input", side_effect=["3"])
    def test_volver_al_menu(self, mock_input):
        # No exporta, solo sale del menú
        with patch("pandas.DataFrame.to_csv") as mock_csv, patch("pandas.DataFrame.to_excel") as mock_excel:
            self.exportador.exportar()
            mock_csv.assert_not_called()
            mock_excel.assert_not_called()

    @patch("builtins.input", side_effect=["9", "3"])  # opción inválida, luego salir
    def test_opcion_invalida(self, mock_input):
        with patch("pandas.DataFrame.to_csv") as mock_csv, patch("pandas.DataFrame.to_excel") as mock_excel:
            self.exportador.exportar()
            mock_csv.assert_not_called()
            mock_excel.assert_not_called()

if __name__ == "__main__":
    unittest.main()
