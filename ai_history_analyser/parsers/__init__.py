"""Parsers for different AI platform chat history formats"""

from .base import BaseParser
from .chatgpt import ChatGPTParser
from .claude import ClaudeParser
from .gemini import GeminiParser

__all__ = ["BaseParser", "ChatGPTParser", "ClaudeParser", "GeminiParser"]


def get_parser(platform: str) -> BaseParser:
    """Get the appropriate parser for a platform"""
    platform_lower = platform.lower()
    
    if platform_lower == "chatgpt":
        return ChatGPTParser()
    elif platform_lower == "claude":
        return ClaudeParser()
    elif platform_lower == "gemini":
        return GeminiParser()
    else:
        raise ValueError(f"Unsupported platform: {platform}")

