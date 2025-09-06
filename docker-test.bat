@echo off
REM Docker Integration Test Script

echo 🐳 Docker Integration Test - Azure DevOps Governance Factory
echo =============================================================

REM Check Docker availability
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not available. Please install Docker first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not available. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose available

REM Clean up any existing containers
echo [INFO] Cleaning up existing containers...
docker-compose down -v >nul 2>&1
docker-compose -f docker-compose.swagger.yml down -v >nul 2>&1

REM Test 1: Build Main Application
echo [TEST 1] Building main application Docker image...
docker build -t azure-devops-governance-factory:test .
if errorlevel 1 (
    echo ❌ Main Docker build failed
    pause
    exit /b 1
) else (
    echo ✅ Main Docker image built successfully
)

REM Test 2: Build Swagger Documentation Image
echo [TEST 2] Building Swagger documentation Docker image...
docker build -f Dockerfile.swagger -t azure-devops-governance-factory:swagger-test .
if errorlevel 1 (
    echo ❌ Swagger Docker build failed
    pause
    exit /b 1
) else (
    echo ✅ Swagger Docker image built successfully
)

REM Test 3: Start Database Services
echo [TEST 3] Starting database services...
docker-compose up -d postgres redis
if errorlevel 1 (
    echo ❌ Database services failed to start
    pause
    exit /b 1
) else (
    echo ✅ Database services started
    
    REM Wait for services to be ready
    echo [INFO] Waiting for database services to be ready...
    timeout /t 15 /nobreak >nul
)

REM Test 4: Check Database Connectivity
echo [TEST 4] Testing database connectivity...

REM Test PostgreSQL
docker exec azure-devops-governance-factory_postgres_1 pg_isready >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL not ready
) else (
    echo ✅ PostgreSQL ready
)

REM Test Redis
docker exec azure-devops-governance-factory_redis_1 redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ❌ Redis not ready
) else (
    echo ✅ Redis ready
)

REM Test 5: Start Main Application
echo [TEST 5] Starting main application...
docker-compose up -d app
if errorlevel 1 (
    echo ❌ Main application failed to start
    docker-compose logs app
    pause
    exit /b 1
) else (
    echo ✅ Main application started
    
    REM Wait for application to be ready
    echo [INFO] Waiting for application to be ready...
    timeout /t 20 /nobreak >nul
)

REM Test 6: Health Check
echo [TEST 6] Testing application health...
set /a retry=0
:health_check
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    set /a retry+=1
    if %retry% lss 5 (
        echo [INFO] Health check failed, retrying... (%retry%/5)
        timeout /t 5 /nobreak >nul
        goto health_check
    ) else (
        echo ❌ Application health check failed after 5 retries
        echo [DEBUG] Application logs:
        docker-compose logs --tail=20 app
    )
) else (
    echo ✅ Application health check passed
)

REM Test 7: API Endpoints
echo [TEST 7] Testing API endpoints...

curl -f http://localhost:8000/api/v1/azure-devops/templates/projects >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Project templates endpoint (may require auth)
) else (
    echo ✅ Project templates endpoint accessible
)

curl -f http://localhost:8000/api/v1/openapi.json >nul 2>&1
if errorlevel 1 (
    echo ❌ OpenAPI schema endpoint failed
) else (
    echo ✅ OpenAPI schema endpoint accessible
)

REM Test 8: Swagger Documentation Services
echo [TEST 8] Testing Swagger documentation services...
docker-compose -f docker-compose.swagger.yml up -d swagger-ui redoc
if errorlevel 1 (
    echo ❌ Swagger services failed to start
) else (
    echo ✅ Swagger services started
    
    REM Wait for Swagger services
    timeout /t 10 /nobreak >nul
    
    REM Test Swagger UI
    curl -f http://localhost:8081 >nul 2>&1
    if errorlevel 1 (
        echo ❌ Swagger UI not accessible
    ) else (
        echo ✅ Swagger UI accessible at http://localhost:8081
    )
    
    REM Test ReDoc
    curl -f http://localhost:8082 >nul 2>&1
    if errorlevel 1 (
        echo ❌ ReDoc not accessible
    ) else (
        echo ✅ ReDoc accessible at http://localhost:8082
    )
)

REM Test 9: Container Resource Usage
echo [TEST 9] Checking container resource usage...
echo [INFO] Container statistics:
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

REM Test 10: Log Collection
echo [TEST 10] Collecting container logs...
echo [INFO] Saving logs to docker-test-logs.txt
docker-compose logs > docker-test-logs.txt 2>&1
echo ✅ Logs saved to docker-test-logs.txt

REM Summary
echo.
echo 📊 Docker Integration Test Summary
echo ==================================

echo [INFO] Running containers:
docker-compose ps

echo.
echo [INFO] Service URLs:
echo   🌐 Main API: http://localhost:8000
echo   📖 API Docs: http://localhost:8000/api/v1/docs
echo   🔍 Health: http://localhost:8000/health
echo   📖 Swagger UI: http://localhost:8081
echo   📚 ReDoc: http://localhost:8082

echo.
echo [INFO] To stop all services:
echo   docker-compose down
echo   docker-compose -f docker-compose.swagger.yml down

echo.
echo [INFO] To view live logs:
echo   docker-compose logs -f

echo.
echo ✅ Docker integration test completed!
echo    Check docker-test-logs.txt for detailed logs

REM Option to clean up
echo.
set /p cleanup="Clean up containers now? (y/N): "
if /i "%cleanup%"=="y" (
    echo [INFO] Cleaning up containers...
    docker-compose down -v
    docker-compose -f docker-compose.swagger.yml down -v
    
    REM Clean up test images
    docker rmi azure-devops-governance-factory:test >nul 2>&1
    docker rmi azure-devops-governance-factory:swagger-test >nul 2>&1
    
    echo ✅ Cleanup completed
) else (
    echo [INFO] Containers left running. Use 'docker-compose down' to stop them.
)

pause
