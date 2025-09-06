"""
Monitoring and metrics configuration
"""

import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response
import structlog

logger = structlog.get_logger(__name__)

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')
GOVERNANCE_CHECKS = Counter('governance_checks_total', 'Total governance checks', ['policy', 'result'])
COMPLIANCE_VALIDATIONS = Counter('compliance_validations_total', 'Total compliance validations', ['framework', 'result'])


def setup_monitoring(app: FastAPI):
    """Setup monitoring and metrics collection"""
    
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        """Collect metrics for requests"""
        start_time = time.time()
        
        response = await call_next(request)
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.observe(time.time() - start_time)
        
        return response
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(generate_latest(), media_type="text/plain")
    
    logger.info("Monitoring configured successfully")
