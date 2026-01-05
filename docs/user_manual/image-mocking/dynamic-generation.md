# Dynamic Generation - Create Custom Images

Learn how to generate images on-the-fly with custom dimensions, formats, and text overlays.

---

## Endpoint

```
GET /api/images/{width}x{height}
```

Returns a binary image file (PNG, JPEG, or WebP).

---

## Simple Generation

### Generate a Basic Image

```bash
curl http://localhost:18000/api/images/300x200 > image.png
```

**What happens:**
1. Mimicus sees request for 300×200 image
2. Checks if already generated (cache)
3. If not cached, generates random checkerboard pattern
4. Returns PNG binary data

**Result:** 300×200 PNG image with random colors

---

## Query Parameters

### format - Choose Image Format

```bash
GET /api/images/300x200?format=png    # PNG (default)
GET /api/images/300x200?format=jpeg   # JPEG
GET /api/images/300x200?format=webp   # WebP
```

**Example:**

```bash
curl http://localhost:18000/api/images/300x200?format=webp -o image.webp
```

Returns WebP format instead of PNG.

### text - Add Text Overlay

```bash
GET /api/images/300x200?text=Hello
```

Adds "Hello" text to the image center.

**Example:**

```html
<img src="/api/images/300x200?text=Product+Image" alt="Product">
```

Image displays with "Product Image" text overlay.

### identifier - Unique Identifier

```bash
GET /api/images/300x200?identifier=card-1
GET /api/images/300x200?identifier=card-2
```

Same dimensions but different identifier = **different image**!

**Why?** Testing grids of images—you need them to look different so you can tell them apart.

**Example:**

```html
<div class="product-grid">
  <img src="/api/images/200x200?identifier=product-1" alt="Product 1">
  <img src="/api/images/200x200?identifier=product-2" alt="Product 2">
  <img src="/api/images/200x200?identifier=product-3" alt="Product 3">
</div>
```

Each product image looks different, making layout testing easier.

---

## Combining Parameters

### All Parameters Together

```bash
GET /api/images/400x300?format=jpeg&text=Featured&identifier=hero-1
```

This:
- Creates 400×300 image
- Saves as JPEG format
- Includes "Featured" text overlay
- Uses identifier "hero-1" for uniqueness

---

## Complete Examples

### Example 1: Product Image

```html
<div class="product-card">
  <img
    src="http://localhost:18000/api/images/300x300?text=Product&identifier=prod-1"
    alt="Product"
  />
  <h3>Laptop</h3>
  <p>$999.99</p>
</div>
```

---

### Example 2: Hero Banner

```html
<div class="hero" style="
  background-image: url('http://localhost:18000/api/images/1920x400?text=Welcome');
  background-size: cover;
">
  <h1>Welcome to Our Store</h1>
</div>
```

---

### Example 3: Multiple Sizes (Responsive)

```html
<picture>
  <!-- Mobile: 320×240 -->
  <source
    srcset="http://localhost:18000/api/images/320x240?identifier=hero"
    media="(max-width: 480px)"
  />

  <!-- Tablet: 768×400 -->
  <source
    srcset="http://localhost:18000/api/images/768x400?identifier=hero"
    media="(max-width: 1024px)"
  />

  <!-- Desktop: 1920×400 -->
  <img
    src="http://localhost:18000/api/images/1920x400?identifier=hero"
    alt="Hero"
  />
</picture>
```

---

### Example 4: Grid of Images

```jsx
export default function ProductGrid() {
  const products = [
    { id: 1, name: 'Laptop' },
    { id: 2, name: 'Mouse' },
    { id: 3, name: 'Keyboard' },
    { id: 4, name: 'Monitor' },
  ];

  return (
    <div className="grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <img
            src={`http://localhost:18000/api/images/200x200?identifier=prod-${product.id}&text=${product.name}`}
            alt={product.name}
          />
          <h3>{product.name}</h3>
        </div>
      ))}
    </div>
  );
}
```

**Result:** 4 different images, each labeled with product name.

---

## Caching Explained

### How Caching Works

```
Request 1: GET /api/images/300x200
├─ No cache → Generate new image
├─ Save to disk
└─ Return image

Request 2: GET /api/images/300x200
├─ Found in cache → Don't regenerate
└─ Return cached image (instant!)

