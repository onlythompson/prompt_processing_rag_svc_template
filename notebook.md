rag-microservice/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conversation_routes.py
│   │   │   │   └── query_routes.py
│   │   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── request/
│   │   │   │   │   ├── conversation_request.py
│   │   │   │   │   └── query_request.py
│   │   │   │   └── response/
│   │   │   │       ├── conversation_response.py
│   │   │   │       └── query_response.py
│   │   │   └── controllers/
│   │   │       ├── __init__.py
│   │   │       ├── conversation_controller.py
│   │   │       └── query_controller.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   └── vector_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── tour.py
│   │   ├── poi.py
│   │   └── story.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   ├── data_sync_service.py
│   │   ├── memory_service.py
│   │   ├── summary_service.py
│   │   └── retrieval_service.py
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── conversation_chain.py
│   │   ├── summary_chain.py
│   │   └── rag_chain.py
│   └── utils/
│       ├── __init__.py
│       └── prefiltering.py
│
├── cross_cutting/
│   ├── __init__.py
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── tracing.py
│   │   └── metrics.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   └── authorization.py
│   ├── caching/
│   │   ├── __init__.py
│   │   └── redis_cache.py
│   ├── resilience/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   └── rate_limiter.py
│   └── compression/
│       ├── __init__.py
│       └── llm_lingua.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── data_ingestion.py
│   └── index_creation.py
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── jaeger/
│       └── jaeger.yml
│
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── cross_cutting_concerns.md
│
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── kubernetes/
│       ├── deployment.yaml
│       └── service.yaml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml