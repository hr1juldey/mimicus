# Low-Level Design: FastAPI Universal Mock & Mimic

## 1. Executive Summary

This document details the low-level design of the Mimicus project, focusing on the modular architecture with clear separation of concerns. The implementation follows SOLID principles, DRY principles, and Domain-Driven Design patterns as specified in QWEN.md. Each module and submodule is designed to be under 100 lines of code with maximum 50 lines of overhead, excluding test files.

## 2. Project Structure

```bash
src/
├── __init__.py
├── main.py
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── app.py              # FastAPI application instance
│   ├── config.py           # Configuration management
│   ├── dependencies.py     # Dependency injection
│   └── middleware/         # Request/response processing
│       ├── __init__.py
│       ├── auth.py
│       ├── cors.py
│       └── logging.py
├── domain/                 # Domain layer (business logic)
│   ├── __init__.py
│   ├── entities/           # Domain entities
│   │   ├── __init__.py
│   │   ├── mock_definition.py
│   │   └── request_context.py
│   ├── services/           # Domain services
│   │   ├── __init__.py
│   │   ├── matching_service.py
│   │   ├── response_service.py
│   │   └── template_service.py
│   └── repositories/       # Domain repositories
│       ├── __init__.py
│       └── mock_repository.py
├── infrastructure/         # Infrastructure layer
│   ├── __init__.py
│   ├── database/           # Database implementations
│   │   ├── __init__.py
│   │   ├── models.py       # SQLModel definitions
│   │   └── connection.py   # Database connection
│   ├── cache/              # Caching implementations
│   │   ├── __init__.py
│   │   └── redis_client.py
│   ├── storage/            # File/object storage
│   │   ├── __init__.py
│   │   └── file_storage.py
│   └── external/           # External service integrations
│       ├── __init__.py
│       ├── http_client.py
│       └── openapi_importer.py
├── application/            # Application layer (use cases)
│   ├── __init__.py
│   ├── dtos/               # Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── mock_dtos.py
│   │   └── request_dtos.py
│   ├── use_cases/          # Business logic orchestrators
│   │   ├── __init__.py
│   │   ├── create_mock.py
│   │   ├── update_mock.py
│   │   ├── delete_mock.py
│   │   └── find_mock.py
│   └── mappers/            # DTO to Entity mappers
│       ├── __init__.py
│       └── mock_mapper.py
└── presentation/           # Presentation layer (API endpoints)
    ├── __init__.py
    ├── api/                # API routes
    │   ├── __init__.py
    │   ├── v1/             # Version 1 API
    │   │   ├── __init__.py
    │   │   ├── mocks.py    # Mock management endpoints
    │   │   ├── admin.py    # Admin endpoints
    │   │   └── proxy.py    # Proxy endpoints
    │   └── health.py       # Health check endpoint
    └── serializers/        # Serialization logic
        ├── __init__.py
        └── mock_serializer.py
```

## 3. Module Descriptions

### 3.1 Core Module

The core module contains the foundational components of the application.

#### 3.1.1 app.py

- Creates and configures the FastAPI application
- Registers middleware, exception handlers, and event handlers
- Implements the application factory pattern

#### 3.1.2 config.py

- Defines application settings using Pydantic Settings
- Handles environment variable loading
- Manages configuration validation

#### 3.1.3 dependencies.py

- Contains dependency injection functions
- Provides database sessions, cache clients, etc.
- Implements security dependencies

#### 3.1.4 Middleware Submodule

- **auth.py**: Authentication and authorization middleware
- **cors.py**: Cross-origin resource sharing configuration
- **logging.py**: Request/response logging middleware

### 3.2 Domain Module

The domain module contains business logic and domain entities.

#### 3.2.1 Entities Submodule

- **mock_definition.py**: Defines the MockDefinition entity with validation
- **request_context.py**: Represents the context of an incoming request

#### 3.2.2 Services Submodule

- **matching_service.py**: Implements request matching logic
- **response_service.py**: Handles response generation
- **template_service.py**: Manages Jinja2 template rendering

#### 3.2.3 Repositories Submodule

- **mock_repository.py**: Data access operations for mock definitions

### 3.3 Infrastructure Module

The infrastructure module handles external integrations and data persistence.

#### 3.3.1 Database Submodule

- **models.py**: SQLModel entity definitions
- **connection.py**: Database connection management

#### 3.3.2 Cache Submodule

- **redis_client.py**: Redis client wrapper with helper methods

#### 3.3.3 Storage Submodule

- **file_storage.py**: File/object storage abstraction

#### 3.3.4 External Submodule

- **http_client.py**: HTTP client for proxy functionality
- **openapi_importer.py**: OpenAPI specification parser and converter

### 3.4 Application Module

The application module orchestrates business logic and contains use cases.

#### 3.4.1 DTOs Submodule

- **mock_dtos.py**: Data Transfer Objects for mock operations
- **request_dtos.py**: DTOs for request/response handling

#### 3.4.2 Use Cases Submodule

- **create_mock.py**: Use case for creating new mock definitions
- **update_mock.py**: Use case for updating existing mock definitions
- **delete_mock.py**: Use case for deleting mock definitions
- **find_mock.py**: Use case for finding and matching mock definitions

#### 3.4.3 Mappers Submodule

- **mock_mapper.py**: Maps between DTOs and domain entities

### 3.5 Presentation Module

The presentation module handles API endpoints and serialization.

#### 3.5.1 API Submodule

- **mocks.py**: Endpoints for mock management (CRUD operations)
- **admin.py**: Administrative endpoints
- **proxy.py**: Proxy endpoints that forward requests to upstream services
- **health.py**: Health check endpoint

#### 3.5.2 Serializers Submodule

