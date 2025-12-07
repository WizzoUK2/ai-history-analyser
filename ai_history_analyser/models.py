"""Data models for chat history and analysis results"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class Platform(Enum):
    """Supported AI platforms"""
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    OTHER = "other"


@dataclass
class Message:
    """A single message in a conversation"""
    role: str  # "user", "assistant", "system", etc.
    content: str
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    """A conversation thread"""
    id: str
    title: Optional[str] = None
    platform: Optional[Platform] = None
    messages: List[Message] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnfinishedProject:
    """An identified unfinished project"""
    id: str
    title: str
    description: str
    source_conversation_id: str
    source_platform: Platform
    detected_at: datetime
    confidence: float  # 0.0 to 1.0
    keywords_found: List[str] = field(default_factory=list)
    context: str = ""  # Relevant conversation context
    priority_score: float = 0.0  # Calculated priority
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """Results from analyzing chat history"""
    platform: Platform
    conversations_analyzed: int
    unfinished_projects: List[UnfinishedProject]
    analysis_date: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

