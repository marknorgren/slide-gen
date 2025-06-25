"""Ollama provider implementation for local AI models."""

import os
from typing import Dict, Any, Optional
import aiohttp
import asyncio

from .base import AIProvider, PromptRequest, ImageRequest, AIResponse


class OllamaProvider(AIProvider):
    """Ollama provider for local AI models."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama3.2")
        self.timeout = config.get("timeout", 60)
        
    def supports_image_generation(self) -> bool:
        # Ollama doesn't natively support image generation
        return False
        
    def supports_prompt_generation(self) -> bool:
        return True
    
    async def generate_prompt(self, request: PromptRequest) -> AIResponse:
        """Generate a creative visual prompt using Ollama."""
        url = f"{self.base_url}/api/generate"
        
        system_prompt = """You are a creative prompt engineer specializing in visual metaphors for presentations. 
        Create compelling, artistic landscape photography prompts that metaphorically represent concepts.
        Focus on real-world photography, not illustrations or paintings.
        Always specify 16:9 aspect ratio in your prompts."""
        
        user_prompt = f"""Create a {request.style} photograph that metaphorically represents: "{request.slide_title}"
        
        Theme: {request.theme}
        Additional context: {request.slide_content or "No additional context"}
        
        Return only the detailed photography prompt with 16:9 aspect ratio. Focus on visual metaphors that represent the concept."""
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 150
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result.get("response", "").strip()
                        return AIResponse(success=True, content=content)
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except aiohttp.ClientConnectorError:
            return AIResponse(success=False, error="Could not connect to Ollama. Is it running?")
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Request timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating prompt: {str(e)}")
    
    async def generate_image(self, request: ImageRequest) -> AIResponse:
        """Ollama doesn't support image generation natively."""
        return AIResponse(
            success=False, 
            error="Ollama provider doesn't support image generation. Use a different provider for images."
        )
        
    async def health_check(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                # Check if Ollama is running
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        models = await response.json()
                        # Check if our model is available
                        model_names = [model.get("name", "") for model in models.get("models", [])]
                        return any(self.model in name for name in model_names)
                    return False
        except Exception:
            return False