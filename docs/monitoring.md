# Monitoring

The monitoring directory include configurations for Prometheus, Grafana, and Jaeger. These tools will help you monitor the performance, health, and tracing of your RAG-powered microservice.

1. Prometheus configuration:



```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'rag-microservice'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['rag-microservice:8000']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'mongodb'
    static_configs:
      - targets: ['mongodb:27017']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - 'alertmanager:9093'

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

```

2. Grafana Dashboard:



```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "links": [],
  "panels": [
    {
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": null,
      "fieldConfig": {
        "defaults": {},
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.5.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "rate(rag_requests_total[5m])",
          "interval": "",
          "legendFormat": "",
          "refId": "A"
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Request Rate",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": null,
      "fieldConfig": {
        "defaults": {},
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 4,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.5.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(rag_response_time_seconds_bucket[5m]))",
          "interval": "",
          "legendFormat": "",
          "refId": "A"
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "95th Percentile Response Time",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "s",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    }
  ],
  "schemaVersion": 27,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "RAG Microservice Dashboard",
  "uid": "rag-microservice",
  "version": 1
}

```

3. Jaeger Configuration:



```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: rag-jaeger
spec:
  strategy: allInOne
  allInOne:
    image: jaegertracing/all-in-one:1.22
    options:
      log-level: info
  storage:
    type: memory
    options:
      memory:
        max-traces: 100000
  ingress:
    enabled: false
  agent:
    strategy: DaemonSet
  ui:
    options:
      dependencies:
        menuEnabled: false
      tracking:
        gaID: UA-000000-2
  sampling:
    options:
      default_strategy:
        type: probabilistic
        param: 1

```

These implementations provide a comprehensive setup for monitoring your RAG-powered microservice:

1. The Prometheus configuration (prometheus.yml) sets up metric scraping for your microservice and its dependencies.

2. The Grafana dashboard JSON file provides a starting point for visualizing key metrics of your RAG microservice. It includes panels for request rate and 95th percentile response time. You can expand this dashboard with more panels as needed.

3. The Jaeger configuration (jaeger.yml) sets up a basic all-in-one deployment of Jaeger for distributed tracing.

To use these in your project:

1. Place the prometheus.yml file in the monitoring/prometheus directory.
2. Place the rag_microservice_dashboard.json file in the monitoring/grafana/dashboards directory.
3. Place the jaeger.yml file in the monitoring/jaeger directory.

For local development and testing, you might want to add these services to your docker-compose.yml file:

```yaml
services:
  # ... other services ...

  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    volumes:
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin_password
    ports:
      - "3000:3000"

  jaeger:
    image: jaegertracing/all-in-one:1.22
    ports:
      - "16686:16686"
      - "14268:14268"
```

For Kubernetes deployment, you would typically use the Prometheus Operator and Jaeger Operator to manage these services.

Remember to adjust the following:

- In prometheus.yml, ensure the targets match your actual service names and ports.
- In the Grafana dashboard, you may need to adjust queries based on your actual metric names and requirements.
- In jaeger.yml, adjust the configuration based on your specific needs, especially for production environments where you might want to use a persistent storage backend.

These configurations provide a solid starting point for monitoring your RAG microservice, but you may need to adjust them based on your specific requirements, such as adding more detailed metrics, creating alerts, or configuring more complex tracing scenarios.

Would you like me to explain any part of these implementations in more detail or make any adjustments to better fit your specific monitoring needs?