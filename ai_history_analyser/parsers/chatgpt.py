"""Parser for ChatGPT export format"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .base import BaseParser
from ..models import Conversation, Message, Platform


class ChatGPTParser(BaseParser):
    """Parser for ChatGPT conversation exports"""
    
    @property
    def platform(self) -> Platform:
        return Platform.CHATGPT
    
    def parse(self, file_path: Path) -> List[Conversation]:
        """Parse ChatGPT export file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        
        # ChatGPT exports can be in different formats
        # Format 1: Array of conversations
        if isinstance(data, list):
            for item in data:
                conv = self._parse_conversation(item)
                if conv:
                    conversations.append(conv)
        # Format 2: Object with conversations array
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
        """Parse a single conversation from ChatGPT format"""
        # Extract conversation ID
        conv_id = data.get('id') or data.get('conversation_id') or data.get('uuid', 'unknown')
        
        # Extract title
        title = data.get('title') or data.get('name') or None
        
        # Extract messages
        messages = []
        message_data = data.get('mapping') or data.get('messages') or data.get('items', [])
        
        if isinstance(message_data, dict):
            # Format with mapping: {message_id: message_data}
            sorted_messages = sorted(
                message_data.items(),
                key=lambda x: x[1].get('create_time', 0) or x[1].get('timestamp', 0)
            )
            for msg_id, msg_data in sorted_messages:
                msg = self._parse_message(msg_data)
                if msg:
                    messages.append(msg)
        elif isinstance(message_data, list):
            # Format with array of messages
            for msg_data in message_data:
                msg = self._parse_message(msg_data)
                if msg:
                    messages.append(msg)
        
        # Extract timestamps
        created_at = self._parse_timestamp(data.get('create_time') or data.get('created_at'))
        updated_at = self._parse_timestamp(data.get('update_time') or data.get('updated_at'))
        
        return Conversation(
            id=conv_id,
            title=title,
            platform=Platform.CHATGPT,
            messages=messages,
            created_at=created_at,
            updated_at=updated_at,
            metadata=data
        )
    
    def _parse_message(self, data: Dict[str, Any]) -> Message:
        """Parse a single message"""
        # Handle nested message structure
        if 'message' in data:
            data = data['message']
        
        role = data.get('author', {}).get('role') or data.get('role', 'unknown')
        if role == 'user':
            role = 'user'
        elif role in ['assistant', 'chatgpt', 'gpt']:
            role = 'assistant'
        else:
            role = 'system'
        
        # Extract content
        content_parts = data.get('content', {}).get('parts', [])
        if isinstance(content_parts, list) and content_parts:
            content = '\n'.join(str(part) for part in content_parts)
        else:
            content = data.get('content', '') or data.get('text', '')
        
        if not content:
            return None
        
        timestamp = self._parse_timestamp(
            data.get('create_time') or 
            data.get('timestamp') or 
            data.get('created_at')
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
            # Unix timestamp
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                return None
        
        if isinstance(value, str):
            # ISO format or other string formats
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                try:
                    from dateutil.parser import parse as date_parse
                    return date_parse(value)
                except Exception:
                    return None
        
        return None

