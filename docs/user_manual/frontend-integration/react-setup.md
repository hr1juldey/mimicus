# React Integration Guide

Connect your React app to Mimicus in minutes!

---

## Prerequisites

- ✅ React 16.8+ (Hooks)
- ✅ Mimicus running on localhost:18000
- ✅ npm or yarn installed

---

## 1. Configure API URL

### Environment Variable Setup

Create `.env` file in your React project root:

```env
REACT_APP_API_URL=http://localhost:18000
REACT_APP_API_ENABLED=true
```

Access in code:

```jsx
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:18000';
```

### Switching Between Mock and Real API

```env
# Development (with mocks)
REACT_APP_API_URL=http://localhost:18000

# Production (real backend)
REACT_APP_API_URL=https://api.example.com
```

No code changes needed—just update `.env`!

---

## 2. Create API Client

### Custom Hook: useApi

```jsx
// hooks/useApi.js
import { useState, useEffect } from 'react';

export function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

### Usage:

```jsx
import { useApi } from './hooks/useApi';

export default function UserProfile() {
  const { data: user, loading, error } = useApi(
    `${process.env.REACT_APP_API_URL}/api/users/1`
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <div>{user.name}</div>;
}
```

---

## 3. Simple Fetch Pattern

### Basic GET Request

```jsx
import { useEffect, useState } from 'react';

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/api/products`
      );
      const data = await response.json();
      setProducts(data);
      setLoading(false);
    };

    fetchProducts();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="products">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          <p>${product.price}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## 4. Add Image Mocking

### Display Generated Images

```jsx
export default function ProductCard({ productId, name, price }) {
  return (
    <div className="product-card">
      {/* Generate placeholder image */}
      <img
        src={`${process.env.REACT_APP_API_URL}/api/images/300x300?identifier=prod-${productId}&text=${name}`}
        alt={name}
      />
      <h3>{name}</h3>
      <p>${price}</p>
    </div>
  );
}
```

### Display Responsive Images

```jsx
import { useEffect, useState } from 'react';

export default function ResponsiveHero() {
  const [preset, setPres et] = useState('mobile');
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/api/images/responsive/${preset}`)
      .then(r => r.json())
      .then(data => setImages(data.images));
  }, [preset]);

  const heroImage = images[0]?.url;

  return (
    <div style={{
      backgroundImage: `url('${heroImage}')`,
      backgroundSize: 'cover',
      height: '400px'
    }}>
      <h1>Welcome</h1>
    </div>
  );
}
```

### Upload User Images

```jsx
import { useState } from 'react';

export default function ImageUpload() {
  const [preview, setPreview] = useState(null);
  const [uploaded, setUploaded] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Show preview
    const reader = new FileReader();
    reader.onload = event => setPreview(event.target.result);
    reader.readAsDataURL(file);

    // Upload to Mimicus
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `${process.env.REACT_APP_API_URL}/api/images/upload`,
      { method: 'POST', body: formData }
    );

    const data = await response.json();
    setUploaded(data);
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} />

      {preview && <img src={preview} alt="Preview" style={{maxWidth: '200px'}} />}

      {uploaded && (
        <div>
          <img src={uploaded.url} alt="Uploaded" />
          <p>Size: {uploaded.dimensions.width}×{uploaded.dimensions.height}</p>
        </div>
      )}
    </div>
  );
}
```

---

## 5. Error Handling

### With Error Boundary

```jsx
import { Component } from 'react';

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>Failed to load data. Please try again.</div>;
    }

    return this.props.children;
  }
}
```

### Graceful Fallback

```jsx
export default function DataDisplay() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/api/data`)
      .then(r => r.json())
      .catch(err => {
        console.warn('API failed, using mock data:', err);
        setData({ fallback: true, message: 'Using cached data' });
      })
      .then(json => setData(json));
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      {data.fallback && <p className="warning">Offline - showing cached data</p>}
      {data.message}
    </div>
  );
}
```

---

## 6. Switching to Production

### Before (Development)

```env
REACT_APP_API_URL=http://localhost:18000
```

### After (Production)

```env
REACT_APP_API_URL=https://api.example.com
```

### Build Commands

```bash
# Development (uses Mimicus)
npm start

# Production (uses real API)
REACT_APP_API_URL=https://api.example.com npm run build
```

---

## 7. Complete Example: Product Page

```jsx
// pages/ProductPage.jsx
import { useEffect, useState } from 'react';

export default function ProductPage({ productId }) {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/api/products/${productId}`
        );
        if (!response.ok) throw new Error('Not found');
        const data = await response.json();
        setProduct(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  if (loading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!product) return <div>Not found</div>;

  return (
    <div className="product-page">
      {/* Generated image */}
      <img
        src={`${process.env.REACT_APP_API_URL}/api/images/400x400?identifier=prod-${product.id}`}
        alt={product.name}
      />

      <h1>{product.name}</h1>
      <p>${product.price}</p>
      <p>{product.description}</p>

      <button onClick={() => console.log('Add to cart')}>
        Add to Cart
      </button>
    </div>
  );
}
```

---

## 8. Testing with Mocks

### Jest + MSW (Mock Service Worker)

```bash
npm install -D msw
```

### Mock Setup

```javascript
// mocks/handlers.js
import { rest } from 'msw';

const API_URL = process.env.REACT_APP_API_URL;

export const handlers = [
  rest.get(`${API_URL}/api/products`, (req, res, ctx) => {
    return res(
      ctx.json([
        { id: 1, name: 'Laptop', price: 999 },
        { id: 2, name: 'Mouse', price: 29 },
      ])
    );
  }),

  rest.get(`${API_URL}/api/products/:id`, (req, res, ctx) => {
    return res(
      ctx.json({
        id: req.params.id,
        name: 'Product',
        price: 99,
        description: 'A great product'
      })
    );
  }),
];
```

### Test Example

```javascript
// ProductPage.test.jsx
import { render, screen } from '@testing-library/react';
import ProductPage from './ProductPage';

test('displays product details', async () => {
  render(<ProductPage productId="1" />);

  expect(screen.getByText('Product')).toBeInTheDocument();
  expect(screen.getByText('$99')).toBeInTheDocument();
});
```

---

## Best Practices

### ✅ Do

- Use environment variables for API URL
- Handle loading and error states
- Cache responses when appropriate
- Use TypeScript for type safety (optional)
- Test with mocks before switching to real API

### ❌ Don't

- Hardcode API URLs
- Ignore loading states
- Forget error handling
- Make requests without try/catch
- Assume API is always available

---

## TypeScript Version

```typescript
// types/api.ts
export interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
}

export interface ImageMetadata {
  image_id: string;
  url: string;
  dimensions: {
    width: number;
    height: number;
  };
}

// hooks/useApi.ts
import { useState, useEffect } from 'react';

export function useApi<T>(url: string): {
  data: T | null;
  loading: boolean;
  error: string | null;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(r => r.json())
      .then(json => setData(json))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

---

## Next Steps

- 🖼️ **[Image Mocking](../image-mocking/overview.md)** - Image features
- 💾 **[API Reference](../api-reference/image-api.md)** - Full API docs
- 🏪 **[E-Commerce Tutorial](../tutorials/ecommerce-store.md)** - Complete example

---

**Your React app is now connected to Mimicus!** ⚛️
