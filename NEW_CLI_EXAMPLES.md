# New CLI Examples - Theme and Style Options

This document showcases the new CLI theme, style, and aspect-ratio options introduced in this PR.

## New Features Demonstrated

### 1. Direct CLI Theme and Style Control
- `--theme` option for custom presentation themes
- `--style` option for custom visual styles  
- `--aspect-ratio` option with validation (16:9, 4:3, 1:1)

### 2. No Configuration Files Required
These examples show how to generate themed slides without creating `config.yaml` files, perfect for quick one-off presentations.

## Example 1: Creative Presentation (Square Format)

**Command:**
```bash
slide-gen --titles "Design Trends 2025" "Innovation in Art" "Creative Process" "Future Vision" \
  --theme "creativity, modern art, innovation" \
  --style "artistic photography, vibrant colors, dynamic composition" \
  --aspect-ratio "1:1" \
  --output examples/creative-presentation
```

**Files:** `examples/creative-presentation/`
- **Aspect Ratio:** 1:1 (square) - Perfect for social media and modern presentations
- **Theme:** Artistic and creative focus
- **Style:** Vibrant colors with dynamic compositions

## Example 2: Corporate Excellence (Traditional Format)

**Command:**
```bash
slide-gen --titles "Strategic Leadership" "Market Expansion" "Operational Excellence" "Financial Growth" \
  --theme "corporate excellence, leadership, innovation" \
  --style "corporate photography, professional lighting, clean aesthetics" \
  --aspect-ratio "4:3" \
  --output examples/corporate-excellence
```

**Files:** `examples/corporate-excellence/`
- **Aspect Ratio:** 4:3 (traditional) - Perfect for boardroom presentations
- **Theme:** Corporate and professional focus  
- **Style:** Clean, professional aesthetics

## Benefits of New CLI Options

1. **Faster Workflow** - No need to create config files for simple customizations
2. **Better Discoverability** - Theme/style options visible in `--help` output
3. **Aspect Ratio Control** - Choose from 16:9, 4:3, or 1:1 formats
4. **Consistent Experience** - All input methods support theme/style configuration
5. **Backward Compatibility** - Directory workflow with config.yaml unchanged

## Validation

The CLI properly validates aspect ratio choices:
```bash
slide-gen --titles "Test" --aspect-ratio "invalid"
# Error: invalid choice: 'invalid' (choose from '16:9', '4:3', '1:1')
```

## Integration with Existing Workflows

The new options work with all input methods:
- `--titles` (demonstrated above)
- `--file slides.md` 
- `--directory` (uses config.yaml, CLI options override)

These examples showcase how the new CLI options provide immediate value while maintaining full backward compatibility.