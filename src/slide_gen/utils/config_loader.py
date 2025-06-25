"""Simple configuration loading."""

import os
from dotenv import load_dotenv

from ..providers.openai_provider import OpenAIProvider
from ..providers.gemini_provider import GeminiProvider
from ..providers.ollama_provider import OllamaProvider
from ..providers.lmstudio_provider import LMStudioProvider


def create_provider(provider_name: str):
    """Create a provider instance with environment config."""
    load_dotenv()
    
    if provider_name == "openai":
        return OpenAIProvider({
            "api_key": os.getenv("OPENAI_API_KEY"),
            "prompt_model": os.getenv("OPENAI_PROMPT_MODEL", "gpt-4"),
            "image_model": os.getenv("OPENAI_IMAGE_MODEL", "dall-e-3"),
        })
    elif provider_name == "gemini":
        return GeminiProvider({
            "api_key": os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
            "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
            "image_model": os.getenv("GEMINI_IMAGE_MODEL", "imagen-3.0-generate-001"),
        })
    elif provider_name == "ollama":
        return OllamaProvider({
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "model": os.getenv("OLLAMA_MODEL", "llama3.1"),
        })
    elif provider_name == "lmstudio":
        return LMStudioProvider({
            "base_url": os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
            "model": os.getenv("LMSTUDIO_MODEL", "local-model"),
        })
    else:
        raise ValueError(f"Unknown provider: {provider_name}")