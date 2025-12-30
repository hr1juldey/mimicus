# Key Variable Name List for Mimicus Project

This document defines the standardized variable names to be used throughout the Mimicus project to ensure consistency and prevent silent failures due to incorrect parameter passing.

## 1. Mock Definition Variables
- `mock_id`: Unique identifier for a mock definition (UUID)
- `mock_name`: Human-readable name for the mock
- `mock_priority`: Priority level for matching (higher = earlier)
- `mock_enabled`: Boolean flag to enable/disable the mock
- `mock_mode`: Mode of operation (mock, proxy, record, passthrough)
- `mock_match`: Matching criteria object
- `mock_response`: Response configuration object
- `mock_state`: State persistence configuration
- `mock_hooks`: Pre/post execution hooks

## 2. Matching Variables
- `match_method`: HTTP method to match (GET, POST, etc.)
- `match_path`: Path pattern to match (supports templates/regex)
- `match_headers`: Headers to match against
- `match_query`: Query parameters to match against
- `match_body`: Body content matching criteria (JSONPath/regex)
- `match_content_type`: Content type to match

## 3. Response Variables
- `response_status`: HTTP status code to return
- `response_headers`: Headers to include in response
- `response_body`: Response body content (static or template)
- `response_delay_ms`: Delay in milliseconds before response
- `response_repeat_policy`: Policy for repeating responses
- `response_variants`: Weighted variants for A/B testing

## 4. Request Context Variables
- `request_method`: HTTP method of incoming request
- `request_path`: Path of incoming request
- `request_headers`: Headers of incoming request
- `request_query_params`: Query parameters of incoming request
- `request_body`: Body content of incoming request
- `request_json`: Parsed JSON content of incoming request
- `request_path_params`: Path parameters extracted from request

## 5. State Variables
- `state_persist_to`: Storage backend for state (redis/db)
- `state_keys`: List of keys to persist in state
- `session_id`: Unique identifier for session-based state
- `state_data`: Actual state data dictionary

## 6. Configuration Variables
- `config_database_url`: Database connection URL
- `config_redis_url`: Redis connection URL
- `config_upstream_url`: Upstream service URL for proxy mode
- `config_api_key`: API key for admin access
- `config_mock_mode`: Global mock mode setting
- `config_rate_limit`: Rate limiting configuration

## 7. Service Variables
- `matching_service`: Instance of matching service
- `response_service`: Instance of response service
- `template_service`: Instance of template service
- `mock_repository`: Instance of mock repository

## 8. HTTP Client Variables
- `http_client`: HTTP client instance for proxy operations
- `upstream_url`: Target URL for proxy requests
- `proxy_headers`: Headers to forward to upstream service
- `timeout_seconds`: Request timeout configuration