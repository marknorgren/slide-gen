"""Abstract base class for AI providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import asyncio


@dataclass
class PromptRequest:
    """Request for generating a creative prompt."""
    slide_title: str
    slide_content: Optional[str] = None
    theme: str = "professional, modern"
    style: str = "landscape photography, natural lighting"
    aspect_ratio: str = "16:9"
    

@dataclass 
class ImageRequest:
    """Request for generating an image."""
    prompt: str
    style: Optional[str] = None
    aspect_ratio: str = "16:9"
    quality: str = "standard"
    size: Optional[str] = None


@dataclass
class AIResponse:
    """Response from AI provider."""
    success: bool
    content: Optional[str] = None
    image_data: Optional[bytes] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with configuration."""
        self.config = config
        self.name = self.__class__.__name__
        
    @abstractmethod
    async def generate_prompt(self, request: PromptRequest) -> AIResponse:
        """Generate a creative visual prompt for the slide content."""
        pass
        
    @abstractmethod 
    async def generate_image(self, request: ImageRequest) -> AIResponse:
        """Generate an image from the prompt."""
        pass
        
    @abstractmethod
    def supports_image_generation(self) -> bool:
        """Return True if this provider supports image generation."""
        pass
        
    @abstractmethod
    def supports_prompt_generation(self) -> bool:
        """Return True if this provider supports prompt generation."""
        pass
        
    def validate_config(self) -> bool:
        """Validate the provider configuration."""
        return True
        
    async def health_check(self) -> bool:
        """Check if the provider is available and healthy."""
        try:
            # Simple test request
            test_request = PromptRequest(slide_title="Test")
            response = await self.generate_prompt(test_request)
            return response.success
        except Exception:
            return False