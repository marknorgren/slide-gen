"""Simple slide processor."""

from typing import List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SlideInfo:
    """Information about a slide."""
    title: str
    index: int = 0


def process_titles(titles: List[str]) -> List[SlideInfo]:
    """Process a list of slide titles."""
    return [SlideInfo(title=title.strip(), index=i) 
            for i, title in enumerate(titles) if title.strip()]


def process_file(file_path: Path) -> List[SlideInfo]:
    """Process a file and extract slide titles."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    content = file_path.read_text(encoding='utf-8')
    
    if file_path.suffix.lower() == '.md':
        # Extract markdown headers
        headers = extract_markdown_headers(content)
        return [SlideInfo(title=title.strip(), index=i) for i, title in enumerate(headers)]
    else:
        # Treat each line as a slide title
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return [SlideInfo(title=line, index=i) for i, line in enumerate(lines)]