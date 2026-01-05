# User Images - Upload and Serve

Upload your own images to Mimicus! It automatically detects dimensions and serves them with a clean URL.

---

## Why Upload User Images?

```
Scenario: You have real product images from your designer
Problem: Where do you serve them during frontend development?
Solution: Upload to Mimicus, serve directly
```

---

## Upload Endpoint

```
POST /api/images/upload
```

Accepts multipart file upload. Returns metadata with auto-detected dimensions.

---

## Basic Upload

### Using curl

```bash
curl -X POST http://localhost:18000/api/images/upload \
  -F "file=@product.jpg"
```

**Response:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "/api/images/550e8400-e29b-41d4-a716-446655440000",
  "dimensions": {
    "width": 1920,
    "height": 1080
  }
}
```

### Using Python

```python
import requests

with open('product.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:18000/api/images/upload',
        files=files
    )
    print(response.json())
```

### Using JavaScript

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/images/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.url);  // Use this URL to display the image
```

---

## What Happens When You Upload

### Step 1: Upload File
```bash
POST /api/images/upload with product.jpg
```

### Step 2: Validate
```
✅ File is a valid image
✅ File size < 10MB (configurable)
```

### Step 3: Detect Dimensions
```
Mimicus opens the image
Detects: 1920×1080 pixels
Format: JPEG
```

### Step 4: Store
```
Saved as: product-1920x1080.jpg
(preserves original name + adds dimension suffix)
```

### Step 5: Return Metadata
```json
{
  "image_id": "uuid",
  "url": "/api/images/uuid",
  "dimensions": {"width": 1920, "height": 1080}
}
```

---

## Accessing Uploaded Images

### Direct URL

```html
<img src="http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000" alt="Product">
```

### From Metadata

```javascript
const response = await fetch('/api/images/upload', { ... });
const data = await response.json();

// Use the returned URL
document.querySelector('img').src = data.url;
```

---

## Bulk Upload

### Upload Multiple Images

```bash
# Upload each file
curl -X POST http://localhost:18000/api/images/upload -F "file=@product1.jpg"
curl -X POST http://localhost:18000/api/images/upload -F "file=@product2.jpg"
curl -X POST http://localhost:18000/api/images/upload -F "file=@product3.jpg"
```

### Batch Upload Script

```python
import os
import requests

# Upload all images in a directory
for filename in os.listdir('./images'):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        with open(f'./images/{filename}', 'rb') as f:
            response = requests.post(
                'http://localhost:18000/api/images/upload',
                files={'file': f}
            )
            print(f"{filename} → {response.json()['url']}")
```

---

## React Upload Component

### Simple Upload Form

```jsx
import { useState } from 'react';

export default function ImageUpload() {
  const [preview, setPreview] = useState(null);
  const [url, setUrl] = useState(null);
  const [dimensions, setDimensions] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Show preview
    const reader = new FileReader();
    reader.onload = (event) => setPreview(event.target.result);
    reader.readAsDataURL(file);

    // Upload to Mimicus
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/images/upload', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    setUrl(data.url);
    setDimensions(data.dimensions);
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} />

      {preview && <img src={preview} alt="Preview" style={{ maxWidth: '200px' }} />}

      {url && (
        <div>
          <p>Image uploaded!</p>
          <img src={url} alt="Uploaded" style={{ maxWidth: '200px' }} />
          <p>Dimensions: {dimensions.width}×{dimensions.height}</p>
          <p>URL: {url}</p>
        </div>
      )}
    </div>
  );
}
```

---

## Supported Formats

### Input Formats (Upload)
- ✅ JPEG
- ✅ PNG
- ✅ WebP
- ✅ GIF
- ✅ BMP

### What You Get Back
Same format as you upload:
- Upload JPEG → Served as JPEG
- Upload PNG → Served as PNG
- Upload WebP → Served as WebP

---

## Filename Handling

### Original Filename Preserved

```
Upload: my-product-photo.jpg (dimensions: 1920×1080)
Stored as: my-product-photo-1920x1080.jpg
```

Filename is:
- Descriptive (original name)
- Unique (includes dimensions)
- Easy to find

