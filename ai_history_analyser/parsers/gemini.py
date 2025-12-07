"""Parser for Google Gemini export format"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .base import BaseParser
from ..models import Conversation, Message, Platform


class GeminiParser(BaseParser):
    """Parser for Gemini conversation exports"""
    
    @property
    def platform(self) -> Platform:
        return Platform.GEMINI
    
    def parse(self, file_path: Path) -> List[Conversation]:
        """Parse Gemini export file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        
        # Gemini exports can be in different formats
        if isinstance(data, list):
            for item in data:
                conv = self._parse_conversation(item)
                if conv:
                    conversations.append(conv)
        elif isinstance(data, dict):
            if 'conversations' in data:
                for item in data['conversations']:
                    conv = self._parse_conversation(item)
                    if conv:
                        conversations.append(conv)
            elif 'items' in data:
                for item in data['items']:
                    conv = self._parse_conversation(item)
                    if conv:
                        conversations.append(conv)
            else:
                # Single conversation
                conv = self._parse_conversation(data)
                if conv:
                    conversations.append(conv)
        
        return conversations
    
    def _parse_conversation(self, data: Dict[str, Any]) -> Conversation:
        """Parse a single conversation from Gemini format"""
        conv_id = data.get('conversation_id') or data.get('id') or data.get('uuid', 'unknown')
        title = data.get('title') or data.get('name') or None
        
        messages = []
        message_data = data.get('messages') or data.get('items') or data.get('history', [])
        
        for msg_data in message_data:
            msg = self._parse_message(msg_data)
            if msg:
                messages.append(msg)
        
        created_at = self._parse_timestamp(data.get('created_at') or data.get('created'))
        updated_at = self._parse_timestamp(data.get('updated_at') or data.get('updated'))
        
        return Conversation(
            id=conv_id,
            title=title,
            platform=Platform.GEMINI,
            messages=messages,
            created_at=created_at,
            updated_at=updated_at,
            metadata=data
        )
    
    def _parse_message(self, data: Dict[str, Any]) -> Message:
        """Parse a single message"""
        role = data.get('role') or data.get('author', {}).get('role', 'unknown')
        
        # Normalize role
        if role in ['user', 'human']:
            role = 'user'
        elif role in ['model', 'assistant', 'gemini']:
            role = 'assistant'
        else:
            role = 'system'
        
        # Extract content
        content = data.get('parts', [{}])[0].get('text', '') if isinstance(data.get('parts'), list) else ''
        if not content:
            content = data.get('text') or data.get('content', '')
        if isinstance(content, dict):
            content = content.get('text', '') or content.get('content', '')
        
        if not content:
            return None
        
        timestamp = self._parse_timestamp(
            data.get('created_at') or 
            data.get('timestamp') or 
            data.get('created')
        )
        
        return Message(
            role=role,
            content=str(content),
            timestamp=timestamp,
            metadata=data
        )
    
    def _parse_timestamp(self, value: Any) -> datetime:
        """Parse timestamp from various formats"""
        if not value:
            return None
        
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                return None
        
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                try:
                    from dateutil.parser import parse as date_parse
                    return date_parse(value)
                except Exception:
                    return None
        
        return None