Request 3: GET /api/images/300x200?identifier=different
├─ Different identifier → Generate new image
└─ Return new image
```

### Cache Benefits

- **Speed**: Cached images return <1ms
- **Consistency**: Same dimensions = same image (good for testing)
- **Flexibility**: Different identifiers = different images

### Cache Storage

Images are stored in: `./storage/images/generated/`

Filename format: `generated-{width}x{height}-{identifier}.{format}`

---

## Image Properties

All generated images include:

- **Checkerboard Pattern**: Easy to see at different sizes
- **Dimension Text**: Shows actual dimensions
- **Random Colors**: Different each time (unless cached)
- **Unique ID**: Based on identifier parameter

---

## Best Practices

### ✅ Do

- Use identifiers to distinguish images in grids
- Test multiple sizes to verify responsive design
- Cache frequently used dimensions
- Add text for clarity in screenshots

### ❌ Don't

- Use same image everywhere (hard to debug layout)
- Forget identifier for grid layouts
- Generate huge images (8000×8000 is max)
- Expect different image each time without identifier change

---

## Dimension Guidelines

### Mobile Images
```bash
320×240   (small phone)
480×360   (regular phone)
640×480   (large phone)
```

### Tablet Images
```bash
768×576   (iPad portrait)
1024×768  (iPad landscape)
```

### Desktop Images
```bash
1280×720  (standard HD)
1920×1080 (Full HD)
2560×1440 (2K)
```

### Square Images (Cards, Avatars)
```bash
100×100   (avatar)
200×200   (card)
300×300   (featured)
```

---

## Testing Different Aspect Ratios

### Square (1:1)
```bash
GET /api/images/300x300
GET /api/images/500x500
```

### Landscape (16:9)
```bash
GET /api/images/320x180
GET /api/images/1920x1080
```

### Portrait (9:16)
```bash
GET /api/images/360x640
GET /api/images/540x960
```

### Wide (21:9)
```bash
GET /api/images/840x360
GET /api/images/1920x820
```

---

## Using in Different Contexts

### Background Images
```css
.hero {
  background-image: url('http://localhost:18000/api/images/1920x400');
  background-size: cover;
  height: 400px;
}
```

### CSS Media Queries
```css
@media (max-width: 480px) {
  .image {
    content: url('/api/images/320x240');
  }
}

@media (min-width: 1920px) {
  .image {
    content: url('/api/images/1920x1080');
  }
}
```

### srcset for Responsive Images
```html
<img
  srcset="
    /api/images/320x240?identifier=hero 320w,
    /api/images/768x400?identifier=hero 768w,
    /api/images/1920x400?identifier=hero 1920w
  "
  src="/api/images/1920x400?identifier=hero"
  alt="Hero"
/>
```

---

## Common Scenarios

### Scenario 1: "My hero image breaks on mobile"

Test it:
```html
<!-- Mobile -->
<img src="/api/images/320x180" alt="hero">
<!-- Tablet -->
<img src="/api/images/768x400" alt="hero">
<!-- Desktop -->
<img src="/api/images/1920x400" alt="hero">
```

### Scenario 2: "Product images look weird in grid"

Test with identifiers:
```html
<img src="/api/images/200x200?identifier=prod-1">
<img src="/api/images/200x200?identifier=prod-2">
<img src="/api/images/200x200?identifier=prod-3">
```

### Scenario 3: "Need to test image with label"

Add text:
```html
<img src="/api/images/300x200?text=Featured+Product">
```

---

## Performance Tips

- **Cache hit**: <1ms
- **Cache miss**: <50ms to generate
- **Reasonable sizes**: 300×300 to 1920×1080 ideal
- **Extreme sizes**: 8000×8000 takes longer

For performance testing, use cached images (same dimensions, same identifier).

---

## API Response

When you request an image, you get:

```
HTTP/1.1 200 OK
Content-Type: image/png
Cache-Control: public, max-age=86400
Content-Length: 2048

[binary image data]
```

---

## Next Steps

- 📱 **[Responsive Images](responsive-images.md)** - Use device presets
- 📷 **[User Images](user-images.md)** - Upload your own
- 🎯 **[Testing Layouts](testing-layouts.md)** - Verify your design

---

**Now you can generate any image you need on the fly!** 🎨
