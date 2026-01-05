# Testing Layouts - Complete Guide

Now that you know how to generate and upload images, let's test your UI layouts across all devices and scenarios!

---

## Testing Strategy

```
Test Coverage:
├─ Mobile layouts (320-640px)
├─ Tablet layouts (768-1024px)
├─ Desktop layouts (1280-2560px)
├─ Different image sizes
├─ Error states
└─ Slow networks
```

---

## Scenario 1: Product Page Responsive Testing

### The Requirement
"Product image should be clear on all devices."

### Manual Testing

**Step 1: Prepare Image URLs**

```bash
# Generate images for each device
Mobile: /api/images/320x240?identifier=product
Tablet: /api/images/768x576?identifier=product
Desktop: /api/images/1920x1080?identifier=product
```

**Step 2: Test on Mobile**

1. Open browser DevTools (F12)
2. Click Device Toolbar (Ctrl+Shift+M)
3. Select iPhone SE (320px)
4. Visit your product page
5. Verify image displays correctly

```html
<!-- HTML to test -->
<img src="/api/images/320x240?identifier=product" alt="Product">
```

**Step 3: Test on Tablet**

1. Change device to iPad (768px)
2. Verify image still looks good
3. Check no overflow or distortion

**Step 4: Test on Desktop**

1. Change to desktop (1920px)
2. Verify image is crisp and clear
3. Check spacing and alignment

### Automated Testing

```javascript
// E2E test using Playwright
import { test, expect } from '@playwright/test';

test.describe('Product Page Images', () => {
  const devices = [
    { name: 'mobile', width: 320, height: 568, imageUrl: '/api/images/320x240' },
    { name: 'tablet', width: 768, height: 1024, imageUrl: '/api/images/768x576' },
    { name: 'desktop', width: 1920, height: 1080, imageUrl: '/api/images/1920x1080' },
  ];

  devices.forEach(device => {
    test(`should render product image on ${device.name}`, async ({ page }) => {
      await page.setViewportSize({ width: device.width, height: device.height });
      await page.goto('/product/1');

      const image = page.locator('img[alt="Product"]');
      await expect(image).toBeVisible();

      // Verify image loaded
      const imageUrl = await image.getAttribute('src');
      expect(imageUrl).toContain(device.imageUrl);
    });
  });
});
```

---

## Scenario 2: Image Grid Layout

### The Requirement
"Product grid should show 1 column on mobile, 2 on tablet, 4 on desktop."

### Test HTML

```html
<div class="product-grid">
  <div class="product-card">
    <img src="/api/images/200x200?identifier=prod-1" alt="Product 1">
  </div>
  <div class="product-card">
    <img src="/api/images/200x200?identifier=prod-2" alt="Product 2">
  </div>
  <div class="product-card">
    <img src="/api/images/200x200?identifier=prod-3" alt="Product 3">
  </div>
  <div class="product-card">
    <img src="/api/images/200x200?identifier=prod-4" alt="Product 4">
  </div>
</div>
```

**CSS:**

