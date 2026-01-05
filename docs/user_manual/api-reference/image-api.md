# Image API Reference

Complete reference for all image generation and management endpoints.

---

## Base URL

```
http://localhost:18000/api/images
```

---

## Endpoints

### GET /{width}x{height} - Generate/Serve Image

**Purpose:** Generate or retrieve cached placeholder image

**Request:**

```
GET /api/images/{width}x{height}?format=png&text=Label&identifier=unique-id
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| width | integer | Yes | - | Image width in pixels (1-8000) |
| height | integer | Yes | - | Image height in pixels (1-8000) |
| format | string | No | png | Image format: png, jpeg, webp |
| text | string | No | - | Text overlay (max 200 chars) |
| identifier | string | No | - | Unique identifier for variation |

**Examples:**

```bash
# Simple image
curl http://localhost:18000/api/images/300x200

# With format
curl http://localhost:18000/api/images/300x200?format=webp

# With text overlay
curl "http://localhost:18000/api/images/300x200?text=Product+Image"

# With identifier (different image)
curl http://localhost:18000/api/images/300x200?identifier=card-1
curl http://localhost:18000/api/images/300x200?identifier=card-2

# All parameters
curl "http://localhost:18000/api/images/300x200?format=jpeg&text=Featured&identifier=hero-1"
```

**Response:**

- Content-Type: `image/png`, `image/jpeg`, or `image/webp`
- Status: `200 OK`
- Body: Binary image data

**Example in HTML:**

```html
<img src="http://localhost:18000/api/images/300x200" alt="Product">
<img src="http://localhost:18000/api/images/300x200?format=webp" alt="Product">
<img src="http://localhost:18000/api/images/300x200?text=New&identifier=badge" alt="New badge">
```

**Example in React:**

```jsx
<img
  src={`http://localhost:18000/api/images/${width}x${height}?identifier=${productId}`}
  alt="Product"
/>
```

**Caching:**

- Same dimensions + identifier = cached (instant)
- Different identifier = new image
- Cache-Control: public, max-age=86400

---

### POST /generate - Generate and Return Metadata

**Purpose:** Generate image and get metadata (not binary)

**Request:**

```
POST /api/images/generate
Content-Type: application/json

{
  "width": 300,
  "height": 200,
  "format": "png",
  "text_overlay": "Product",
  "identifier": "prod-1"
}
```

**Request Body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| width | integer | Yes | - | Image width (1-8000) |
| height | integer | Yes | - | Image height (1-8000) |
| format | string | No | png | Format: png, jpeg, webp |
| text_overlay | string | No | - | Text overlay (max 200 chars) |
| identifier | string | No | - | Unique identifier |

**Response:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "original_filename": "generated-300x200",
  "width": 300,
  "height": 200,
  "format": "png",
  "file_size_bytes": 2048,
  "created_at": "2024-01-15T10:30:00Z",
  "url": "http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000"
}
```

**Example with curl:**

```bash
curl -X POST http://localhost:18000/api/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "width": 300,
    "height": 200,
    "format": "webp",
    "text_overlay": "Featured",
    "identifier": "hero-1"
  }'
```

---

### GET /responsive/{preset} - Get Responsive Image Set

**Purpose:** Get URLs for all device variants (mobile, tablet, desktop)

**Request:**

```
GET /api/images/responsive/{preset}
```

**Parameters:**

| Parameter | Type | Required | Values | Description |
|-----------|------|----------|--------|-------------|
| preset | string | Yes | mobile, tablet, desktop, all | Device preset |

**Presets:**

- **mobile**: 320×240, 480×360, 640×480
- **tablet**: 768×576, 1024×768
- **desktop**: 1280×720, 1920×1080, 2560×1440
- **all**: All sizes combined

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

**Examples:**

```bash
# Get mobile preset
curl http://localhost:18000/api/images/responsive/mobile

# Get tablet preset
curl http://localhost:18000/api/images/responsive/tablet

# Get all presets
curl http://localhost:18000/api/images/responsive/all
```

**Example in React:**

```jsx
const response = await fetch('/api/images/responsive/mobile');
const data = await response.json();

return (
  <div>
    {data.images.map(img => (
      <img key={img.width} src={img.url} alt={`${img.width}x${img.height}`} />
    ))}
  </div>
);
```

---

### POST /upload - Upload User Image

**Purpose:** Upload custom image and get auto-detected dimensions

**Request:**

```
POST /api/images/upload
Content-Type: multipart/form-data

file: <image file>
```

**Supported Formats:**
- JPEG, PNG, WebP, GIF, BMP

**Max File Size:** 10 MB (configurable)

**Response:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000",
  "dimensions": {
    "width": 1920,
    "height": 1080
  }
}
```

**Examples:**

**With curl:**

```bash
curl -X POST http://localhost:18000/api/images/upload \
  -F "file=@product.jpg"
```

**With Python:**

```python
import requests

with open('product.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:18000/api/images/upload',
        files={'file': f}
    )
    data = response.json()
    print(data['url'])
```

**With JavaScript:**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/images/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.url);  // Use this URL
```

---

### GET /list - List All Images

**Purpose:** Get all uploaded and generated images

**Request:**

```
GET /api/images/list
```

**Response:**

