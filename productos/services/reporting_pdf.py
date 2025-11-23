from io import BytesIO
from reportlab.pdfgen import canvas
from .reporting_base import ReportGenerator

class PDFReportGenerator(ReportGenerator):

    def generate(self, rows):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 800, "Reporte de Productos")
        
        y = 760
        for r in rows:
            pdf.drawString(100, y, f"{r['name']} - ${r['price']}")
            y -= 20

        pdf.save()
        buffer.seek(0)
        return buffer.read()

    def filename(self):
        return "reporte_productos.pdf"
