"""Simple image generation."""

import asyncio
from typing import List, Optional
from pathlib import Path
from dataclasses import dataclass

from ..providers.base import AIProvider, PromptRequest, ImageRequest
from ..utils.file_utils import save_image, sanitize_filename
from .slide_processor import SlideInfo


@dataclass
class GenerationResult:
    """Result of image generation."""
    slide: SlideInfo
    success: bool
    image_path: Optional[Path] = None
    error: Optional[str] = None
    prompt: Optional[str] = None
    theme: Optional[str] = None
    style: Optional[str] = None


async def generate_images(slides: List[SlideInfo], 
                         prompt_provider: AIProvider,
                         image_provider: AIProvider,
                         output_dir: Path = Path("generated")) -> List[GenerationResult]:
    """Generate images for slides."""
    
    async def generate_single(slide: SlideInfo) -> GenerationResult:
        try:
            # Generate prompt
            prompt_request = PromptRequest(
                slide_title=slide.title,
                slide_content=""
            )
            prompt_response = await prompt_provider.generate_prompt(prompt_request)
            
            if not prompt_response.success:
                return GenerationResult(slide, False, error=prompt_response.error)
            
            # Generate image
            image_request = ImageRequest(prompt=prompt_response.content)
            image_response = await image_provider.generate_image(image_request)
            
            if not image_response.success:
                return GenerationResult(slide, False, error=image_response.error, 
                                       prompt=prompt_response.content)
            
            # Save image
            filename = f"{sanitize_filename(slide.title)}.png"
            image_path = save_image(image_response.image_data, filename, output_dir)
            
            return GenerationResult(slide, True, image_path, prompt=prompt_response.content)
            
        except Exception as e:
            return GenerationResult(slide, False, error=str(e))
    
    # Generate all slides
    tasks = [generate_single(slide) for slide in slides]
    return await asyncio.gather(*tasks)