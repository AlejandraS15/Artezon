from abc import ABC, abstractmethod
from typing import List, Dict

class ReportGenerator(ABC):
    """Interfaz para generar reportes."""

    @abstractmethod
    def generate(self, rows: List[Dict]) -> bytes:
        """Retorna el archivo en bytes."""
        pass

    @abstractmethod
    def filename(self) -> str:
        """Nombre del archivo final."""
        pass
