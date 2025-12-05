# CodeSnap Infrastructure

This repository contains the infrastructure setup for the CodeSnap microservices project.

## Architecture

- **NATS**: Message broker for inter-service communication
- **PostgreSQL**: Separate databases for each service
- **Keycloak**: Authentication and authorization
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization

## Services

1. **API Gateway** - Entry point, handles routing and authentication
2. **User Service** - Manages user data and profiles
3. **Exercise Service** - Manages coding exercises
4. **Attempt Service** - Handles user submissions and grading
5. **Code Execution Service** - Executes user code safely
6. **AI Service** - Provides AI responses from both the rival and assistant agents

## Getting Started

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in values
3. Start infrastructure: `docker-compose up -d`
4. Verify services are running: `docker-compose ps`

## Database Access

- Users DB: `localhost:5432`
- Exercises DB: `localhost:5433`
- Attempts DB: `localhost:5434`
- Keycloak DB: `localhost:5435`

## Monitoring

- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- NATS Monitoring: http://localhost:8222

## NATS Subjects Convention

- `users.*` - User service messages
- `exercises.*` - Exercise service messages
- `attempts.*` - Attempt service messages
- `code.execute` - Code execution requests
- `ai.assist` - AI assistance requests
```