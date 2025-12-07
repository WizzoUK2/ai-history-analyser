"""JSON exporter"""

import json
from pathlib import Path
from typing import Dict, Any

from .base import BaseExporter
from ..models import AnalysisResult


class JSONExporter(BaseExporter):
    """Export analysis results to JSON format"""
    
    def get_name(self) -> str:
        return "json"
    
    def export(self, result: AnalysisResult, output_path: Path, config: dict = None) -> Path:
        """Export to JSON format"""
        config = config or {}
        
        # Determine output file
        if output_path.is_dir():
            output_file = output_path / "analysis_results.json"
        else:
            output_file = output_path
        
        # Convert to dict
        data = {
            'platform': result.platform.value,
            'conversations_analyzed': result.conversations_analyzed,
            'analysis_date': result.analysis_date.isoformat(),
            'unfinished_projects': [
                {
                    'id': p.id,
                    'title': p.title,
                    'description': p.description,
                    'source_conversation_id': p.source_conversation_id,
                    'source_platform': p.source_platform.value,
                    'detected_at': p.detected_at.isoformat() if p.detected_at else None,
                    'confidence': p.confidence,
                    'priority_score': p.priority_score,
                    'keywords_found': p.keywords_found,
                    'tags': p.tags,
                    'context': p.context,
                    'metadata': p.metadata
                }
                for p in result.unfinished_projects
            ],
            'metadata': result.metadata
        }
        
        # Write JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_file

