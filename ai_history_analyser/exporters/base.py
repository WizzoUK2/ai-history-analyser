"""Base exporter interface"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import AnalysisResult


class BaseExporter(ABC):
    """Base class for exporters"""
    
    @abstractmethod
    def export(self, result: AnalysisResult, output_path: Path, config: dict = None) -> Path:
        """
        Export analysis results
        
        Args:
            result: AnalysisResult to export
            output_path: Path to export to
            config: Optional configuration dictionary
            
        Returns:
            Path to the exported file(s)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this exporter"""
        pass

