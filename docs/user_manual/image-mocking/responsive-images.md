# Responsive Images - Device Presets

Mimicus includes built-in device presets so you can test your design across phone, tablet, and desktop without manually creating images.

---

## What are Device Presets?

Presets are **predefined image sets** for different devices:

```
Mobile:  320×240, 480×360, 640×480
Tablet:  768×576, 1024×768
Desktop: 1280×720, 1920×1080, 2560×1440
All:     All of the above combined
```

Instead of creating each image manually, request a preset and get all sizes at once!

---

## Endpoint

```
GET /api/images/responsive/{preset}
```

Returns a JSON response with URLs for all images in that preset.

---

## Available Presets

### Mobile Preset

```bash
GET /api/images/responsive/mobile
```

**Response:**

```json
{
  "preset": "mobile",
  "images": [
    {
      "width": 320,
      "height": 240,
      "url": "http://localhost:18000/api/images/320x240",
      "format": "webp"
    },
    {
      "width": 480,
      "height": 360,
      "url": "http://localhost:18000/api/images/480x360",
      "format": "webp"
    },
    {
      "width": 640,
      "height": 480,
      "url": "http://localhost:18000/api/images/640x480",
      "format": "webp"
    }
  ]
}
```

All mobile images are returned in WebP format (fast, modern).

### Tablet Preset

```bash
GET /api/images/responsive/tablet
```

Returns:
- 768×576 (iPad portrait)
- 1024×768 (iPad landscape)

### Desktop Preset

```bash
GET /api/images/responsive/desktop
```

Returns:
- 1280×720 (HD)
- 1920×1080 (Full HD)
- 2560×1440 (2K)

### All Preset

```bash
GET /api/images/responsive/all
```

Returns all images from mobile + tablet + desktop (9 images total).

---

## Using Presets in HTML

### Picture Element

```html
<picture>
  <!-- Mobile -->
  <source media="(max-width: 480px)"
    srcset="http://localhost:18000/api/images/320x240 1x,
            http://localhost:18000/api/images/480x360 2x">

  <!-- Tablet -->
  <source media="(max-width: 1024px)"
    srcset="http://localhost:18000/api/images/768x576">

  <!-- Desktop -->
  <img src="http://localhost:18000/api/images/1920x1080" alt="Hero">
</picture>
```

### Srcset Attribute

```html
<img
  srcset="
    http://localhost:18000/api/images/320x240 320w,
    http://localhost:18000/api/images/480x360 480w,
    http://localhost:18000/api/images/1920x1080 1920w
  "
  src="http://localhost:18000/api/images/1920x1080"
  alt="Product"
  sizes="
    (max-width: 480px) 100vw,
    (max-width: 1024px) 100vw,
    1920px
  "
/>
```

---

## Using Presets in React

### Fetch and Display

```jsx
import { useEffect, useState } from 'react';

export default function ResponsiveImages() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch('/api/images/responsive/mobile')
      .then(res => res.json())
      .then(data => setImages(data.images));
  }, []);

  return (
    <div>
      <h2>Mobile Images</h2>
      {images.map(img => (
        <img key={img.width} src={img.url} alt={`${img.width}x${img.height}`} />
      ))}
    </div>
  );
}
```

### Display All Presets

```jsx
export default function AllPresets() {
  const presets = ['mobile', 'tablet', 'desktop'];

  return (
    <div>
      {presets.map(preset => (
        <PresetSection key={preset} preset={preset} />
      ))}
    </div>
  );
}

function PresetSection({ preset }) {
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch(`/api/images/responsive/${preset}`)
      .then(res => res.json())
      .then(data => setImages(data.images));
  }, [preset]);

  return (
    <section>
      <h2>{preset.charAt(0).toUpperCase() + preset.slice(1)}</h2>
      <div className="gallery">
        {images.map(img => (
          <div key={img.width}>
            <img src={img.url} alt={`${img.width}x${img.height}`} />
            <p>{img.width}×{img.height}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
```

### Responsive Hero Section

```jsx
export default function Hero() {
  const [images, setImages] = useState({});

  useEffect(() => {
    Promise.all([
      fetch('/api/images/responsive/mobile').then(r => r.json()),
      fetch('/api/images/responsive/tablet').then(r => r.json()),
      fetch('/api/images/responsive/desktop').then(r => r.json()),
    ]).then(([mobile, tablet, desktop]) => {
      setImages({ mobile, tablet, desktop });
    });
  }, []);

  if (Object.keys(images).length === 0) return <div>Loading...</div>;

  return (
    <picture>
      <source
        media="(max-width: 480px)"
        srcSet={images.mobile.images[0].url}
      />
      <source
        media="(max-width: 1024px)"
        srcSet={images.tablet.images[0].url}
      />
      <img
        src={images.desktop.images[1].url}
        alt="Hero"
        style={{ width: '100%', height: 'auto' }}
      />
    </picture>
  );
}
```

