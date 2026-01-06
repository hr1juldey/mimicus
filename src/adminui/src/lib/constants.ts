// src/lib/constants.ts

export const THEME_CONFIG = {
  default: 'system',
  storageKey: 'mimicus-theme',
} as const;

export const API_ENDPOINTS = {
  mocks: {
    getAll: '/api/admin/mocks',
    getById: (id: string) => `/api/admin/mocks/${id}`,
    create: '/api/admin/mocks',
    update: (id: string) => `/api/admin/mocks/${id}`,
    delete: (id: string) => `/api/admin/mocks/${id}`,
  },
  inspector: {
    requests: '/api/admin/inspector/requests',
    requestById: (id: string) => `/api/admin/inspector/requests/${id}`,
  },
  state: {
    getAll: '/api/admin/state',
    getBySession: (sessionId: string) => `/api/admin/state?session_id=${sessionId}`,
    create: '/api/admin/state',
    update: (id: string) => `/api/admin/state/${id}`,
    delete: (id: string) => `/api/admin/state/${id}`,
  },
} as const;

export const MOCK_MODES = ['mock', 'proxy'] as const;
export type MockMode = typeof MOCK_MODES[number];

export const HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'] as const;
export type HttpMethod = typeof HTTP_METHODS[number];