from io import BytesIO
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from .reporting import ReportGenerator


class PDFReportGenerator(ReportGenerator):
    """Generador PDF con detalle de producto.

    Es simple (canvas) y hace saltos de página cuando hace falta.
    """

    def __init__(self, page_size=A4, margin=50, line_height=14):
        self.page_size = page_size
        self.margin = margin
        self.line_height = line_height

    def _write_line(self, pdf, x, y, text, max_width):
        # split text if it's too long for the width
        lines = simpleSplit(str(text), pdf._fontname, pdf._fontsize, max_width)
        for i, ln in enumerate(lines):
            pdf.drawString(x, y - i * self.line_height, ln)
        return len(lines)

    def generate(self, rows):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=self.page_size)
        width, height = self.page_size
        pdf.setFont("Helvetica", 12)

        title = "Reporte de Productos"
        pdf.drawString(self.margin, height - self.margin, title)

        y = height - self.margin - 30
        max_width = width - 2 * self.margin

        for r in rows:
            if y < self.margin + 100:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = height - self.margin

            # Nombre y precio en una línea
            name = r.get("name", "")
            price = r.get("price", "")
            pdf.drawString(self.margin, y, f"Nombre: {name}    Precio: {price}")
            y -= self.line_height + 2

            # Descripción (wrap)
            desc = r.get("description", "")
            if desc:
                used = self._write_line(pdf, self.margin, y, f"Descripción: {desc}", max_width)
                y -= used * self.line_height

            # Otros campos en una línea
            category = r.get("category", "")
            material = r.get("material", "")
            color = r.get("color", "")
            stock = r.get("stock", "")
            seller = r.get("seller_username", "")
            created = r.get("created_at", "")
            # Asegurar formato ISO si es datetime
            if isinstance(created, datetime.datetime):
                created = created.isoformat()

            pdf.drawString(self.margin, y, f"Categoría: {category}    Material: {material}    Color: {color}")
            y -= self.line_height
            pdf.drawString(self.margin, y, f"Stock: {stock}    Vendedor: {seller}    Creado: {created}")
            y -= self.line_height + 8

        pdf.save()
        buffer.seek(0)
        return buffer.read()

    def filename(self) -> str:
        return "productos_report.pdf"
