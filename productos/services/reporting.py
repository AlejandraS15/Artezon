from abc import ABC, abstractmethod
import csv
import io
import json
from typing import Iterable, Mapping, Sequence
import datetime


class ReportGenerator(ABC):
    """Interfaz para generadores de reportes."""

    @abstractmethod
    def generate(self, rows: Iterable[Mapping]) -> bytes:
        """Genera el contenido del reporte y lo devuelve como bytes."""

    @abstractmethod
    def filename(self) -> str:
        """Nombre de archivo sugerido para la descarga."""


class CsvReportGenerator(ReportGenerator):
    def __init__(self, columns: Sequence[str] = ("name", "price", "description", "category", "material", "color", "stock", "created_at", "seller_username")):
        self.columns = list(columns)

    def generate(self, rows: Iterable[Mapping]) -> bytes:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.columns)
        writer.writeheader()
        for r in rows:
            # aseguramos que las claves existan y que los datetimes estén serializados
            row = {}
            for k in self.columns:
                v = r.get(k, "")
                if isinstance(v, datetime.datetime):
                    v = v.isoformat()
                row[k] = v
            writer.writerow(row)
        return buf.getvalue().encode("utf-8")

    def filename(self) -> str:
        return "productos_report.csv"


class JsonReportGenerator(ReportGenerator):
    def __init__(self, *, indent: int = 2):
        self.indent = indent

    def generate(self, rows: Iterable[Mapping]) -> bytes:
        # Convert rows to plain serializable types (e.g. datetimes -> ISO strings)
        data = []
        for r in rows:
            obj = {}
            for k, v in dict(r).items():
                if isinstance(v, datetime.datetime):
                    obj[k] = v.isoformat()
                else:
                    obj[k] = v
            data.append(obj)
        return json.dumps(data, ensure_ascii=False, indent=self.indent).encode("utf-8")

    def filename(self) -> str:
        return "productos_report.json"
