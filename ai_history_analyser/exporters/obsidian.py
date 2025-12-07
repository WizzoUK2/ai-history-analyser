"""Obsidian markdown exporter"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from .base import BaseExporter
from ..models import AnalysisResult, UnfinishedProject


class ObsidianExporter(BaseExporter):
    """Export analysis results to Obsidian markdown format"""
    
    def get_name(self) -> str:
        return "obsidian"
    
    def export(self, result: AnalysisResult, output_path: Path, config: dict = None) -> Path:
        """Export to Obsidian format"""
        config = config or {}
        
        # Determine output directory
        if output_path.is_dir():
            vault_path = output_path
            folder = config.get('folder', 'AI Projects')
            output_dir = vault_path / folder
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create main index file
        index_path = self._create_index(result, output_dir, config)
        
        # Create individual project files
        for project in result.unfinished_projects:
            self._create_project_file(project, output_dir, config)
        
        return index_path
    
    def _create_index(self, result: AnalysisResult, output_dir: Path, config: dict) -> Path:
        """Create the main index file"""
        index_path = output_dir / "Unfinished Projects Index.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Unfinished Projects Index\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Platform:** {result.platform.value.title()}\n")
            f.write(f"**Conversations Analyzed:** {result.conversations_analyzed}\n")
            f.write(f"**Total Unfinished Projects:** {len(result.unfinished_projects)}\n\n")
            
            f.write("---\n\n")
            
            # Summary by priority
            high_priority = [p for p in result.unfinished_projects if p.priority_score >= 0.7]
            medium_priority = [p for p in result.unfinished_projects if 0.4 <= p.priority_score < 0.7]
            low_priority = [p for p in result.unfinished_projects if p.priority_score < 0.4]
            
            f.write("## Priority Summary\n\n")
            f.write(f"- **High Priority:** {len(high_priority)}\n")
            f.write(f"- **Medium Priority:** {len(medium_priority)}\n")
            f.write(f"- **Low Priority:** {len(low_priority)}\n\n")
            
            f.write("---\n\n")
            
            # List all projects
            f.write("## All Projects\n\n")
            
            for i, project in enumerate(result.unfinished_projects, 1):
                priority_emoji = "🔴" if project.priority_score >= 0.7 else "🟡" if project.priority_score >= 0.4 else "🟢"
                
                f.write(f"### {i}. {priority_emoji} [{project.title}]({self._get_project_filename(project)}.md)\n\n")
                f.write(f"**Priority Score:** {project.priority_score:.2f}  \n")
                f.write(f"**Confidence:** {project.confidence:.2f}  \n")
                f.write(f"**Platform:** {project.source_platform.value}  \n")
                f.write(f"**Detected:** {project.detected_at.strftime('%Y-%m-%d') if project.detected_at else 'Unknown'}  \n")
                
                if project.tags:
                    f.write(f"**Tags:** {', '.join(f'#{tag}' for tag in project.tags)}  \n")
                
                f.write(f"\n{project.description[:200]}...\n\n")
                f.write("---\n\n")
        
        return index_path
    
    def _create_project_file(self, project: UnfinishedProject, output_dir: Path, config: dict):
        """Create an individual project file"""
        filename = self._get_project_filename(project)
        file_path = output_dir / f"{filename}.md"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {project.title}\n\n")
            
            # Metadata
            f.write("## Metadata\n\n")
            f.write(f"- **ID:** `{project.id}`\n")
            f.write(f"- **Priority Score:** {project.priority_score:.2f}\n")
            f.write(f"- **Confidence:** {project.confidence:.2f}\n")
            f.write(f"- **Platform:** {project.source_platform.value}\n")
            f.write(f"- **Source Conversation:** `{project.source_conversation_id}`\n")
            f.write(f"- **Detected:** {project.detected_at.strftime('%Y-%m-%d %H:%M:%S') if project.detected_at else 'Unknown'}\n")
            
            if project.tags:
                f.write(f"- **Tags:** {', '.join(f'#{tag}' for tag in project.tags)}\n")
            
            f.write("\n---\n\n")
            
            # Description
            f.write("## Description\n\n")
            f.write(f"{project.description}\n\n")
            
            # Keywords found
            if project.keywords_found:
                f.write("## Keywords Detected\n\n")
                for keyword in project.keywords_found:
                    f.write(f"- `{keyword}`\n")
                f.write("\n")
            
            # Context
            if project.context:
                f.write("## Context\n\n")
                f.write("```\n")
                f.write(project.context)
                f.write("\n```\n\n")
            
            # Links
            f.write("## Links\n\n")
            f.write(f"- [Back to Index](Unfinished Projects Index.md)\n")
            
            # Add frontmatter for Obsidian
            f.write("\n---\n\n")
            f.write("```yaml\n")
            f.write("tags:\n")
            for tag in project.tags:
                f.write(f"  - {tag}\n")
            f.write(f"platform: {project.source_platform.value}\n")
            f.write(f"priority: {project.priority_score:.2f}\n")
            f.write(f"confidence: {project.confidence:.2f}\n")
            f.write("```\n")
    
    def _get_project_filename(self, project: UnfinishedProject) -> str:
        """Generate a safe filename for the project"""
        # Clean title for filename
        import re
        filename = re.sub(r'[^\w\s-]', '', project.title)
        filename = re.sub(r'[-\s]+', '-', filename)
        filename = filename[:50]  # Limit length
        return filename or f"project-{project.id}"

