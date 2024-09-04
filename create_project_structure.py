import os
from pathlib import Path

def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def create_file(path):
    Path(path).touch()

def create_project_structure():
    # Root directory
    root = Path(os.getcwd())
    create_directory(root)

    # App directory
    app_dir =  root / "app"
    create_directory(app_dir)
    create_file(app_dir / "main.py")

    # API directory
    api_dir = app_dir / "api"
    create_directory(api_dir)
    create_file(api_dir / "__init__.py")
    # create_file(api_dir / "dependencies.py")

    # API v1 directory
    api_v1_dir = api_dir / "v1"
    create_directory(api_v1_dir)
    create_file(api_v1_dir / "__init__.py")

    for subdir in ["routes", "schemas", "controllers"]:
        subdir_path = api_v1_dir / subdir
        create_directory(subdir_path)
        create_file(subdir_path / "__init__.py")

    # Create specific files in API v1 subdirectories
    create_file(api_v1_dir / "routes" / "__init__.py")
    create_file(api_v1_dir / "routes" / "admin_routes.py")
    create_file(api_v1_dir / "routes" / "query_routes.py")

    for schema_type in ["request", "response"]:
        schema_dir = api_v1_dir / "schemas" / schema_type
        create_directory(schema_dir)
        create_file(schema_dir / "__init__.py")
        create_file(schema_dir / "conversation_{schema_type}.py")
        create_file(schema_dir / "query_{schema_type}.py")

    create_file(api_v1_dir / "controllers" / "conversation_controller.py")
    create_file(api_v1_dir / "controllers" / "query_controller.py")

    # Core directory
    core_dir = app_dir / "core"
    create_directory(core_dir)
    create_file(core_dir / "__init__.py")
    create_file(core_dir / "config.py")
    create_file(core_dir / "exceptions.py")
    create_file(core_dir / "dependencies.py")

    # DB directory
    db_dir = app_dir / "db"
    create_directory(db_dir)
    create_file(db_dir / "__init__.py")
    create_file(db_dir / "mongodb.py")
    create_file(db_dir / "vector_store.py")

    # Models directory
    models_dir = app_dir / "models"
    create_directory(models_dir)
    create_file(models_dir / "__init__.py")
    create_file(models_dir / "document.py")

    # Schemas directory
    schemas_dir = app_dir / "schemas"
    create_directory(schemas_dir)
    create_file(schemas_dir / "__init__.py")
    create_file(schemas_dir / "tour.py")
    create_file(schemas_dir / "poi.py")
    create_file(schemas_dir / "story.py")

    # Services directory
    services_dir = app_dir / "services"
    create_directory(services_dir)
    create_file(services_dir / "__init__.py")
    for service in ["rag_service", "llm_service", "data_sync_service", "memory_service", "summary_service", "retrieval_service"]:
        create_file(services_dir / f"{service}.py")

    # Chains directory
    chains_dir = app_dir / "chains"
    create_directory(chains_dir)
    create_file(chains_dir / "__init__.py")
    create_file(chains_dir / "conversation_chain.py")
    create_file(chains_dir / "summary_chain.py")
    create_file(chains_dir / "rag_chain.py")

    # Utils directory
    utils_dir = app_dir / "utils"
    create_directory(utils_dir)
    create_file(utils_dir / "__init__.py")
    create_file(utils_dir / "prefiltering.py")

    # Cross-cutting directory
    cross_cutting_dir = root / "cross_cutting"
    create_directory(cross_cutting_dir)
    create_file(cross_cutting_dir / "__init__.py")

    for subdir in ["observability", "security", "caching", "resilience", "compression"]:
        subdir_path = cross_cutting_dir / subdir
        create_directory(subdir_path)
        create_file(subdir_path / "__init__.py")

    # Create specific files in cross-cutting subdirectories
    create_file(cross_cutting_dir / "observability" / "logging.py")
    create_file(cross_cutting_dir / "observability" / "tracing.py")
    create_file(cross_cutting_dir / "observability" / "metrics.py")
    create_file(cross_cutting_dir / "security" / "authentication.py")
    create_file(cross_cutting_dir / "security" / "authorization.py")
    create_file(cross_cutting_dir / "caching" / "redis_cache.py")
    create_file(cross_cutting_dir / "resilience" / "circuit_breaker.py")
    create_file(cross_cutting_dir / "resilience" / "rate_limiter.py")
    create_file(cross_cutting_dir / "compression" / "llm_lingua.py")

    # Tests directory
    tests_dir = root / "tests"
    create_directory(tests_dir)
    create_file(tests_dir / "__init__.py")
    for test_type in ["unit", "integration", "e2e"]:
        create_directory(tests_dir / test_type)

    # Scripts directory
    scripts_dir = root / "scripts"
    create_directory(scripts_dir)
    create_file(scripts_dir / "data_ingestion.py")
    create_file(scripts_dir / "index_creation.py")

    # Monitoring directory
    monitoring_dir = root / "monitoring"
    create_directory(monitoring_dir)
    create_directory(monitoring_dir / "prometheus")
    create_file(monitoring_dir / "prometheus" / "prometheus.yml")
    create_directory(monitoring_dir / "grafana" / "dashboards")
    create_directory(monitoring_dir / "jaeger")
    create_file(monitoring_dir / "jaeger" / "jaeger.yml")

    # Docs directory
    docs_dir = root / "docs"
    create_directory(docs_dir)
    create_file(docs_dir / "api.md")
    create_file(docs_dir / "architecture.md")
    create_file(docs_dir / "cross_cutting_concerns.md")

    # Deployment directory
    deployment_dir = root / "deployment"
    create_directory(deployment_dir)
    create_file(deployment_dir / "Dockerfile")
    create_file(deployment_dir / "docker-compose.yml")
    create_directory(deployment_dir / "kubernetes")
    create_file(deployment_dir / "kubernetes" / "deployment.yaml")
    create_file(deployment_dir / "kubernetes" / "service.yaml")

    # GitHub workflows
    github_dir = root / ".github" / "workflows"
    create_directory(github_dir)
    create_file(github_dir / "ci.yml")
    create_file(github_dir / "cd.yml")

    # Root level files
    create_file(root / "requirements.txt")
    create_file(root / "requirements-dev.txt")
    create_file(root / ".env.example")
    # create_file(root / ".gitignore")
    # create_file(root / "README.md")
    create_file(root / "pyproject.toml")

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully!")