---

## Testing Responsiveness

### Manual Testing

1. **Mobile**: Open your browser DevTools (F12)
2. Click Device Toolbar (Ctrl+Shift+M)
3. Change device size
4. Verify images load correctly at each size

### Automated Testing

```jsx
import { render, screen } from '@testing-library/react';

test('Hero image loads at mobile size', () => {
  render(<Hero />);
  const img = screen.getByAltText('Hero');
  expect(img).toHaveAttribute('src', expect.stringContaining('320x240'));
});

test('Hero image loads at desktop size', () => {
  // Simulate desktop viewport
  window.innerWidth = 1920;
  render(<Hero />);
  const img = screen.getByAltText('Hero');
  expect(img).toHaveAttribute('src', expect.stringContaining('1920x1080'));
});
```

---

## Common Patterns

### Pattern 1: Simple Responsive Image

**HTML:**
```html
<picture>
  <source srcset="/api/images/responsive/mobile" media="(max-width: 600px)">
  <source srcset="/api/images/responsive/tablet" media="(max-width: 1024px)">
  <img src="/api/images/responsive/desktop" alt="Product">
</picture>
```

**CSS:**
```css
picture img {
  width: 100%;
  height: auto;
  display: block;
}
```

### Pattern 2: Background Image

```css
.hero {
  background-image: url('/api/images/320x240');
  background-size: cover;
  height: 240px;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('/api/images/768x576');
    height: 576px;
  }
}

@media (min-width: 1920px) {
  .hero {
    background-image: url('/api/images/1920x1080');
    height: 1080px;
  }
}
```

### Pattern 3: Grid with Responsive Images

```jsx
const ImageGrid = ({ preset }) => {
  return (
    <div className="grid">
      {preset.images.map(img => (
        <div key={img.width} className="grid-item">
          <img src={img.url} alt={`${img.width}x${img.height}`} />
        </div>
      ))}
    </div>
  );
};
```

---

## Device Specifications

### Mobile Devices

| Device | Width | Height | Ratio |
|--------|-------|--------|-------|
| iPhone SE | 320 | 240 | 4:3 |
| iPhone 12 | 480 | 360 | 4:3 |
| Pixel 5 | 640 | 480 | 4:3 |

### Tablet Devices

| Device | Width | Height | Ratio |
|--------|-------|--------|-------|
| iPad Portrait | 768 | 576 | 4:3 |
| iPad Landscape | 1024 | 768 | 4:3 |

### Desktop Displays

| Display | Width | Height | Ratio |
|---------|-------|--------|-------|
| HD | 1280 | 720 | 16:9 |
| Full HD | 1920 | 1080 | 16:9 |
| 2K | 2560 | 1440 | 16:9 |

---

## Performance Optimization

### Cache Strategy

Preset images are cached by dimension:
- First request: Generate (fast)
- Subsequent requests: Cached (<1ms)

### Best Practices

- ✅ Pre-load critical images
- ✅ Use WebP format (smaller files)
- ✅ Use srcset for responsive loading
- ✅ Test on real devices occasionally

### Example: Pre-load

```jsx
useEffect(() => {
  // Pre-load all images when component mounts
  Promise.all([
    fetch('/api/images/responsive/mobile'),
    fetch('/api/images/responsive/tablet'),
    fetch('/api/images/responsive/desktop'),
  ]);
}, []);
```

---

## Debugging Responsive Issues

### Check Viewport
```javascript
console.log(window.innerWidth);  // Current viewport width
```

### Test Each Preset
```bash
# Test mobile
curl http://localhost:18000/api/images/responsive/mobile | jq

# Test tablet
curl http://localhost:18000/api/images/responsive/tablet | jq

# Test desktop
curl http://localhost:18000/api/images/responsive/desktop | jq
```

### Verify Image Loads
```javascript
const img = new Image();
img.onload = () => console.log('Image loaded!');
img.onerror = () => console.log('Image failed!');
img.src = '/api/images/320x240';
```

---

## Next Steps

- 📷 **[User Images](user-images.md)** - Upload your own images
- 🎯 **[Testing Layouts](testing-layouts.md)** - Complete testing guide
- ⚛️ **[Frontend Integration](../frontend-integration/react-setup.md)** - Full React setup

---

**Device presets make responsive testing easy!** 📱💻🖥️
