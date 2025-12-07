"""Base parser interface"""

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from ..models import Conversation, Platform


class BaseParser(ABC):
    """Base class for platform-specific parsers"""
    
    @property
    @abstractmethod
    def platform(self) -> Platform:
        """The platform this parser handles"""
        pass
    
    @abstractmethod
    def parse(self, file_path: Path) -> List[Conversation]:
        """
        Parse a chat history export file
        
        Args:
            file_path: Path to the export file
            
        Returns:
            List of Conversation objects
        """
        pass
    
    def validate(self, file_path: Path) -> bool:
        """
        Validate that a file can be parsed by this parser
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if the file appears to be in the correct format
        """
        try:
            return file_path.exists() and file_path.is_file()
        except Exception:
            return False

