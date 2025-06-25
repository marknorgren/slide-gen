"""OpenAI provider implementation."""

import os
import base64
from typing import Dict, Any, Optional
import aiohttp
import asyncio

from .base import AIProvider, PromptRequest, ImageRequest, AIResponse


class OpenAIProvider(AIProvider):
    """OpenAI provider for prompt and image generation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.prompt_model = config.get("prompt_model", "gpt-4")
        self.image_model = config.get("image_model", "dall-e-3")
        self.timeout = config.get("timeout", 60)
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def supports_image_generation(self) -> bool:
        return True
        
    def supports_prompt_generation(self) -> bool:
        return True
    
    async def generate_prompt(self, request: PromptRequest) -> AIResponse:
        """Generate a creative visual prompt using OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are a creative prompt engineer specializing in visual metaphors for presentations. 
        Create compelling, artistic landscape photography prompts that metaphorically represent concepts.
        Focus on real-world photography, not illustrations or paintings.
        Always specify 16:9 aspect ratio in your prompts."""
        
        user_prompt = f"""Create a single, visually striking landscape photography prompt that metaphorically represents: "{request.slide_title}"
        
        Additional context: {request.slide_content or "No additional context"}
        Style preferences: {request.style or "Professional, metaphorical, landscape photography"}
        
        Return only the prompt, no other text. Make it detailed and specific for a photographer."""
        
        payload = {
            "model": self.prompt_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(f"{self.base_url}/chat/completions", 
                                      headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        return AIResponse(success=True, content=content.strip())
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Request timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating prompt: {str(e)}")
    
    async def generate_image(self, request: ImageRequest) -> AIResponse:
        """Generate an image using DALL-E."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Map aspect ratio to DALL-E size
        size_map = {
            "16:9": "1792x1024",
            "1:1": "1024x1024", 
            "9:16": "1024x1792"
        }
        size = request.size or size_map.get(request.aspect_ratio, "1792x1024")
        
        payload = {
            "model": self.image_model,
            "prompt": request.prompt,
            "n": 1,
            "size": size,
            "quality": request.quality,
            "response_format": "b64_json"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
                async with session.post(f"{self.base_url}/images/generations",
                                      headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        image_b64 = result["data"][0]["b64_json"]
                        image_data = base64.b64decode(image_b64)
                        return AIResponse(success=True, image_data=image_data)
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Image generation timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating image: {str(e)}")