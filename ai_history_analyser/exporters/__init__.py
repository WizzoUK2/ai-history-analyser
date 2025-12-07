"""Export modules for analysis results"""

from .base import BaseExporter
from .obsidian import ObsidianExporter
from .json import JSONExporter

__all__ = ["BaseExporter", "ObsidianExporter", "JSONExporter"]


def get_exporter(exporter_type: str) -> BaseExporter:
    """Get the appropriate exporter"""
    exporter_lower = exporter_type.lower()
    
    if exporter_lower == "obsidian":
        return ObsidianExporter()
    elif exporter_lower == "json":
        return JSONExporter()
    else:
        raise ValueError(f"Unsupported exporter type: {exporter_type}")

