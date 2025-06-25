"""Simple file utilities."""

import re
from pathlib import Path
from PIL import Image
from io import BytesIO


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitize text for use as a filename."""
    safe_text = re.sub(r'[^\w\s-]', '', text)
    safe_text = re.sub(r'[-\s]+', '_', safe_text)
    safe_text = safe_text.strip('_')[:max_length]
    return safe_text if safe_text else "unnamed"


def save_image(image_data: bytes, filename: str, output_dir: Path) -> Path:
    """Save image data to a file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename
    
    # Convert to PNG
    image = Image.open(BytesIO(image_data))
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    
    image.save(file_path, 'PNG')
    return file_path