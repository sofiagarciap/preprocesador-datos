class PreprocesadoDatos:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.features = []
        self.target = None

    def seleccionar_columnas(self, features_input, target_input):
        features_input = [int(x.strip()) for x in features_input.split(",")]
        columnas = list(self.data_loader.dataset.columns)

        self.features = [columnas[i - 1] for i in features_input]
        self.target = columnas[target_input - 1]

        if self.target in self.features:
            print("⚠ Error: La columna de salida no puede ser una feature.")
            self.features = []
            self.target = None
