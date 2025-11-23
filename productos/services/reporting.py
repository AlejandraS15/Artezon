from abc import ABC, abstractmethod
import csv
import io
import json
from typing import Iterable, Mapping, Sequence


class ReportGenerator(ABC):
    """Interfaz para generadores de reportes."""

    @abstractmethod
    def generate(self, rows: Iterable[Mapping]) -> bytes:
        """Genera el contenido del reporte y lo devuelve como bytes."""

    @abstractmethod
    def filename(self) -> str:
        """Nombre de archivo sugerido para la descarga."""


class CsvReportGenerator(ReportGenerator):
    def __init__(self, columns: Sequence[str] = ("name", "price")):
        self.columns = list(columns)

    def generate(self, rows: Iterable[Mapping]) -> bytes:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.columns)
        writer.writeheader()
        for r in rows:
            # aseguramos que las claves existan
            row = {k: r.get(k, "") for k in self.columns}
            writer.writerow(row)
        return buf.getvalue().encode("utf-8")

    def filename(self) -> str:
        return "productos_report.csv"


class JsonReportGenerator(ReportGenerator):
    def __init__(self, *, indent: int = 2):
        self.indent = indent

    def generate(self, rows: Iterable[Mapping]) -> bytes:
        # For determinism, convert to list first
        data = [dict(r) for r in rows]
        return json.dumps(data, ensure_ascii=False, indent=self.indent).encode("utf-8")

    def filename(self) -> str:
        return "productos_report.json"
