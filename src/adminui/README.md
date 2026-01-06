# Mimicus Admin UI

The admin interface for managing Mimicus mock services. Built with Next.js, TypeScript, and shadcn/ui.

## Features

- Mock management: Create, edit, and delete API mocks
- Request inspector: View and debug incoming requests
- State management: Manage session and global state
- Image generation: Create placeholder images for mocks
- Settings: Configure API keys and system settings

## Tech Stack

- [Next.js](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [shadcn/ui](https://ui.shadcn.com/) - Accessible UI components
- [Radix UI](https://www.radix-ui.com/) - Accessible primitives

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the Mimicus API (defaults to http://localhost:8000)

## Theming

The UI supports both light and dark modes, with a default black and white theme. Themes can be customized through the centralized theme configuration in `src/lib/theme-config.ts`.

## Project Structure

```
src/
├── app/              # Next.js app router pages
├── components/       # Reusable UI components
│   ├── ui/           # shadcn/ui components
│   └── layout/       # Layout components
├── lib/              # Utilities and configuration
├── types/            # TypeScript type definitions
├── styles/           # Global styles
└── hooks/            # Custom React hooks
```

## API Integration

The UI communicates with the Mimicus backend through the API client in `src/lib/api-client.ts`. All API endpoints are defined in `src/lib/constants.ts`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
