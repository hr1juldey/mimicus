// src/types/api.ts

export interface MockDefinition {
  id: string;
  name: string;
  enabled: boolean;
  priority: number;
  mode: 'mock' | 'proxy';
  match: {
    method: string;
    path: string;
    headers?: Record<string, string>;
    query?: Record<string, string>;
    body?: string;
  };
  response: {
    status: number;
    headers?: Record<string, string>;
    body: string;
    delay?: number;
    error_rate?: number;
    error_status_code?: number;
    error_body?: string;
  };
  proxy_config?: {
    upstream_url: string;
    proxy_headers?: Record<string, string>;
  };
  created_at: string;
  updated_at: string;
}

export interface RequestLog {
  id: string;
  request_method: string;
  request_path: string;
  request_headers: Record<string, string>;
  request_body: string;
  response_status: number;
  response_headers: Record<string, string>;
  response_body: string;
  matched_mock_id?: string;
  client_ip: string;
  session_id: string;
  created_at: string;
}

export interface StateValue {
  id: string;
  key: string;
  value: string;
  session_id: string;
  mock_id?: string;
  client_ip?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateMockRequest {
  name: string;
  enabled: boolean;
  priority: number;
  mode: 'mock' | 'proxy';
  match: {
    method: string;
    path: string;
    headers?: Record<string, string>;
    query?: Record<string, string>;
    body?: string;
  };
  response: {
    status: number;
    headers?: Record<string, string>;
    body: string;
    delay?: number;
    error_rate?: number;
    error_status_code?: number;
    error_body?: string;
  };
  proxy_config?: {
    upstream_url: string;
    proxy_headers?: Record<string, string>;
  };
}

export interface UpdateMockRequest extends CreateMockRequest {
  id: string;
}