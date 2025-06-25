# Slide Gen

<p align="center">
  <img src="logo.png" alt="Slide Gen" width="300">
</p>

Generate beautiful AI-powered background images for your presentation slides.

## Quick Start

1. **Setup**

```bash
git clone https://github.com/[username]/slide-gen.git
cd slide-gen
just setup
```

2. **Add API Keys** Edit `.env` file:

```bash
OPENAI_API_KEY=your-openai-key
OLLAMA_BASE_URL=http://localhost:11434
```

3. **Generate Images**

```bash
# From a directory (recommended)
uv run slide-gen --directory my-talk/

# From slide titles
uv run slide-gen --titles "Modern Architecture" "Cloud Computing" "AI Ethics"

# From a markdown file
uv run slide-gen --file slides.md

# Health check
uv run slide-gen --health-check
```

## Providers

| Provider  | Prompts | Images | Setup       |
| --------- | ------- | ------ | ----------- |
| OpenAI    | ✅      | ✅     | Add API key |
| Gemini    | ✅      | ✅     | Add API key |
| Ollama    | ✅      | ❌     | Run locally |
| LM Studio | ✅      | ❌     | Run locally |

## Directory Workflow (Recommended)

Create a folder with `slides.md` and `config.yaml`:

**config.yaml:**

```yaml
theme: "modern tech, clean geometric shapes"
style: "architectural photography, clean lines"
prompt_provider: "ollama"
image_provider: "openai"
```

**slides.md:**

```markdown
# Introduction to AI

Overview of artificial intelligence concepts

# Machine Learning

Algorithms that learn from data

# Future Trends

Emerging technologies and possibilities
```

**Generate:**

```bash
uv run slide-gen --directory my-talk/

# Or try the included examples:
uv run slide-gen --directory examples/tech-presentation-openai/
uv run slide-gen --directory examples/business-strategy/
```

**Output:**

- `my-talk/Introduction_to_AI.png`
- `my-talk/Machine_Learning.png`
- `my-talk/Future_Trends.png`
- `my-talk/slides-images.md` (markdown with embedded images)
- `my-talk/generation-log.md` (detailed prompts and generation log)

## Other Examples

```bash
# Use different providers
uv run slide-gen --titles "My Slide" --prompt-provider ollama --image-provider openai

# Process markdown file
echo "# AI Overview\n# Machine Learning\n# Future Trends" > slides.md
uv run slide-gen --file slides.md

# Custom theme and style
uv run slide-gen --titles "Market Analysis" "Growth Strategy" \
  --theme "corporate excellence, innovation, leadership" \
  --style "corporate photography, professional" \
  --aspect-ratio "4:3"

# Academic presentation style
uv run slide-gen --file research.md \
  --theme "academic research, scholarly" \
  --style "documentary photography, natural lighting"
```

## Configuration

Set environment variables in `.env`:

```bash
# OpenAI
OPENAI_API_KEY=your-key

# Gemini
GEMINI_API_KEY=your-key

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# LM Studio (local)
LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

## CLI Options

```bash
uv run slide-gen [options]

# Input
--directory my-talk/             # Directory with slides.md and config.yaml
--titles "Title 1" "Title 2"     # Slide titles
--file slides.md                 # Markdown/text file

# Providers
--prompt-provider ollama         # AI for prompts
--image-provider openai          # AI for images

# Style and Theme
--theme "corporate, modern"      # Theme for generation
--style "clean photography"      # Style for generation  
--aspect-ratio 16:9              # Image aspect ratio (16:9, 4:3, 1:1)

# Output
--output generated               # Output directory

# Utilities
--health-check                   # Test providers
```

## Development

```bash
# Install
just install

# Test
just test

# Examples
just example               # Basic title-based generation
just example-directory     # Directory-based generation
```

## Included Examples

The repository includes example presentations you can try immediately:

- `examples/tech-presentation-openai/` - Technology theme with OpenAI
  ([view gallery](examples/tech-presentation-openai/slides-images.md))
- `examples/tech-presentation-gemini/` - Technology theme with Gemini
  ([view gallery](examples/tech-presentation-gemini/slides-images.md))
- `examples/business-strategy/` - Corporate and strategic planning theme
  ([view gallery](examples/business-strategy/slides-images.md))
- `examples/academic-research/` - Academic and research methodology theme
  ([view gallery](examples/academic-research/slides-images.md))

Try them with:

```bash
uv run slide-gen --directory examples/tech-presentation-openai/
uv run slide-gen --directory examples/tech-presentation-gemini/
```
