import unittest 
from unittest.mock import patch
import pandas as pd
import numpy as np

from preprocesado_datos import PreprocesadoDatos  

class DummyDataLoader:
    def __init__(self, dataset):
        self.dataset = dataset

class TestSeleccionarColumnas(unittest.TestCase):

    def setUp(self):
        # Crear un DataFrame simulado
        data = pd.DataFrame({
            'PassengerId': [1, 2, 3, 4, 5, 6, 7],
            'Survived': [0, 1, 1, 1, 0, 0, 0],
            'Pclass': [3, 1, 3, 1, 3, 3, 1],
            'Name': [
                'Braund, Mr. Owen Harris', 
                'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 
                'Heikkinen, Miss. Laina', 
                'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 
                'Allen, Mr. William Henry',
                'Moran, Mr. James',
                'McCarthy, Mr. Timothy J'
            ],
            'Sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male'],
            'Age': [22, 38, 26, 35, 35, np.nan, 54], #valor faltante
            'SibSp': [1, 1, 0, 1, 0, 0, 0],
            'Parch': [0, 0, 0, 0, 0, 0, 0],
            'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450', '330877', '17463'],
            'Fare': [7.25, 71.2833, 7.925, 53.1, 8.05, 8.4583, 1000], #valor atipico
            'Cabin': [np.nan, 'C85', np.nan, 'C123', np.nan, np.nan, 'E46'],
            'Embarked': ['S', 'C', 'S', 'S', 'S', 'Q', 'S']
        })

        self.df = pd.DataFrame(data)
        self.data_loader = DummyDataLoader(self.df)
        self.preprocesador = PreprocesadoDatos(self.data_loader)

    def seleccionar_columnas_manual(self, features, target):
        self.preprocesador.features = features
        self.preprocesador.target = target
        self.preprocesador.dataset_modificado = self.df.copy()

    @patch('builtins.input', side_effect=["1,3", "4"])  # Selecciona columnas 1 y 3 como 'features' y columna 4 como 'target'
    def test_seleccion_valida(self, mock_input):
        result = self.preprocesador.seleccionar_columnas()
        self.assertTrue(result)
        self.assertEqual(self.preprocesador.features, ['PassengerId', 'Pclass'])  # Features seleccionadas
        self.assertEqual(self.preprocesador.target, 'Name')  # Target seleccionado
        # Comprobamos que las columnas numéricas contienen 'PassengerId' y 'Pclass' y no 'Name'
        self.assertIn('PassengerId', self.preprocesador.columnas_numericas)
        self.assertIn('Pclass', self.preprocesador.columnas_numericas)
        self.assertNotIn('Name', self.preprocesador.columnas_numericas)
        # Comprobamos que las columnas categóricas contienen 'Name' y no 'PassengerId' y 'Pclass'.
        self.assertIn('Name', self.preprocesador.columnas_categoricas)
        self.assertNotIn('PassengerId', self.preprocesador.columnas_categoricas)
        self.assertNotIn('Pclass', self.preprocesador.columnas_categoricas)

    @patch('builtins.input', side_effect=["1,4", "4"])  # Selecciona la columna 1 y 4 como 'features' pero target 4 también es una feature
    def test_target_en_features(self, mock_input):
        result = self.preprocesador.seleccionar_columnas()
        self.assertFalse(result)  # La función debe devolver False ya que no se puede seleccionar el target como feature
        self.assertEqual(self.preprocesador.features, [])  # No deben quedar 'features' seleccionadas
        self.assertIsNone(self.preprocesador.target)  # El target debe ser None

    @patch('builtins.input', side_effect=["15,2", "1"])  # Intentamos seleccionar una columna fuera de rango
    def test_indices_fuera_de_rango(self, mock_input):
        result = self.preprocesador.seleccionar_columnas()
        self.assertFalse(result)  # Se debe devolver False si se selecciona un índice fuera de rango

    @patch('builtins.input', side_effect=["a,b", "2"])  # Entrada no válida para las columnas
    def test_entrada_invalida(self, mock_input):
        result = self.preprocesador.seleccionar_columnas()
        self.assertFalse(result)  # La entrada no válida debe dar False

    @patch('builtins.input', side_effect=["1,2", "3, 4"])  # Intentamos seleccionar dos columnas como target
    def test_target_no_especificado(self, mock_input):
        result = self.preprocesador.seleccionar_columnas()
        self.assertFalse(result)  # No se puede seleccionar más de un target

    
    ########## Valores Faltantes #############

    
    def test_eliminar_filas_con_faltantes(self):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')

        before = len(self.preprocesador.dataset_modificado)
        with patch('builtins.input', side_effect=["1"]):  # Eliminar
            result = self.preprocesador.valores_faltantes()
            self.assertTrue(result)
            after = len(self.preprocesador.dataset_modificado)
            self.assertLess(after, before)

    def test_rellenar_con_media(self):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')

        with patch('builtins.input', side_effect=["2"]):  # Rellenar con media
            result = self.preprocesador.valores_faltantes()
            self.assertTrue(result)
            self.assertFalse(self.preprocesador.dataset_modificado['Age'].isnull().any())

    @patch('builtins.input', side_effect=["3"])  # Rellenar con la mediana
    def test_rellenar_con_mediana(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        resultado = self.preprocesador.valores_faltantes()
        self.assertTrue(resultado)
        self.assertEqual(self.preprocesador.dataset_modificado['Age'].isnull().sum(), 0)
        esperado = self.df['Age'].median(skipna=True)
        self.assertEqual(self.preprocesador.dataset_modificado.loc[5, 'Age'], esperado)

    @patch('builtins.input', side_effect=["4"])  # Rellenar con la moda
    def test_rellenar_con_moda(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        resultado = self.preprocesador.valores_faltantes()
        self.assertTrue(resultado)
        self.assertEqual(self.preprocesador.dataset_modificado['Age'].isnull().sum(), 0)
        esperado = self.df['Age'].mode()[0]
        self.assertEqual(self.preprocesador.dataset_modificado.loc[5, 'Age'], esperado)

    @patch('builtins.input', side_effect=["5", "99"])  # Rellenar con constante
    def test_rellenar_con_constante(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        resultado = self.preprocesador.valores_faltantes()
        self.assertTrue(resultado)
        self.assertEqual(self.preprocesador.dataset_modificado['Age'].isnull().sum(), 0)
        self.assertEqual(self.preprocesador.dataset_modificado.loc[5, 'Age'], "99")


    @patch('builtins.input', side_effect=["6"])  # Cancelar operación
    def test_cancelar_estrategia(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        resultado = self.preprocesador.valores_faltantes()
        self.assertFalse(resultado)
        self.assertEqual(self.preprocesador.dataset_modificado['Age'].isnull().sum(), 1)


    def test_sin_valores_faltantes(self):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        self.preprocesador.dataset_modificado['Age'] = self.preprocesador.dataset_modificado['Age'].fillna(30)
        resultado = self.preprocesador.valores_faltantes()
        self.assertTrue(resultado)

    ########## Manejo de Datos Categóricos #############
    
    def test_one_hot_encoding(self):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        self.preprocesador.columnas_categoricas = ['Sex', 'Name']

        with patch('builtins.input', side_effect=["1"]):  # One-hot encoding
            result = self.preprocesador.datos_categoricos()
            self.assertTrue(result)
            cols = self.preprocesador.dataset_modificado.columns
            self.assertTrue(any('Sex_' in col for col in cols))
            self.assertTrue(all(col in self.preprocesador.features for col in cols if col.startswith("Sex_")))


    def test_label_encoding(self):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        self.preprocesador.columnas_categoricas = ['Sex', 'Name']

        with patch('builtins.input', side_effect=["2"]):  # Label encoding
            result = self.preprocesador.datos_categoricos()
            self.assertTrue(result)
            self.assertTrue(pd.api.types.is_integer_dtype(self.preprocesador.dataset_modificado['Sex']))

    @patch('builtins.input', side_effect=["3"])  # Cancelar
    def test_cancelar_transformacion(self, mock_input):
        self.seleccionar_columnas_manual(['Sex', 'Age'], 'Name')
        self.preprocesador.columnas_categoricas = ['Sex', 'Name']

        resultado = self.preprocesador.datos_categoricos()
        self.assertFalse(resultado)

    def test_sin_columnas_categoricas(self):
        self.seleccionar_columnas_manual(['Age'], 'Name')
        self.preprocesador.columnas_categoricas = ['Name']

        resultado = self.preprocesador.datos_categoricos()
        self.assertTrue(resultado)
        self.assertTrue(self.preprocesador.categoricos_transformados)

    ########## Normalización y Escalado de Datos Numéricos ##########

    @patch('builtins.input', side_effect=["1"])  # Min-Max Scaling
    def test_min_max_scaling(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Fare')
        self.preprocesador.columnas_numericas = ['Age', 'Fare']
        fare_original = self.preprocesador.dataset_modificado['Fare'].copy()

        result = self.preprocesador.normalizar_escalar_datos()
        self.assertTrue(result)

        age = self.preprocesador.dataset_modificado['Age']
        self.assertGreaterEqual(age.min(), 0)
        self.assertLessEqual(age.max(), 1)

        fare_modificado = self.preprocesador.dataset_modificado['Fare']
        pd.testing.assert_series_equal(fare_original, fare_modificado) #Los valores de 'Fare' no se modifican por ser una salida




    @patch('builtins.input', side_effect=["2"])  # Z-score Normalization
    def test_z_score_normalization(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Name')
        self.preprocesador.columnas_numericas = ['Age', 'Fare']

        result = self.preprocesador.normalizar_escalar_datos()
        self.assertTrue(result)

        age = self.preprocesador.dataset_modificado['Age']
        self.assertAlmostEqual(age.mean(), 0, delta=0.1)
        self.assertAlmostEqual(age.std(), 1, delta=0.1)


    @patch('builtins.input', side_effect=["3"])  # Cancelar
    def test_cancelar_normalizacion(self, mock_input):
        self.seleccionar_columnas_manual(['Age', 'Sex'], 'Fare')
        self.preprocesador.columnas_numericas = ['Age', 'Fare']

        result = self.preprocesador.normalizar_escalar_datos()
        self.assertFalse(result)


    def test_sin_columnas_numericas(self):
        self.seleccionar_columnas_manual(['Sex'], 'Fare')
        self.preprocesador.columnas_numericas = ['Fare']

        result = self.preprocesador.normalizar_escalar_datos()
        self.assertTrue(result)

    ########## Manejo de Valores Atípicos #############

    @patch('builtins.input', side_effect=["1"])  # Eliminar valores atípicos
    def test_eliminar_valores_atipicos(self, mock_input):
        self.preprocesador.columnas_numericas = ['Fare']
        self.seleccionar_columnas_manual(['Fare'], 'Target')

        filas_antes = self.preprocesador.dataset_modificado.shape[0]

        result = self.preprocesador.valores_atipicos()
        self.assertTrue(result)

        filas_despues = self.preprocesador.dataset_modificado.shape[0]
        self.assertLess(filas_despues, filas_antes)  # Se eliminó al menos una fila


    @patch('builtins.input', side_effect=["2"])  # Reemplazar valores atípicos
    def test_reemplazar_valores_atipicos(self, mock_input):
        self.preprocesador.columnas_numericas = ['Fare']
        self.seleccionar_columnas_manual(['Fare'], 'Target')

        result = self.preprocesador.valores_atipicos()
        self.assertTrue(result)

        # El valor extremo debe haber sido reemplazado
        self.assertNotIn(1000, self.preprocesador.dataset_modificado['Fare'].values)


    @patch('builtins.input', side_effect=["3"])  # Mantener valores atípicos
    def test_mantener_valores_atipicos(self, mock_input):
        self.preprocesador.columnas_numericas = ['Fare']
        self.seleccionar_columnas_manual(['Fare'], 'Target')

        result = self.preprocesador.valores_atipicos()
        self.assertTrue(result)

        # El valor extremo sigue presente
        self.assertIn(1000, self.preprocesador.dataset_modificado['Fare'].values)


    @patch('builtins.input', side_effect=["4"])  # Cancelar
    def test_cancelar_manejo_atipicos(self, mock_input):
        self.preprocesador.columnas_numericas = ['Fare']
        self.seleccionar_columnas_manual(['Fare'], 'Target')

        result = self.preprocesador.valores_atipicos()
        self.assertFalse(result)


    def test_sin_valores_atipicos(self):
        self.preprocesador.columnas_numericas = ['Pclass']
        self.seleccionar_columnas_manual(['Pclass'], 'Target')

        result = self.preprocesador.valores_atipicos()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
