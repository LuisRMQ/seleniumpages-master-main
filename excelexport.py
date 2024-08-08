import pandas as pd

class ExcelExporter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []
        self.columns = []

    def set_fields(self, fields):
        self.columns = list(fields.keys())

    def set_columns(self, columns):
        self.columns = columns

    def add_row(self, row):
        if len(row) != len(self.columns):
            raise ValueError("El número de elementos en la fila debe coincidir con el número de columnas")
        self.data.append(row)

    def export_to_excel(self):
        if not self.columns:
            raise ValueError("Las columnas no están definidas")
        if not self.data:
            raise ValueError("No hay datos para exportar")

        df = pd.DataFrame(self.data, columns=self.columns)
        df.to_excel(self.file_name, index=False)
        print(f"Datos exportados exitosamente a {self.file_name}")


