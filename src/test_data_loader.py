import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from io import StringIO

from data_loader import DataLoader  

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        """Crea un objeto DataLoader antes de cada prueba."""
        self.dataloader = DataLoader()

    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_cargar_csv_exito(self, mock_read_csv, mock_exists):
        """Prueba la carga de un archivo CSV exitoso."""
        mock_exists.return_value = True
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        archivo = "archivo.csv"
        self.dataloader.cargar_csv(archivo)

        # Verificar que el dataset se cargó correctamente
        self.assertIsNotNone(self.dataloader.dataset)
        self.assertEqual(self.dataloader.dataset.shape, (3, 2))

    @patch('os.path.exists')
    def test_cargar_csv_no_existente(self, mock_exists):
        """Prueba el caso en que el archivo CSV no existe."""
        mock_exists.return_value = False

        archivo = "archivo_no_existente.csv"
        resultado = self.dataloader.cargar_csv(archivo)

        # Verificar que no se cargó nada
        self.assertIsNone(resultado)

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_cargar_excel_exito(self, mock_read_excel, mock_exists):
        """Prueba la carga de un archivo Excel exitoso."""
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        archivo = "archivo.xlsx"
        self.dataloader.cargar_excel(archivo)

        # Verificar que el dataset se cargó correctamente
        self.assertIsNotNone(self.dataloader.dataset)
        self.assertEqual(self.dataloader.dataset.shape, (3, 2))

    @patch('os.path.exists')
    def test_cargar_excel_no_existente(self, mock_exists):
        """Prueba el caso en que el archivo Excel no existe."""
        mock_exists.return_value = False

        archivo = "archivo_no_existente.xlsx"
        resultado = self.dataloader.cargar_excel(archivo)

        # Verificar que no se cargó nada
        self.assertIsNone(resultado)

    @patch('os.path.exists', return_value=True)
    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='1')  # Simula selección tabla 1
    def test_cargar_sqlite_exito(self, mock_input, mock_read_sql, mock_connect, mock_exists):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Simular dos lecturas: una para tablas y otra para datos
        mock_read_sql.side_effect = [
            pd.DataFrame({'name': ['mi_tabla']}),  # lista de tablas
            pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})  # contenido de tabla
        ]

        self.dataloader.cargar_sqlite("fake_path.sqlite")

        self.assertIsNotNone(self.dataloader.dataset)
        self.assertEqual(self.dataloader.dataset.shape, (2, 2))


    @patch('os.path.exists')
    def test_cargar_sqlite_no_existente(self, mock_exists):
        """Prueba el caso en que la base de datos SQLite no existe."""
        mock_exists.return_value = False

        archivo = "base_no_existente.sqlite"
        resultado = self.dataloader.cargar_sqlite(archivo)

        # Verificar que no se cargó nada
        self.assertIsNone(resultado)

    @patch('builtins.print')
    def test_mostrar_informacion_con_datos(self, mock_print):
        """Prueba la función de mostrar información cuando hay datos cargados."""
        self.dataloader.dataset = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        self.dataloader.mostrar_informacion()

        # Verificar que la información se mostró
        mock_print.assert_any_call("Primeras 5 filas:")
        self.assertTrue(any("   col1" in str(call) for call in mock_print.call_args_list))

        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_mostrar_informacion_sin_datos(self, mock_print):
        """Prueba la función de mostrar información cuando no hay datos cargados."""
        self.dataloader.dataset = None
        self.dataloader.mostrar_informacion()

        # Verificar que se muestra el mensaje de no haber datos
        mock_print.assert_called_with("No se ha cargado ningún conjunto de datos.")

    @patch('os.path.exists', return_value=True)
    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    @patch('builtins.input', return_value='1')  # Simula selección tabla 1
    def test_cargar_sqlite_seleccion_tabla(self, mock_input, mock_read_sql, mock_connect, mock_exists):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        mock_read_sql.side_effect = [
            pd.DataFrame({'name': ['mi_tabla']}),  # tabla disponible
            pd.DataFrame({'col1': [10, 20], 'col2': [30, 40]})  # datos de la tabla
        ]

        self.dataloader.cargar_sqlite("fake_path.sqlite")

        self.assertIsNotNone(self.dataloader.dataset)
        self.assertEqual(list(self.dataloader.dataset.columns), ['col1', 'col2'])


    @patch('builtins.input', side_effect=['2'])
    @patch('os.path.exists')
    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    def test_cargar_sqlite_seleccion_invalida(self, mock_read_sql, mock_connect, mock_exists, mock_input):
        """Prueba el caso de selección de tabla inválida en SQLite."""
        mock_exists.return_value = True
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_read_sql.return_value = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        archivo = "base_datos.sqlite"
        self.dataloader.cargar_sqlite(archivo)

        # Verificar que el dataset no se cargó
        self.assertIsNone(self.dataloader.dataset)

if __name__ == '__main__':
    unittest.main()
