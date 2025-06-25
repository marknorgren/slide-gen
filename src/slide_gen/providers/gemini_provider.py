"""Google Gemini provider implementation."""

import os
import base64
from typing import Dict, Any, Optional
import aiohttp
import asyncio

from .base import AIProvider, PromptRequest, ImageRequest, AIResponse


class GeminiProvider(AIProvider):
    """Google Gemini provider for prompt generation and image generation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.base_url = config.get("base_url", "https://generativelanguage.googleapis.com/v1beta")
        self.model = config.get("model", "gemini-2.0-flash-exp")
        self.image_model = config.get("image_model", "imagen-4.0-generate-preview-06-06")
        self.timeout = config.get("timeout", 60)
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
    
    def supports_image_generation(self) -> bool:
        return True
        
    def supports_prompt_generation(self) -> bool:
        return True
    
    async def generate_prompt(self, request: PromptRequest) -> AIResponse:
        """Generate a creative visual prompt using Gemini."""
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        system_instruction = """You are a creative prompt engineer specializing in visual metaphors for presentations. 
        Create compelling, artistic landscape photography prompts that metaphorically represent concepts.
        Focus on real-world photography, not illustrations or paintings.
        Always specify 16:9 aspect ratio in your prompts."""
        
        user_prompt = f"""Create a single, visually striking landscape photography prompt that metaphorically represents: "{request.slide_title}"
        
        Additional context: {request.slide_content or "No additional context"}
        Theme: {request.theme or "Professional, modern"}
        Style preferences: {request.style or "Professional, metaphorical, landscape photography"}
        
        Return only the prompt, no other text. Make it detailed and specific for a photographer."""
        
        payload = {
            "contents": [{
                "parts": [{"text": user_prompt}]
            }],
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 150
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        return AIResponse(success=True, content=content.strip())
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Request timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating prompt: {str(e)}")
    
    async def generate_image(self, request: ImageRequest) -> AIResponse:
        """Generate an image using Imagen."""
        url = f"{self.base_url}/models/{self.image_model}:predict?key={self.api_key}"
        
        # Enhance prompt with aspect ratio
        enhanced_prompt = f"{request.prompt}, 16:9 aspect ratio, high quality photography"
        
        payload = {
            "instances": [
                {
                    "prompt": enhanced_prompt
                }
            ],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9"
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        # Imagen returns image data in predictions format
                        if "predictions" in result and result["predictions"]:
                            prediction = result["predictions"][0]
                            if "bytesBase64Encoded" in prediction:
                                image_b64 = prediction["bytesBase64Encoded"]
                                image_data = base64.b64decode(image_b64)
                                return AIResponse(success=True, image_data=image_data)
                            else:
                                return AIResponse(success=False, error="No image data in prediction")
                        else:
                            return AIResponse(success=False, error="No predictions in response")
                    else:
                        error_text = await response.text()
                        return AIResponse(success=False, error=f"API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            return AIResponse(success=False, error="Image generation timed out")
        except Exception as e:
            return AIResponse(success=False, error=f"Error generating image: {str(e)}")