```css
.product-grid {
  display: grid;
  gap: 20px;
}

/* Mobile: 1 column */
@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}

/* Tablet: 2 columns */
@media (min-width: 481px) and (max-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 4 columns */
@media (min-width: 1025px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Manual Verification Checklist

- [ ] Mobile (320px): 1 column, images stack vertically
- [ ] Mobile (480px): Still 1 column, fits width
- [ ] Tablet (768px): 2 columns, images evenly spaced
- [ ] Tablet (1024px): 2 columns, scales nicely
- [ ] Desktop (1280px): 4 columns, grid looks balanced
- [ ] Desktop (1920px): 4 columns, proper spacing
- [ ] All images load (no 404)
- [ ] No distortion or stretching
- [ ] Text readable on all sizes

---

## Scenario 3: Hero Banner Responsiveness

### The Requirement
"Hero should look good at any size."

### Test with Responsive Presets

```jsx
export default function Hero() {
  const [preset, setPreset] = useState('mobile');
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch(`/api/images/responsive/${preset}`)
      .then(r => r.json())
      .then(data => setImages(data.images));
  }, [preset]);

  const heroImage = images[0]?.url;

  return (
    <div>
      {/* Preset selector for testing */}
      <div className="controls">
        <button onClick={() => setPreset('mobile')}>Mobile</button>
        <button onClick={() => setPreset('tablet')}>Tablet</button>
        <button onClick={() => setPreset('desktop')}>Desktop</button>
      </div>

      {/* Hero section */}
      <div className="hero" style={{
        backgroundImage: `url('${heroImage}')`,
        backgroundSize: 'cover',
        height: '400px'
      }}>
        <h1>Welcome</h1>
      </div>

      {/* Show all sizes */}
      <div className="previews">
        {images.map(img => (
          <div key={img.width}>
            <img src={img.url} alt={`${img.width}x${img.height}`} />
            <p>{img.width}×{img.height}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Checklist

- [ ] Text readable on all sizes
- [ ] Image fills container without stretching
- [ ] No unwanted cropping on mobile
- [ ] Aspect ratio correct on all devices
- [ ] Text contrast sufficient on all backgrounds

---

## Scenario 4: Error States & Edge Cases

### Test with Generated Images

```html
<!-- Test with different aspect ratios -->
<img src="/api/images/100x300" alt="Tall image">
<img src="/api/images/300x100" alt="Wide image">
<img src="/api/images/50x50" alt="Tiny image">
<img src="/api/images/2560x1440" alt="Huge image">
```

### Checklist

- [ ] Very small images don't break layout
- [ ] Very large images scale properly
- [ ] Tall images don't push footer down
- [ ] Wide images don't overflow container
- [ ] Alt text displays when image fails
- [ ] Loading spinner shows for slow images

---

## Scenario 5: Slow Network Simulation

### Add Delay to Images

```bash
# Simulate 2-second delay
GET /api/images/300x200?text=Slow
```

But Mimicus doesn't support delay parameter yet, so use response templates:

```json
{
  "mock_name": "Slow Image Endpoint",
  "match_method": "GET",
  "match_path": "/api/images-slow/300x200",
  "response_delay_ms": 2000,
  "response_body": "..."
}
```

### Test Slow Network

```jsx
export default function ProductWithSkeleton() {
  const [loading, setLoading] = useState(true);

  return (
    <div className="product">
      {loading && <div className="skeleton"></div>}
      <img
        src="/api/images-slow/300x200"
        alt="Product"
        onLoad={() => setLoading(false)}
        style={{ display: loading ? 'none' : 'block' }}
      />
    </div>
  );
}
```

### Checklist

- [ ] Skeleton/spinner shows while loading
- [ ] No "broken image" icon visible
- [ ] Content below doesn't jump when image loads
- [ ] User can still interact during loading

---

## Scenario 6: Image Upload & Display

### Test Real Images

**Step 1: Upload Image**

```bash
curl -X POST /api/images/upload -F "file=@product.jpg"
# Returns: {"url": "/api/images/550e8400...", "dimensions": {"width": 1920, "height": 1080}}
```

**Step 2: Display in UI**

```jsx
export default function ProductPage() {
  const imageUrl = '/api/images/550e8400...';  // From upload response

  return (
    <img src={imageUrl} alt="Product" style={{ maxWidth: '100%' }} />
  );
}
```

**Step 3: Test on All Devices**

- [ ] Original image displays at full quality
- [ ] Scales down on mobile without quality loss
- [ ] Crops properly in different containers
- [ ] Works in different image contexts (background, img tag, etc.)

---

## Complete Testing Checklist

### Layout Testing

- [ ] Mobile (320-480px): All elements visible, text readable
- [ ] Tablet (768-1024px): Proper two-column layouts
- [ ] Desktop (1280+px): Full layouts with whitespace
- [ ] Extreme sizes (100px, 2560px): No crashes

### Image Testing

- [ ] Generated images display correctly
- [ ] Uploaded images display correctly
- [ ] Different formats (PNG, JPEG, WebP) work
- [ ] Different aspect ratios fit containers
- [ ] No distortion or stretching

### Performance Testing

- [ ] Cached images load instantly (<5ms)
- [ ] Slow images show loading state
- [ ] Responsive images load appropriate size
- [ ] No console errors

### Accessibility Testing

- [ ] Alt text provided for all images
- [ ] Images have proper semantic meaning
- [ ] Text in images readable on all sizes
- [ ] Color contrast sufficient

---

## Tools for Testing

### Browser DevTools

1. Open DevTools (F12)
2. Device Toolbar (Ctrl+Shift+M)
3. Select device or custom size
4. Refresh page and verify layout

### Online Tools

- [BrowserStack](https://www.browserstack.com/) - Test real devices
- [Responsively App](https://responsively.app/) - Multi-device testing
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

### Automated Tools

- **Playwright**: E2E testing across devices
- **Jest**: Unit test image loading
- **Lighthouse**: Performance & accessibility

---

## Recording Tests

### Screenshot Comparison

```javascript
import { test, expect } from '@playwright/test';

test('product page screenshot', async ({ page }) => {
  const devices = ['mobile', 'tablet', 'desktop'];

  for (const device of devices) {
    const viewport = device === 'mobile'
      ? { width: 320, height: 568 }
      : device === 'tablet'
      ? { width: 768, height: 1024 }
      : { width: 1920, height: 1080 };

    await page.setViewportSize(viewport);
    await page.goto('/product/1');
    await expect(page).toHaveScreenshot(`product-${device}.png`);
  }
});
```

---

## Common Issues & Fixes

### Issue: Image distorted on mobile
**Fix:** Use `object-fit: cover` or `object-fit: contain` in CSS

### Issue: Image doesn't load
**Fix:** Check image URL is correct, verify Mimicus is running

### Issue: Layout breaks with large images
**Fix:** Set `max-width: 100%` on images

### Issue: Slow on mobile
**Fix:** Use smaller images, optimize compression

---

## Before/After Comparison

### Before Image Mocking
```
"Let's ship and hope images work on mobile" 😰
```

### After Image Mocking
```
"I've tested on 9 different screen sizes and it looks great!" 🚀
```

---

## CI/CD Integration

```yaml
# GitHub Actions example
name: Test Layouts

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm ci
      - run: npm start &
      - run: npm run test:playwright
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-results
          path: playwright-report/
```

---

## Best Practices Summary

✅ **Do**
- Test on actual devices (not just DevTools)
- Use responsive images (srcset, picture)
- Optimize images before upload
- Automate screenshot testing
- Document layouts by device

❌ **Don't**
- Assume desktop works on mobile
- Use only one image size
- Forget about accessibility
- Skip testing edge cases
- Hardcode image dimensions

---

## Next Steps

- 📚 **[Image API Reference](../api-reference/image-api.md)** - Full endpoint docs
- ⚛️ **[Frontend Integration](../frontend-integration/react-setup.md)** - Use in your app
- 📖 **[Core Features](../core-features/creating-mocks.md)** - Learn more mocking

---

**You're now ready to test layouts with confidence!** 🎨📱💻🖥️
