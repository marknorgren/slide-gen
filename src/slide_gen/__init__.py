"""Slide AI Backgrounds - Pluggable AI-powered slide background generator."""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .processors import SlideInfo, process_titles, process_file, generate_images
from .utils import create_provider

__all__ = ["SlideInfo", "process_titles", "process_file", "generate_images", "create_provider"]