```json
{
  "images": [
    {
      "image_id": "550e8400-e29b-41d4-a716-446655440000",
      "original_filename": "product.jpg",
      "dimensions": {
        "width": 1920,
        "height": 1080
      },
      "format": "jpeg",
      "created_at": "2024-01-15T10:30:00Z",
      "url": "http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000",
      "is_user_provided": true
    },
    {
      "image_id": "generated-300x200",
      "original_filename": "generated-300x200",
      "dimensions": {
        "width": 300,
        "height": 200
      },
      "format": "png",
      "created_at": "2024-01-15T10:31:00Z",
      "url": "http://localhost:18000/api/images/300x200",
      "is_user_provided": false
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:18000/api/images/list | jq
```

---

### DELETE /{image_id} - Delete Image

**Purpose:** Remove image from storage

**Request:**

```
DELETE /api/images/{image_id}
```

**Response:**

```
HTTP/1.1 204 No Content
```

**Examples:**

```bash
# Delete by image ID
curl -X DELETE http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000

# Verify deletion
curl http://localhost:18000/api/images/list
```

---

## Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Image generated/served successfully |
| 201 | Created | Image uploaded successfully |
| 204 | No Content | Image deleted successfully |
| 400 | Bad Request | Invalid dimensions, format, or file |
| 404 | Not Found | Image not found |
| 413 | Payload Too Large | File exceeds size limit |
| 500 | Server Error | Internal server error |

---

## Error Responses

**Invalid Dimensions:**

```json
{
  "error": "Invalid dimensions",
  "detail": "Width and height must be between 1 and 8000"
}
```

**Invalid Format:**

```json
{
  "error": "Invalid format",
  "detail": "Format must be png, jpeg, or webp"
}
```

**File Too Large:**

```json
{
  "error": "File too large",
  "detail": "Maximum upload size is 10 MB"
}
```

**Invalid Image:**

```json
{
  "error": "Invalid image",
  "detail": "File is not a valid image"
}
```

---

## Headers

**Request Headers:**

```
Content-Type: application/json        (for JSON requests)
Content-Type: multipart/form-data     (for file uploads)
```

**Response Headers:**

```
Content-Type: image/png|jpeg|webp    (for image responses)
Cache-Control: public, max-age=86400  (for generated images)
Content-Length: <size>                (image size in bytes)
```

---

## Configuration

### Environment Variables

```env
IMAGE_STORAGE_PATH=./storage/images
IMAGE_MAX_DIMENSION=8000
IMAGE_MAX_UPLOAD_MB=10
IMAGE_DEFAULT_FORMAT=png
IMAGE_CACHE_ENABLED=true
```

---

## Rate Limiting

Currently no rate limiting on image endpoints.

Recommendations:
- Cache requests on frontend
- Use responsive images (don't request all sizes)
- Pre-generate commonly used sizes

---

## Performance

### Generation Time

| Size | Time | Notes |
|------|------|-------|
| 300×300 | <50ms | First request |
| 300×300 | <1ms | Cached |
| 1920×1080 | <100ms | Large image |
| 2560×1440 | <150ms | Very large |

### Network Size

| Format | 300×300 | 1920×1080 |
|--------|---------|-----------|
| PNG | ~2KB | ~20KB |
| JPEG | ~1KB | ~15KB |
| WebP | ~0.5KB | ~8KB |

---

## Complete Example: Product Gallery

```jsx
import { useEffect, useState } from 'react';

export default function ProductGallery() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    // Get responsive image set
    fetch('/api/images/responsive/mobile')
      .then(r => r.json())
      .then(data => setImages(data.images));
  }, []);

  return (
    <div className="gallery">
      {images.map(img => (
        <img
          key={img.width}
          src={img.url}
          alt={`Product ${img.width}x${img.height}`}
          style={{ maxWidth: '100%', margin: '10px' }}
        />
      ))}
    </div>
  );
}
```

---

## SDKs & Tools

### Generate URLs Programmatically

```javascript
function generateImageUrl(width, height, options = {}) {
  const base = `http://localhost:18000/api/images/${width}x${height}`;
  const params = new URLSearchParams();

  if (options.format) params.append('format', options.format);
  if (options.text) params.append('text', options.text);
  if (options.identifier) params.append('identifier', options.identifier);

  return params.toString() ? `${base}?${params}` : base;
}

// Usage
const url = generateImageUrl(300, 200, {
  format: 'webp',
  text: 'Product',
  identifier: 'prod-1'
});
```

---

## Troubleshooting

**Q: Image not displaying**
A: Check URL is correct, verify Mimicus is running, check browser console

**Q: Upload fails with "too large"**
A: File exceeds 10MB limit, compress before uploading

**Q: Dimensions auto-detected wrong**
A: Image may be corrupted, try re-exporting from design tool

**Q: Different devices get different images**
A: Use same identifier for consistency across devices

---

## Next Steps

- 📖 **[Dynamic Generation](../image-mocking/dynamic-generation.md)** - Learn usage patterns
- 📱 **[Responsive Images](../image-mocking/responsive-images.md)** - Device presets
- 🎯 **[Testing Layouts](../image-mocking/testing-layouts.md)** - Complete testing guide

---

**You have all the information you need to integrate image mocking!** 🎨
