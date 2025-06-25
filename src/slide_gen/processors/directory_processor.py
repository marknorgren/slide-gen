"""Simple directory-based slide processing."""

import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass

from .slide_processor import SlideInfo, extract_markdown_headers


@dataclass
class DirectoryConfig:
    """Configuration from config.yaml."""
    theme: str = "professional, modern"
    style: str = "landscape photography, natural lighting"
    prompt_provider: str = "ollama"
    image_provider: str = "openai"


def load_config(directory: Path) -> DirectoryConfig:
    """Load config.yaml from directory."""
    config_file = directory / "config.yaml"
    if not config_file.exists():
        return DirectoryConfig()
    
    with open(config_file, 'r') as f:
        data = yaml.safe_load(f) or {}
    
    return DirectoryConfig(
        theme=data.get('theme', DirectoryConfig.theme),
        style=data.get('style', DirectoryConfig.style),
        prompt_provider=data.get('prompt_provider', DirectoryConfig.prompt_provider),
        image_provider=data.get('image_provider', DirectoryConfig.image_provider),
    )


def extract_slides_from_md(directory: Path) -> List[SlideInfo]:
    """Extract slides from slides.md file."""
    slides_file = directory / "slides.md"
    if not slides_file.exists():
        raise FileNotFoundError(f"slides.md not found in {directory}")
    
    content = slides_file.read_text(encoding='utf-8')
    
    # Extract headers (# Title)
    headers = extract_markdown_headers(content)
    
    return [SlideInfo(title=title.strip(), index=i) 
            for i, title in enumerate(headers)]


def create_slides_images_md(directory: Path, results: List) -> Path:
    """Create slides-images.md with embedded images."""
    output_file = directory / "slides-images.md"
    
    content = "# Slides with Generated Images\n\n"
    
    for result in results:
        if result.success:
            # Get relative image path
            image_name = result.image_path.name
            content += f"## {result.slide.title}\n\n"
            content += f"![{result.slide.title}]({image_name})\n\n"
        else:
            content += f"## {result.slide.title}\n\n"
            content += f"*Image generation failed: {result.error}*\n\n"
    
    output_file.write_text(content, encoding='utf-8')
    return output_file


def create_generation_log(directory: Path, results: List, config) -> Path:
    """Create generation-log.md with detailed prompt information."""
    output_file = directory / "generation-log.md"
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"# Generation Log\n\n"
    content += f"**Generated:** {timestamp}\n"
    content += f"**Theme:** {config.theme}\n"
    content += f"**Style:** {config.style}\n"
    content += f"**Prompt Provider:** {config.prompt_provider}\n"
    content += f"**Image Provider:** {config.image_provider}\n\n"
    
    success_count = sum(1 for r in results if r.success)
    content += f"**Results:** {success_count}/{len(results)} successful\n\n"
    content += "---\n\n"
    
    for i, result in enumerate(results, 1):
        content += f"## {i}. {result.slide.title}\n\n"
        
        if result.success:
            content += f"**Status:** ✅ Success\n"
            content += f"**Image:** {result.image_path.name}\n\n"
        else:
            content += f"**Status:** ❌ Failed\n"
            content += f"**Error:** {result.error}\n\n"
        
        if result.prompt:
            content += f"**Generated Prompt:**\n```\n{result.prompt}\n```\n\n"
        
        content += "---\n\n"
    
    output_file.write_text(content, encoding='utf-8')
    return output_file