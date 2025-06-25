"""LM Studio provider implementation for local AI models."""

import os
from typing import Dict, Any, Optional
import aiohttp
import asyncio

from .base import AIProvider, PromptRequest, ImageRequest, AIResponse


class LMStudioProvider(AIProvider):
    """LM Studio provider for local AI models via OpenAI-compatible API."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:1234/v1")
        self.model = config.get("model", "local-model")  # LM Studio uses "local-model" by default
        self.timeout = config.get("timeout", 60)
        
    def supports_image_generation(self) -> bool:
        # LM Studio doesn't natively support image generation
        return False
        
    def supports_prompt_generation(self) -> bool:
        return True
    
    async def generate_prompt(self, request: PromptRequest) -> AIResponse:
        """Generate a creative visual prompt using LM Studio."""
        url = f"{self.base_url}/chat/completions"
        
        system_prompt = """You are a creative prompt engineer specializing in visual metaphors for presentations. 
        Create compelling, artistic landscape photography prompts that metaphorically represent concepts.
        Focus on real-world photography, not illustrations or paintings.
        Always specify 16:9 aspect ratio in your prompts."""
        
        user_prompt = f"""Create a single, visually striking landscape photography prompt that metaphorically represents: "{request.slide_title}"
        
        Additional context: {request.slide_content or "No additional context"}
        Style preferences: {request.style or "Professional, metaphorical, landscape photography"}
        
        Return only the prompt, no other text. Make it detailed and specific for a photographer."""
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        return AIResponse(success=True, content=content.strip())
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except aiohttp.ClientConnectorError:
            return AIResponse(success=False, error="Could not connect to LM Studio. Is it running?")
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Request timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating prompt: {str(e)}")
    
    async def generate_image(self, request: ImageRequest) -> AIResponse:
        """LM Studio doesn't support image generation natively."""
        return AIResponse(
            success=False, 
            error="LM Studio provider doesn't support image generation. Use a different provider for images."
        )
        
    async def health_check(self) -> bool:
        """Check if LM Studio is running and responding."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                # Check if LM Studio is responding
                async with session.get(f"{self.base_url}/models") as response:
                    return response.status == 200
        except Exception:
            return False