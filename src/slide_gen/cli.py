"""Simple command line interface."""

import asyncio
import argparse
from pathlib import Path

from .utils.config_loader import create_provider
from .processors import process_titles, process_file, generate_images
from .processors.directory_generator import process_directory


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate AI-powered background images for slides"
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("--file", "-f", help="Path to slide file")
    input_group.add_argument("--titles", "-t", nargs="+", help="List of slide titles")
    input_group.add_argument("--directory", "-d", help="Directory with slides.md and config.yaml")
    
    # Provider options
    parser.add_argument("--prompt-provider", default="ollama", 
                       choices=["openai", "gemini", "ollama", "lmstudio"],
                       help="AI provider for prompts (default: ollama)")
    parser.add_argument("--image-provider", default="openai",
                       choices=["openai", "gemini"],
                       help="AI provider for images (default: openai)")
    
    # Output
    parser.add_argument("--output", "-o", default="generated", help="Output directory")
    
    # Utility options
    parser.add_argument("--health-check", action="store_true", 
                       help="Check provider health")
    
    args = parser.parse_args()
    
    # Handle health check
    if args.health_check:
        try:
            prompt_provider = create_provider(args.prompt_provider)
            image_provider = create_provider(args.image_provider)
            
            print(f"✓ {args.prompt_provider} provider: OK")
            print(f"✓ {args.image_provider} provider: OK")
        except Exception as e:
            print(f"✗ Provider error: {e}")
            return 1
        return 0
    
    # Process input
    if args.directory:
        # Directory-based workflow
        directory = Path(args.directory)
        if not directory.exists():
            print(f"Error: Directory not found: {directory}")
            return 1
        
        try:
            results = await process_directory(directory)
        except Exception as e:
            print(f"Error processing directory: {e}")
            return 1
            
    elif args.titles:
        slides = process_titles(args.titles)
        if not slides:
            print("Error: No slides found")
            return 1
        
        print(f"Processing {len(slides)} slides...")
        
        # Create providers
        try:
            prompt_provider = create_provider(args.prompt_provider)
            image_provider = create_provider(args.image_provider)
        except Exception as e:
            print(f"Error creating providers: {e}")
            return 1
        
        # Generate images
        output_dir = Path(args.output)
        results = await generate_images(slides, prompt_provider, image_provider, output_dir)
        
    elif args.file:
        slides = process_file(Path(args.file))
        if not slides:
            print("Error: No slides found")
            return 1
        
        print(f"Processing {len(slides)} slides...")
        
        # Create providers
        try:
            prompt_provider = create_provider(args.prompt_provider)
            image_provider = create_provider(args.image_provider)
        except Exception as e:
            print(f"Error creating providers: {e}")
            return 1
        
        # Generate images
        output_dir = Path(args.output)
        results = await generate_images(slides, prompt_provider, image_provider, output_dir)
        
    else:
        print("Error: Please provide --titles, --file, or --directory")
        return 1
    
    # Print results
    success_count = sum(1 for r in results if r.success)
    print(f"\nCompleted: {success_count}/{len(results)} successful")
    
    for result in results:
        if result.success:
            print(f"✓ {result.slide.title}: {result.image_path}")
        else:
            print(f"✗ {result.slide.title}: {result.error}")
    
    return 0


def cli_main():
    """Entry point for the CLI script."""
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\nCancelled by user")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)