"""Analysis engines for chat history"""

from .base import BaseAnalyzer
from .unfinished_projects import UnfinishedProjectsAnalyzer

__all__ = ["BaseAnalyzer", "UnfinishedProjectsAnalyzer"]


def get_analyzer(analyzer_type: str) -> BaseAnalyzer:
    """Get the appropriate analyzer"""
    analyzer_lower = analyzer_type.lower()
    
    if analyzer_lower in ["unfinished", "unfinished-projects", "unfinished_projects"]:
        return UnfinishedProjectsAnalyzer()
    else:
        raise ValueError(f"Unsupported analyzer type: {analyzer_type}")

