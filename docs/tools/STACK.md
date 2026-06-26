# Stack de Herramientas — Capillas de la Fe

## Testing

| Herramienta | Propósito | Comando |
|-------------|-----------|---------|
| [pytest](https://docs.pytest.org) | Framework de tests | `pytest` |
| [httpx](https://www.python-httpx.org) | Cliente HTTP async para tests de API | Usado con pytest |
| [pytest-cov](https://pytest-cov.readthedocs.io) | Cobertura de código | `pytest --cov=app` |
| [pytest-asyncio](https://pytest-asyncio.readthedocs.io) | Tests async | `pytest -k async` |
| [pytest-xdist](https://pytest-xdist.readthedocs.io) | Tests paralelos | `pytest -n auto` |
| [Locust](https://locust.io) | Tests de carga | `locust -f locustfile.py` |
| [schemathesis](https://schemathesis.readthedocs.io) | Testing de APIs basado en OpenAPI | `schemathesis run` |

### Instalación

```bash
pip install pytest httpx pytest-cov pytest-asyncio pytest-xdist locust schemathesis
```

### Configuración (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["app"]
branch = true
```

## Calidad de Código

| Herramienta | Propósito | Comando |
|-------------|-----------|---------|
| [ruff](https://docs.astral.sh/ruff) | Linter + formatter (ultrarrápido) | `ruff check . && ruff format .` |
| [mypy](https://mypy-lang.org) | Type checking estático | `mypy app/` |
| [bandit](https://bandit.readthedocs.io) | Seguridad en código Python | `bandit -r app/` |
| [Semgrep](https://semgrep.dev) | SAST (análisis estático) | `semgrep --config=auto` |
| [CodeQL](https://codeql.github.com) | Análisis de seguridad (CI) | GitHub Action |

### Instalación

```bash
pip install ruff mypy bandit semgrep
```

### Configuración (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "ARG", "C4", "T10"]

[tool.mypy]
strict = true
python_version = "3.12"
warn_unused_configs = true
```

## Monitoreo y Observabilidad

| Herramienta | Propósito | Costo |
|-------------|-----------|-------|
| [Prometheus](https://prometheus.io) | Métricas y alertas | Gratuito (self-hosted) |
| [Grafana](https://grafana.com) | Dashboards de métricas | Gratuito (self-hosted) |
| [Loki](https://grafana.com/oss/loki) | Agregación de logs | Gratuito (self-hosted) |
| [Tempo](https://grafana.com/oss/tempo) | Trazabilidad distribuida | Gratuito (self-hosted) |
| [Sentry](https://sentry.io) | Error tracking | Gratuito (5K eventos/mes) |
| [Uptime Kuma](https://uptime.kuma.pet) | Monitoreo de uptime | Gratuito (self-hosted) |

## Documentación

| Herramienta | Propósito | Estado |
|-------------|-----------|--------|
| [Marp](https://marp.app) | Presentaciones técnicas | En uso |
| [Notion](https://notion.so) | Documentación interna | Actual |
| [Docusaurus](https://docusaurus.io) | Documentación pública | Futuro |

## CI/CD

| Herramienta | Propósito |
|-------------|-----------|
| GitHub Actions | Pipeline CI/CD |
| Docker / ECR | Container registry |
| ECS Fargate | Orquestación serverless |

## Scripts útiles

```bash
# Test + calidad completo
pytest --cov=app --cov-report=term-missing && ruff check . && mypy app/ && bandit -r app/

# Tests en paralelo
pytest -n auto

# Tests de carga
locust -f tests/locustfile.py --host=https://api.example.com

# Lint + auto-fix
ruff check --fix .

# Formatear
ruff format .
```
