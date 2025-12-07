"""Base analyzer interface"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..models import Conversation, AnalysisResult


class BaseAnalyzer(ABC):
    """Base class for analysis engines"""
    
    @abstractmethod
    def analyze(self, conversations: List[Conversation], config: Dict[str, Any] = None) -> AnalysisResult:
        """
        Analyze conversations and return results
        
        Args:
            conversations: List of conversations to analyze
            config: Optional configuration dictionary
            
        Returns:
            AnalysisResult with findings
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this analyzer"""
        pass

