// src/lib/theme-config.ts
import { THEME_CONFIG } from '@/lib/constants';

export interface ThemeOptions {
  primaryColor: string;
  secondaryColor: string;
  backgroundColor: string;
  textColor: string;
  borderRadius: string;
  fontFamily: string;
}

export const DEFAULT_THEME: ThemeOptions = {
  primaryColor: '#000000', // Black
  secondaryColor: '#444444', // Dark gray
  backgroundColor: '#ffffff', // White
  textColor: '#000000', // Black
  borderRadius: '0.5rem', // 8px
  fontFamily: 'Inter, system-ui, sans-serif',
};

export const DARK_THEME: ThemeOptions = {
  primaryColor: '#ffffff', // White
  secondaryColor: '#cccccc', // Light gray
  backgroundColor: '#000000', // Black
  textColor: '#ffffff', // White
  borderRadius: '0.5rem', // 8px
  fontFamily: 'Inter, system-ui, sans-serif',
};

export const CUSTOM_THEMES: Record<string, ThemeOptions> = {
  'minimalist-dark': {
    primaryColor: '#ffffff',
    secondaryColor: '#aaaaaa',
    backgroundColor: '#1a1a1a',
    textColor: '#ffffff',
    borderRadius: '0',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  'typewriter': {
    primaryColor: '#000000',
    secondaryColor: '#555555',
    backgroundColor: '#f5f5f5',
    textColor: '#000000',
    borderRadius: '0',
    fontFamily: '"Courier New", Courier, monospace',
  },
};

export function getTheme(name?: string): ThemeOptions {
  if (name && CUSTOM_THEMES[name]) {
    return CUSTOM_THEMES[name];
  }
  return DEFAULT_THEME;
}

export function applyTheme(theme: ThemeOptions) {
  const root = document.documentElement;
  root.style.setProperty('--color-primary', theme.primaryColor);
  root.style.setProperty('--color-secondary', theme.secondaryColor);
  root.style.setProperty('--color-background', theme.backgroundColor);
  root.style.setProperty('--color-text', theme.textColor);
  root.style.setProperty('--radius', theme.borderRadius);
  root.style.setProperty('--font-family', theme.fontFamily);
}