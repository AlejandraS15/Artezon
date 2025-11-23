import io
from openpyxl import Workbook
from .reporting_base import ReportGenerator

class ExcelReportGenerator(ReportGenerator):

    def generate(self, rows):
        wb = Workbook()
        ws = wb.active
        ws.append(["Nombre", "Precio"])

        for r in rows:
            ws.append([r["name"], r["price"]])

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer.read()

    def filename(self):
        return "reporte_productos.xlsx"
