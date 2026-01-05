# Image Mocking - Generate and Serve Images

Mimicus can generate placeholder images on the fly. Perfect for testing frontend layouts without waiting for real images!

---

## What is Image Mocking?

Image mocking means:
- Generate random placeholder images with custom dimensions
- Serve user-provided images with automatic dimension detection
- Create responsive image sets for different devices
- No external image APIs needed

```
Frontend requests: GET /api/images/300x200
Mimicus generates: Random checkerboard image 300×200px
Returns: PNG/JPEG/WebP binary data
```

---

## Why Mock Images?

### Problem: Before Image Mocking
```
Designer: "Here's your layout mockup"
Frontend Dev: "Need images for testing"
Backend: "We don't have images yet"
Frontend Dev: "Let me find placeholder images online..."
                (Time wasted searching, downloading, converting)
```

### Solution: With Image Mocking
```
Designer: "Here's your layout mockup"
Frontend Dev: "GET /api/images/300x200 returns image instantly"
               (Spend time on real frontend code, not image hunting)
```

---

## Key Features

### 🎨 Generate Placeholder Images
```bash
GET /api/images/300x200
# Returns random 300×200 image instantly
```

### 📱 Device Presets
```bash
GET /api/images/responsive/mobile
# Returns images for: 320×240, 480×360, 640×480
```

### 📷 Upload User Images
```bash
POST /api/images/upload
# Upload your own image, get back dimensions
```

### 🔢 Auto-Dimension Detection
```bash
Upload: product-photo.jpg (1920×1080)
Get back: Auto-detected dimensions + dimension-suffixed filename
```

### 🎯 Unique Identifiers
```bash
GET /api/images/300x200?identifier=product-1
# Different identifier = different image (helps testing)
```

---

## Quick Start

### Generate a Simple Image

```bash
curl http://localhost:18000/api/images/300x200 > image.png
```

Opens as a 300×200 PNG image in your browser or image viewer.

### Display in HTML

```html
<img src="http://localhost:18000/api/images/300x200" alt="Product">
```

Your browser displays the generated image instantly.

### Display in React

```jsx
export default function ProductCard() {
  return (
    <img
      src="http://localhost:18000/api/images/300x200"
      alt="Product"
    />
  );
}
```

---

## Image Formats

### Supported Formats

```bash
GET /api/images/300x200?format=png    # PNG (default)
GET /api/images/300x200?format=jpeg   # JPEG
GET /api/images/300x200?format=webp   # WebP (modern)
```

### Which Format to Use?

- **PNG**: Lossless, supports transparency, larger file size
- **JPEG**: Lossy, no transparency, smaller file size
- **WebP**: Modern, small file size, best for web

---

## Image Formats Returned

All generated images are **checkerboard pattern** with:
- Random colors
- Dimension text overlay
- Unique identifier (if provided)
- Instant generation

---

## Caching Behavior

### Same Dimensions = Same Image
```bash
GET /api/images/300x200   # Generated, cached
GET /api/images/300x200   # Returns same image (no regeneration)
```

### Different Dimensions = Different Image
```bash
GET /api/images/300x200    # Image A
GET /api/images/400x300    # Image B (different dimensions)
```

### With Identifier = Always Different
```bash
GET /api/images/300x200?identifier=card-1    # Image A
GET /api/images/300x200?identifier=card-2    # Image B (different identifier)
```

---

## Common Use Cases

### Use Case 1: Product Placeholders
```html
<div class="product-card">
  <img src="/api/images/300x300" alt="Product">
  <h3>Product Name</h3>
  <p>$99.99</p>
</div>
```

### Use Case 2: Hero Image
```html
<header style="background-image: url('/api/images/1920x400')">
  Hero Section
</header>
```

### Use Case 3: Responsive Images
```html
<picture>
  <source srcset="/api/images/320x240" media="(max-width: 480px)">
  <source srcset="/api/images/768x576" media="(max-width: 1024px)">
  <img src="/api/images/1920x1080" alt="Hero">
</picture>
```

### Use Case 4: Testing Different Sizes
```jsx
const sizes = [300, 400, 500, 600];
return sizes.map(size => (
  <img key={size} src={`/api/images/${size}x${size}`} alt="test" />
));
```

---

## Endpoints Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/{width}x{height}` | Generate/serve image |
| POST | `/generate` | Generate & return metadata |
| GET | `/responsive/{preset}` | Get image set URLs |
| POST | `/upload` | Upload user image |
| GET | `/list` | List all images |
| DELETE | `/{image_id}` | Delete image |

---

## What You'll Learn

In this section:

- 📖 **[Dynamic Generation](dynamic-generation.md)** - Generate images on-the-fly
- 📱 **[Responsive Images](responsive-images.md)** - Device-specific presets
- 📷 **[User Images](user-images.md)** - Upload and serve your own
- 🎯 **[Testing Layouts](testing-layouts.md)** - Verify UI at different sizes

---

## Configuration

### Image Settings

In your `.env` file:

```env
# Where to store generated/uploaded images
IMAGE_STORAGE_PATH=./storage/images

# Maximum dimension allowed
IMAGE_MAX_DIMENSION=8000

# Maximum upload size (MB)
IMAGE_MAX_UPLOAD_MB=10

# Default format (png, jpeg, webp)
IMAGE_DEFAULT_FORMAT=png

# Enable caching
IMAGE_CACHE_ENABLED=true
```

---

## Benefits

✅ **Fast Development** - No time finding images
✅ **Consistent Testing** - Same image every time
✅ **Unique IDs** - Test multiple images in grid
✅ **Responsive Testing** - Device presets ready
✅ **No Dependencies** - Built-in, no external APIs
✅ **Instant** - <5ms image generation

---

## Common Questions

### Q: Can I customize the colors?

A: Currently uses random colors. You can upload your own images instead.

### Q: What if I upload the same image twice?

A: Creates separate entries with dimension-suffixed names.

### Q: Can I delete images?

A: Yes! Use the DELETE endpoint with image_id.

### Q: How many images can I generate?

A: Unlimited (limited only by disk space).

### Q: Can I use these in production?

A: Mimicus is for development. Switch to real images for production.

---

## Next Steps

Ready to dive deeper?

- 📖 **[Dynamic Generation](dynamic-generation.md)** - Create custom images with parameters
- 📱 **[Responsive Images](responsive-images.md)** - Test across device sizes
- 📷 **[User Images](user-images.md)** - Upload and test your own images
- 🎯 **[Testing Layouts](testing-layouts.md)** - Verify your UI works everywhere

---

**Image mocking is one of Mimicus's superpowers. Let's learn how to use it!** 🎨