### Why Dimensions in Filename?

Helps identify images:
```
product-1920x1080.jpg  ← This is the large version
product-640x480.jpg    ← This is the small version (if uploaded)
```

---

## Size Limits

### Default Limits

```
Maximum upload: 10 MB
Maximum dimension: 8000 × 8000 pixels
```

### Change Limits

In `.env`:

```env
IMAGE_MAX_UPLOAD_MB=50      # Allow up to 50 MB files
IMAGE_MAX_DIMENSION=10000   # Allow up to 10000×10000 pixels
```

---

## Common Workflows

### Workflow 1: Designer Uploads Assets

**Designer:**
1. Exports images from Figma
2. Uploads to Mimicus via UI
3. Gets URLs

**Frontend Dev:**
1. Receives URLs from designer
2. Uses URLs in code
3. Images instantly available

**Result:** No file transfer, no hosting setup!

### Workflow 2: Test with Real Images

**Setup:**
1. Upload real product images
2. Use URLs in HTML templates
3. Test layout with realistic content

**Before:**
```html
<!-- Using generated placeholder -->
<img src="/api/images/300x200" alt="Product">
```

**After:**
```html
<!-- Using real uploaded image -->
<img src="/api/images/550e8400-e29b-41d4-a716-446655440000" alt="Product">
```

### Workflow 3: Multiple Versions

Upload same product in different sizes:

```bash
curl -X POST .../upload -F "file=@product-large.jpg"   # 1920×1080
curl -X POST .../upload -F "file=@product-medium.jpg"  # 768×576
curl -X POST .../upload -F "file=@product-small.jpg"   # 320×240
```

Get three different URLs for responsive testing!

---

## List All Uploaded Images

```bash
curl http://localhost:18000/api/images/list
```

**Response:**

```json
{
  "images": [
    {
      "image_id": "550e8400...",
      "original_filename": "product.jpg",
      "dimensions": {"width": 1920, "height": 1080},
      "url": "/api/images/550e8400...",
      "created_at": "2024-01-15T10:30:00Z"
    },
    ...
  ]
}
```

---

## Delete Uploaded Images

```bash
curl -X DELETE http://localhost:18000/api/images/550e8400-e29b-41d4-a716-446655440000
```

Removes the image from storage.

---

## Error Handling

### "Invalid file type"

Uploaded file isn't an image. Try:
- JPEG, PNG, WebP, GIF, BMP

### "File too large"

File exceeds size limit (default 10MB). Try:
- Compress the image
- Increase limit in config

### "Image dimensions too large"

Image is bigger than 8000×8000. Try:
- Resize the image
- Increase limit in config

### "Failed to detect dimensions"

Image is corrupted. Try:
- Re-export from design tool
- Open and re-save in image editor

---

## Best Practices

### ✅ Do

- Use descriptive filenames
- Optimize images before upload (smaller = faster)
- Test with real product images
- Use URLs from upload response

### ❌ Don't

- Upload huge unoptimized images (10MB limit)
- Delete images still in use
- Store sensitive data in image metadata
- Upload same image multiple times (use the URL instead)

---

## Performance Tips

### Optimize Before Upload

```bash
# Compress image
ImageMagick:
convert original.jpg -quality 85 optimized.jpg

# Or use online tool
# https://tinypng.com/
```

### Serve Responsively

```html
<picture>
  <source media="(max-width: 480px)" srcset="/api/images/small">
  <source media="(max-width: 1024px)" srcset="/api/images/medium">
  <img src="/api/images/large" alt="Product">
</picture>
```

---

## Storage Location

Uploaded images are stored in:

```
./storage/images/user/
  ├── product-1920x1080.jpg
  ├── hero-1280x720.png
  └── banner-1920x400.webp
```

All files with dimension-suffixed names.

---

## Next Steps

- 🎯 **[Testing Layouts](testing-layouts.md)** - Complete testing guide
- 📚 **[Image API Reference](../api-reference/image-api.md)** - Full endpoint docs
- ⚛️ **[Frontend Integration](../frontend-integration/react-setup.md)** - Use in React

---

**Upload real images and test with confidence!** 🎨