- **mock_serializer.py**: Serialization/deserialization logic for mock data

## 4. Key Variable Name List

### 4.1 Mock Definition Variables

- `mock_id`: Unique identifier for a mock definition (UUID)
- `mock_name`: Human-readable name for the mock
- `mock_priority`: Priority level for matching (higher = earlier)
- `mock_enabled`: Boolean flag to enable/disable the mock
- `mock_mode`: Mode of operation (mock, proxy, record, passthrough)
- `mock_match`: Matching criteria object
- `mock_response`: Response configuration object
- `mock_state`: State persistence configuration
- `mock_hooks`: Pre/post execution hooks

### 4.2 Matching Variables

- `match_method`: HTTP method to match (GET, POST, etc.)
- `match_path`: Path pattern to match (supports templates/regex)
- `match_headers`: Headers to match against
- `match_query`: Query parameters to match against
- `match_body`: Body content matching criteria (JSONPath/regex)
- `match_content_type`: Content type to match

### 4.3 Response Variables

- `response_status`: HTTP status code to return
- `response_headers`: Headers to include in response
- `response_body`: Response body content (static or template)
- `response_delay_ms`: Delay in milliseconds before response
- `response_repeat_policy`: Policy for repeating responses
- `response_variants`: Weighted variants for A/B testing

### 4.4 Request Context Variables

- `request_method`: HTTP method of incoming request
- `request_path`: Path of incoming request
- `request_headers`: Headers of incoming request
- `request_query_params`: Query parameters of incoming request
- `request_body`: Body content of incoming request
- `request_json`: Parsed JSON content of incoming request
- `request_path_params`: Path parameters extracted from request

### 4.5 State Variables

- `state_persist_to`: Storage backend for state (redis/db)
- `state_keys`: List of keys to persist in state
- `session_id`: Unique identifier for session-based state
- `state_data`: Actual state data dictionary

### 4.6 Configuration Variables

- `config_database_url`: Database connection URL
- `config_redis_url`: Redis connection URL
- `config_upstream_url`: Upstream service URL for proxy mode
- `config_api_key`: API key for admin access
- `config_mock_mode`: Global mock mode setting
- `config_rate_limit`: Rate limiting configuration

### 4.7 Service Variables

- `matching_service`: Instance of matching service
- `response_service`: Instance of response service
- `template_service`: Instance of template service
- `mock_repository`: Instance of mock repository

### 4.8 HTTP Client Variables

- `http_client`: HTTP client instance for proxy operations
- `upstream_url`: Target URL for proxy requests
- `proxy_headers`: Headers to forward to upstream service
- `timeout_seconds`: Request timeout configuration

## 5. Implementation Guidelines

### 5.1 SOLID Principles Implementation

- **SRP**: Each class has a single responsibility (e.g., MatchingService only handles matching)
- **OCP**: Use abstract base classes and dependency injection for extensibility
- **LSP**: Subtypes properly extend parent behavior without breaking contracts
- **ISP**: Create focused interfaces with minimal methods
- **DIP**: Depend on abstractions rather than concrete implementations

### 5.2 DRY Principles Implementation

- Extract common functionality into reusable utility functions
- Use configuration files for repeated values
- Implement base classes for shared behavior
- Create generic templates for similar operations

### 5.3 Domain-Driven Design Implementation

- Use ubiquitous language consistently across codebase
- Define clear bounded contexts for different domains
- Implement entities, value objects, and aggregates appropriately
- Separate domain logic from infrastructure concerns

### 5.4 File Size Constraints

- Each Python file must be under 100 lines of code
- Maximum 50 lines of overhead (imports, comments, blank lines)
- Test files are exempt from this constraint
- Split large modules into smaller, focused components

## 6. Data Flow

### 6.1 Request Processing Flow

1. Incoming request arrives at presentation layer
2. Request is validated and converted to DTO
3. Use case orchestrates domain services
4. Matching service finds appropriate mock definition
5. Response service generates response using template service
6. Response is serialized and returned

### 6.2 Mock Creation Flow

1. Admin API receives mock creation request
2. DTO is validated and converted to domain entity
3. Use case persists mock definition to repository
4. Cache is updated if applicable
5. Success response is returned

## 7. Error Handling Strategy

### 7.1 Domain Layer

- Domain entities validate their own state
- Domain services handle domain-specific errors
- Use custom exceptions that extend base domain exceptions

### 7.2 Application Layer

- Use cases handle transaction boundaries
- Convert domain exceptions to application-level exceptions
- Implement retry logic where appropriate

### 7.3 Infrastructure Layer

- Handle connection failures gracefully
- Implement circuit breaker pattern for external services
- Log infrastructure-level errors with appropriate context

### 7.4 Presentation Layer

- Convert application exceptions to HTTP responses
- Implement global exception handlers
- Provide meaningful error messages to clients

## 8. Security Considerations

### 8.1 Input Validation

- Validate all incoming requests at the presentation layer
- Sanitize user input before processing
- Implement proper escaping for template rendering

### 8.2 Access Control

- Implement authentication and authorization middleware
- Use API keys for admin access
- Validate permissions for each operation

### 8.3 Proxy Security

- Implement domain whitelisting for proxy operations
- Prevent proxying to private networks
- Sanitize headers forwarded to upstream services

## 9. Performance Considerations

### 9.1 Caching Strategy

- Cache compiled Jinja2 templates
- Cache frequently accessed mock definitions
- Implement LRU cache for matching results

### 9.2 Database Optimization

- Use connection pooling
- Implement proper indexing on database tables
- Use async database operations where possible

### 9.3 Response Generation

- Pre-compile templates during startup
- Cache template contexts where appropriate
- Implement streaming for large responses
