# RAG-Powered Microservice Template

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Architecture Overview](#architecture-overview)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Core Components](#core-components)
   - [FastAPI Application](#fastapi-application)
   - [LangChain Integration](#langchain-integration)
   - [MongoDB and Vector Search](#mongodb-and-vector-search)
   - [RAG Implementation](#rag-implementation)
7. [API Reference](#api-reference)
   - [Query Endpoint](#query-endpoint)
   - [Conversation Endpoint](#conversation-endpoint)
8. [Development Guide](#development-guide)
   - [Adding New Features](#adding-new-features)
   - [Testing](#testing)
   - [Code Style and Linting](#code-style-and-linting)
9. [Deployment](#deployment)
   - [Docker](#docker)
   - [Kubernetes](#kubernetes)
10. [Monitoring and Observability](#monitoring-and-observability)
    - [Logging](#logging)
    - [Metrics](#metrics)
    - [Tracing](#tracing)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)
15. [License](#license)
16. [Acknowledgements](#acknowledgements)

## Introduction

This repository serves as a comprehensive template for building a Retrieval-Augmented Generation (RAG) powered microservice. It combines the power of FastAPI, LangChain, and MongoDB to create a scalable, efficient, and intelligent information retrieval and generation system.

RAG enhances the capabilities of large language models by augmenting them with relevant information retrieved from a knowledge base. This approach significantly improves the accuracy and relevance of generated responses, making it ideal for a wide range of AI-driven applications.

## Key Features

- **RAG Architecture**: Implements a state-of-the-art Retrieval-Augmented Generation system.
- **FastAPI Framework**: Utilizes FastAPI for building high-performance, easy-to-use APIs with automatic OpenAPI documentation.
- **LangChain Integration**: Seamlessly integrates with LangChain for advanced language model operations and chain-of-thought processes.
- **MongoDB & Vector Search**: Leverages MongoDB's vector search capabilities for efficient similarity searches and data storage.
- **Asynchronous Design**: Built with asynchronous programming paradigms for optimal performance and scalability.
- **Modular Structure**: Highly modular architecture allowing for easy customization and extension.
- **Comprehensive Observability**: Integrated logging, metrics, and tracing for full system observability.
- **Security Features**: Implements authentication, authorization, and other security best practices.
- **Docker & Kubernetes Support**: Includes configurations for containerization and orchestration, enabling easy deployment and scaling.
- **Extensive Documentation**: Thoroughly documented codebase and API endpoints for ease of use and modification.

## Architecture Overview

The RAG-powered microservice is built on a layered architecture:

1. **API Layer**: FastAPI-based REST API endpoints for query and conversation interfaces.
2. **Service Layer**: Core business logic, including RAG processing, LLM interactions, and data retrieval.
3. **Data Access Layer**: Interfaces with MongoDB for document storage and vector search operations.
4. **LangChain Integration Layer**: Utilizes LangChain for advanced LLM operations and RAG implementation.
5. **Cross-Cutting Concerns**: Handles logging, monitoring, caching, and security across all layers.

![Architecture diagram](/architecture.PNG)

## Getting Started

### Prerequisites

To use this template, ensure you have the following installed:

- Python 3.8+
- MongoDB 4.4+
- Docker (optional, for containerization)
- Kubernetes (optional, for orchestration)

### Installation

1. Use this template to create a new GitHub repository.

2. Clone your new repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your specific configuration values.

### Configuration

1. Database Configuration:
   - Set `MONGODB_URL` in the `.env` file to your MongoDB connection string.
   - Configure database name and collection names in `app/core/config.py`.

2. LLM Configuration:
   - Set `OPENAI_API_KEY` in the `.env` file if using OpenAI's GPT models.
   - Adjust LLM settings in `app/core/config.py`.

3. Vector Store Configuration:
   - Configure vector store settings in `app/db/vector_store.py`.
   - Set index and similarity search parameters as needed.

4. API Configuration:
   - Modify API settings in `app/core/config.py`, including versioning and rate limiting.

## Project Structure

```
rag-microservice/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API routes and request/response models
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   ├── schemas/
│   │   │   └── controllers/
│   ├── core/                   # Core application modules
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── db/                     # Database and vector store interactions
│   │   ├── mongodb.py
│   │   └── vector_store.py
│   ├── models/                 # Data models
│   ├── schemas/                # Pydantic schemas for data validation
│   ├── services/               # Business logic services
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   └── retrieval_service.py
│   ├── chains/                 # LangChain components
│   │   ├── conversation_chain.py
│   │   ├── summary_chain.py
│   │   └── rag_chain.py
│   └── utils/                  # Utility functions
│       └── prefiltering.py
│
├── cross_cutting/              # Cross-cutting concerns
│   ├── observability/
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   └── tracing.py
│   ├── security/
│   │   ├── authentication.py
│   │   └── authorization.py
│   ├── caching/
│   │   └── redis_cache.py
│   ├── resilience/
│   │   ├── circuit_breaker.py
│   │   └── rate_limiter.py
│   └── compression/
│       └── llm_lingua.py
│
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/                    # Utility scripts
│   ├── data_ingestion.py
│   └── index_creation.py
├── monitoring/                 # Monitoring configurations
│   ├── prometheus/
│   ├── grafana/
│   └── jaeger/
├── docs/                       # Additional documentation
├── deployment/                 # Deployment configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── kubernetes/
│
├── requirements.txt            # Project dependencies
├── requirements-dev.txt        # Development dependencies
├── .env.example                # Example environment variable file
├── README.md                   # This file
├── .gitignore
└── pyproject.toml              # Project metadata and configuration
```

## Core Components

### FastAPI Application

The FastAPI application is defined in `app/main.py`. It sets up the API routes, middleware, and initializes core services. Key aspects include:

- API versioning
- CORS middleware
- Authentication middleware
- Exception handlers
- OpenAPI documentation

### LangChain Integration

LangChain is integrated throughout the application, primarily in the `app/chains/` directory:

- `conversation_chain.py`: Implements stateful conversations.
- `summary_chain.py`: Provides text summarization capabilities.
- `rag_chain.py`: Orchestrates the RAG process, combining retrieval and generation.

### MongoDB and Vector Search

MongoDB is used for both document storage and vector search operations:

- `app/db/mongodb.py`: Handles connection and basic CRUD operations.
- `app/db/vector_store.py`: Implements vector storage and similarity search using MongoDB's vector search capabilities.

### RAG Implementation

The RAG (Retrieval-Augmented Generation) process is implemented in `app/services/rag_service.py`. It combines:

1. Query understanding
2. Relevant document retrieval
3. Context preparation
4. LLM-based response generation

## API Reference

### Query Endpoint

- **URL**: `/v1/query`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "query": "string",
    "context": {
      "additional_info": "string"
    }
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "sources": [
      {
        "document": "string",
        "relevance_score": 0.95
      }
    ]
  }
  ```

### Conversation Endpoint

- **URL**: `/v1/conversation`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "conversation_id": "string"
  }
  ```

### Request Flow

![Request Flow](/request_flow.PNG)

## Development Guide

### Adding New Features

1. Create new routes in `app/api/v1/routes/`.
2. Implement corresponding controllers in `app/api/v1/controllers/`.
3. Add new services in `app/services/` for business logic.
4. Extend or create new LangChain components in `app/chains/` if needed.
5. Update API schemas in `app/api/v1/schemas/`.

### Testing

We use pytest for testing. Run the test suite with:

```bash
pytest
```

Add new tests in the `tests/` directory:
- `unit/`: For testing individual components in isolation.
- `integration/`: For testing interactions between components.
- `e2e/`: For testing the entire system from the API level.

### Code Style and Linting

We use Black for code formatting and Flake8 for linting:

```bash
black .
flake8
```

Configure code style settings in `pyproject.toml`.

## Deployment

### Docker

Build the Docker image:

```bash
docker build -t rag-microservice .
```

Run the container:

```bash
docker run -p 8000:8000 rag-microservice
```

### Kubernetes

Apply the Kubernetes configurations:

```bash
kubectl apply -f deployment/kubernetes/
```

This will create the necessary deployments, services, and ingress rules.

## Monitoring and Observability

### Logging

Logging is implemented using Python's built-in logging module, configured in `cross_cutting/observability/logging.py`. Logs are structured in JSON format for easy parsing.

### Metrics

We use Prometheus for metrics collection. Key metrics include:
- Request latency
- Error rates
- RAG processing time
- LLM token usage

Metrics are exposed at `/metrics` endpoint.

### Tracing

Distributed tracing is implemented using OpenTelemetry and Jaeger. This allows for tracking requests across different components of the system.

Configure Jaeger in `monitoring/jaeger/jaeger.yml`.

## Performance Optimization

- Implement caching for frequent queries using Redis (`cross_cutting/caching/redis_cache.py`).
- Use LLM input compression techniques with LLMLingua (`cross_cutting/compression/llm_lingua.py`).
- Optimize MongoDB queries and index usage.
- Implement parallel processing for independent operations.

## Security Considerations

- **Authentication**: JWT-based authentication implemented in `cross_cutting/security/authentication.py`.
- **Authorization**: Role-based access control in `cross_cutting/security/authorization.py`.
- **Rate Limiting**: Implemented in `cross_cutting/resilience/rate_limiter.py`.
- **Input Validation**: Handled by Pydantic schemas in `app/api/v1/schemas/`.
- **Dependency Injection**: Used throughout the application to manage component lifecycles securely.

## Troubleshooting

Common issues and their solutions:

1. **MongoDB Connection Issues**: 
   - Ensure MongoDB is running and accessible.
   - Check the connection string in the `.env` file.

2. **LLM API Errors**:
   - Verify the API key is correct and has sufficient permissions.
   - Check for rate limiting or quota issues.

3. **Slow Query Performance**:
   - Optimize MongoDB indexes.
   - Check the efficiency of vector search operations.

4. **High Memory Usage**:
   - Monitor and adjust the cache size.
   - Optimize large data processing operations.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

Please adhere to the coding standards and add unit tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- FastAPI
- LangChain
- MongoDB
- OpenAI (if using GPT models)
- All other open-source libraries used in this project

---

For more detailed information on specific components, please refer to the documentation in the `docs/` directory.