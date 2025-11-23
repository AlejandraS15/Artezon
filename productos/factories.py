from django.conf import settings
from .services.reporting import CsvReportGenerator, JsonReportGenerator, ReportGenerator


def get_report_generator() -> ReportGenerator:
    """Devuelve una implementación de ReportGenerator según `settings.REPORT_IMPL`.

    Soporta por defecto 'csv' y 'json'. Para 'excel' y 'pdf' hace importaciones
    perezosas y lanza un error claro si falta la dependencia (por ejemplo `openpyxl`).
    """
    impl = getattr(settings, "REPORT_IMPL", "csv") or "csv"
    impl = impl.lower()

    if impl == "json":
        return JsonReportGenerator()

    if impl == "excel":
        # importación perezosa: solo si el usuario pidió excel
        try:
            from .services.reporting_excel import ExcelReportGenerator
        except Exception as e:  # ImportError u otros
            raise RuntimeError(
                "No se pudo cargar el generador Excel. Instala 'openpyxl' y vuelve a intentar. "
                f"Detalle: {e}"
            )
        return ExcelReportGenerator()

    if impl == "pdf":
        try:
            from .services.reporting_pdf import PDFReportGenerator
        except Exception as e:
            raise RuntimeError(
                "No se pudo cargar el generador PDF. Instala 'reportlab' y vuelve a intentar. "
                f"Detalle: {e}"
            )
        return PDFReportGenerator()

    # por defecto -> csv
    return CsvReportGenerator()
