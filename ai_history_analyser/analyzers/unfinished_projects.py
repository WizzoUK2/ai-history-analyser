"""Analyzer for detecting unfinished projects"""

import re
from typing import List, Dict, Any
from datetime import datetime
import hashlib

from .base import BaseAnalyzer
from ..models import Conversation, UnfinishedProject, AnalysisResult, Platform


class UnfinishedProjectsAnalyzer(BaseAnalyzer):
    """Detects unfinished projects in conversations"""
    
    # Default keywords that indicate unfinished work
    DEFAULT_KEYWORDS = [
        r'\bTODO\b',
        r'\bFIXME\b',
        r'\bXXX\b',
        r'\bHACK\b',
        r'\bneed to\b',
        r'\bneeds to\b',
        r'\bshould\s+(?:implement|add|create|build|fix|complete|finish)',
        r'\bnext steps?\b',
        r'\bto do\b',
        r'\bnot\s+(?:yet|done|complete|finished)',
        r'\bstill\s+(?:need|have|working)',
        r'\bwill\s+(?:implement|add|create|build|fix|complete)',
        r'\bplanning to\b',
        r'\bgoing to\b',
        r'\bintend to\b',
        r'\bunfinished\b',
        r'\bincomplete\b',
        r'\bwork in progress\b',
        r'\bWIP\b',
        r'\bpartially\s+(?:done|complete|implemented)',
        r'\bmissing\b',
        r'\bnot implemented\b',
        r'\bnot done\b',
    ]
    
    def __init__(self, keywords: List[str] = None, min_confidence: float = 0.5):
        """
        Initialize the analyzer
        
        Args:
            keywords: Custom keywords to search for (regex patterns)
            min_confidence: Minimum confidence threshold (0.0-1.0)
        """
        self.keywords = keywords or self.DEFAULT_KEYWORDS
        self.min_confidence = min_confidence
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.keywords]
    
    def get_name(self) -> str:
        return "unfinished_projects"
    
    def analyze(self, conversations: List[Conversation], config: Dict[str, Any] = None) -> AnalysisResult:
        """Analyze conversations for unfinished projects"""
        config = config or {}
        
        # Override settings from config
        if 'keywords' in config:
            self.keywords = config['keywords']
            self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.keywords]
        if 'min_confidence' in config:
            self.min_confidence = config['min_confidence']
        
        unfinished_projects = []
        platform = None
        
        for conv in conversations:
            if not platform:
                platform = conv.platform
            
            projects = self._analyze_conversation(conv)
            unfinished_projects.extend(projects)
        
        # Calculate priorities
        for project in unfinished_projects:
            project.priority_score = self._calculate_priority(project, conversations)
        
        # Sort by priority
        unfinished_projects.sort(key=lambda p: p.priority_score, reverse=True)
        
        return AnalysisResult(
            platform=platform or Platform.OTHER,
            conversations_analyzed=len(conversations),
            unfinished_projects=unfinished_projects
        )
    
    def _analyze_conversation(self, conversation: Conversation) -> List[UnfinishedProject]:
        """Analyze a single conversation for unfinished projects"""
        projects = []
        
        # Combine all messages for context
        full_text = '\n'.join([msg.content for msg in conversation.messages])
        
        # Find matches
        matches = []
        for pattern in self.compiled_patterns:
            for match in pattern.finditer(full_text):
                matches.append({
                    'keyword': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'context': self._extract_context(full_text, match.start(), match.end())
                })
        
        if not matches:
            return projects
        
        # Group matches by proximity (likely same project)
        grouped_matches = self._group_matches(matches)
        
        # Create projects from groups
        for i, group in enumerate(grouped_matches):
            confidence = self._calculate_confidence(group, full_text)
            
            if confidence >= self.min_confidence:
                project = self._create_project(
                    conversation=conversation,
                    matches=group,
                    confidence=confidence,
                    index=i
                )
                projects.append(project)
        
        return projects
    
    def _extract_context(self, text: str, start: int, end: int, context_size: int = 200) -> str:
        """Extract context around a match"""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:context_end].strip()
    
    def _group_matches(self, matches: List[Dict], max_distance: int = 500) -> List[List[Dict]]:
        """Group matches that are close together (likely same project)"""
        if not matches:
            return []
        
        # Sort by position
        sorted_matches = sorted(matches, key=lambda m: m['start'])
        
        groups = []
        current_group = [sorted_matches[0]]
        
        for match in sorted_matches[1:]:
            # If close to previous match, add to current group
            if match['start'] - current_group[-1]['end'] < max_distance:
                current_group.append(match)
            else:
                # Start new group
                groups.append(current_group)
                current_group = [match]
        
        groups.append(current_group)
        return groups
    
    def _calculate_confidence(self, matches: List[Dict], full_text: str) -> float:
        """Calculate confidence that this represents an unfinished project"""
        base_confidence = min(1.0, len(matches) * 0.2)  # More matches = higher confidence
        
        # Check for multiple keywords
        unique_keywords = len(set(m['keyword'].lower() for m in matches))
        base_confidence += unique_keywords * 0.1
        
        # Check for action words
        action_words = ['implement', 'create', 'build', 'fix', 'complete', 'add']
        context_text = ' '.join(m['context'].lower() for m in matches)
        action_count = sum(1 for word in action_words if word in context_text)
        base_confidence += min(0.3, action_count * 0.1)
        
        return min(1.0, base_confidence)
    
    def _calculate_priority(self, project: UnfinishedProject, all_conversations: List[Conversation]) -> float:
        """Calculate priority score for a project"""
        score = 0.0
        
        # Base score from confidence
        score += project.confidence * 0.4
        
        # Recency: more recent = higher priority
        if project.detected_at:
            days_ago = (datetime.now() - project.detected_at).days
            recency_score = max(0, 1.0 - (days_ago / 365.0))  # Decay over a year
            score += recency_score * 0.3
        
        # Number of keywords found
        score += min(0.2, len(project.keywords_found) * 0.05)
        
        # Context length (more context might indicate more important)
        context_length = len(project.context)
        if context_length > 500:
            score += 0.1
        
        return min(1.0, score)
    
    def _create_project(
        self,
        conversation: Conversation,
        matches: List[Dict],
        confidence: float,
        index: int
    ) -> UnfinishedProject:
        """Create an UnfinishedProject from matches"""
        # Generate ID
        project_id = hashlib.md5(
            f"{conversation.id}_{index}_{matches[0]['start']}".encode()
        ).hexdigest()[:12]
        
        # Extract title from context
        title = self._extract_title(matches, conversation)
        
        # Extract description
        description = self._extract_description(matches)
        
        # Get keywords found
        keywords_found = list(set(m['keyword'] for m in matches))
        
        # Combine context
        context = '\n\n'.join(m['context'] for m in matches[:3])  # Top 3 contexts
        
        # Get detection timestamp
        detected_at = conversation.updated_at or conversation.created_at or datetime.now()
        
        return UnfinishedProject(
            id=project_id,
            title=title,
            description=description,
            source_conversation_id=conversation.id,
            source_platform=conversation.platform,
            detected_at=detected_at,
            confidence=confidence,
            keywords_found=keywords_found,
            context=context,
            tags=self._extract_tags(matches, conversation)
        )
    
    def _extract_title(self, matches: List[Dict], conversation: Conversation) -> str:
        """Extract a title for the project"""
        # Try to find a title-like phrase in the context
        first_context = matches[0]['context']
        
        # Look for sentences that contain the keyword
        sentences = re.split(r'[.!?]\s+', first_context)
        for sentence in sentences:
            if any(m['keyword'].lower() in sentence.lower() for m in matches[:2]):
                # Clean up the sentence
                title = sentence.strip()[:100]
                if len(title) > 20:
                    return title
        
        # Fallback to conversation title or first keyword
        if conversation.title:
            return f"{conversation.title} - {matches[0]['keyword']}"
        
        return f"Unfinished Project: {matches[0]['keyword']}"
    
    def _extract_description(self, matches: List[Dict]) -> str:
        """Extract a description for the project"""
        # Combine contexts, removing duplicates
        contexts = []
        seen = set()
        
        for match in matches[:3]:  # Top 3 matches
            context = match['context']
            # Simple deduplication
            if context not in seen:
                contexts.append(context)
                seen.add(context)
        
        description = '\n\n'.join(contexts)
        
        # Limit length
        if len(description) > 500:
            description = description[:500] + "..."
        
        return description
    
    def _extract_tags(self, matches: List[Dict], conversation: Conversation) -> List[str]:
        """Extract relevant tags"""
        tags = []
        
        # Add platform tag
        if conversation.platform:
            tags.append(conversation.platform.value)
        
        # Extract tags from keywords
        keyword_text = ' '.join(m['keyword'].lower() for m in matches)
        
        if 'implement' in keyword_text or 'create' in keyword_text:
            tags.append('implementation')
        if 'fix' in keyword_text or 'bug' in keyword_text:
            tags.append('bugfix')
        if 'add' in keyword_text or 'feature' in keyword_text:
            tags.append('feature')
        
        return tags

