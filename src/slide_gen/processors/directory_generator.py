"""Directory-based image generation workflow."""

import asyncio
from pathlib import Path
from typing import List

from ..providers.base import PromptRequest, ImageRequest
from ..utils.config_loader import create_provider
from ..utils.file_utils import save_image, sanitize_filename
from .slide_processor import SlideInfo
from .image_generator import GenerationResult
from .directory_processor import load_config, extract_slides_from_md, create_slides_images_md, create_generation_log


async def process_directory(directory_path: Path) -> List[GenerationResult]:
    """Process a directory with slides.md and config.yaml."""
    
    # Load configuration
    config = load_config(directory_path)
    print(f"Using theme: {config.theme}")
    print(f"Using style: {config.style}")
    
    # Extract slides
    slides = extract_slides_from_md(directory_path)
    print(f"Found {len(slides)} slides")
    
    # Create providers
    prompt_provider = create_provider(config.prompt_provider)
    image_provider = create_provider(config.image_provider)
    
    # Generate images
    results = await generate_images_with_config(
        slides, 
        prompt_provider, 
        image_provider, 
        directory_path,
        config
    )
    
    # Create slides-images.md
    images_file = create_slides_images_md(directory_path, results)
    print(f"Created: {images_file}")
    
    # Create generation log
    log_file = create_generation_log(directory_path, results, config)
    print(f"Created: {log_file}")
    
    return results


async def generate_images_with_config(slides: List[SlideInfo],
                                     prompt_provider,
                                     image_provider, 
                                     output_dir: Path,
                                     config) -> List[GenerationResult]:
    """Generate images with directory config."""
    
    async def generate_single(slide: SlideInfo) -> GenerationResult:
        try:
            # Generate prompt with theme/style
            prompt_request = PromptRequest(
                slide_title=slide.title,
                slide_content="",
                theme=config.theme,
                style=config.style
            )
            prompt_response = await prompt_provider.generate_prompt(prompt_request)
            
            if not prompt_response.success:
                return GenerationResult(slide, False, error=prompt_response.error)
            
            # Generate image
            image_request = ImageRequest(prompt=prompt_response.content)
            image_response = await image_provider.generate_image(image_request)
            
            if not image_response.success:
                return GenerationResult(slide, False, error=image_response.error,
                                       prompt=prompt_response.content,
                                       theme=config.theme, 
                                       style=config.style)
            
            # Save image in the directory
            filename = f"{sanitize_filename(slide.title)}.png"
            image_path = save_image(image_response.image_data, filename, output_dir)
            
            return GenerationResult(slide, True, image_path, 
                                   prompt=prompt_response.content,
                                   theme=config.theme, 
                                   style=config.style)
            
        except Exception as e:
            return GenerationResult(slide, False, error=str(e),
                                   theme=config.theme, 
                                   style=config.style)
    
    # Generate all slides
    tasks = [generate_single(slide) for slide in slides]
    return await asyncio.gather(*tasks)