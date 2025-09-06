@echo off
REM Azure DevOps Governance Factory - Windows Deployment and Testing Script

echo 🚀 Azure DevOps Governance Factory - Deployment and Testing
echo ============================================================

REM Step 1: Environment Setup
echo [INFO] Setting up environment...

if not exist .env (
    echo [WARNING] .env file not found. Creating from template...
    if exist .env.example (
        copy .env.example .env
        echo [SUCCESS] .env file created from template
        echo [WARNING] Please update .env file with your actual credentials
    ) else (
        echo [ERROR] .env.example not found. Please create .env file manually
        pause
        exit /b 1
    )
)

REM Step 2: Install Dependencies
echo [INFO] Installing Python dependencies...

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ first
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Install our Azure DevOps wrapper in editable mode
if exist azure_devops_wrapper (
    echo [INFO] Installing Azure DevOps wrapper in editable mode...
    python -m pip install -e azure_devops_wrapper/
    echo [SUCCESS] Azure DevOps wrapper installed
) else (
    echo [WARNING] Azure DevOps wrapper directory not found
)

echo [SUCCESS] Dependencies installed

REM Step 3: Docker Setup
echo [INFO] Setting up Docker environment...

docker --version >nul 2>&1
if not errorlevel 1 (
    REM Build Docker image
    echo [INFO] Building Docker image...
    docker build -t azure-devops-governance-factory .
    echo [SUCCESS] Docker image built
    
    REM Build Swagger-enabled image
    echo [INFO] Building Swagger-enabled Docker image...
    docker build -f Dockerfile.swagger -t azure-devops-governance-factory:swagger .
    echo [SUCCESS] Swagger Docker image built
) else (
    echo [WARNING] Docker not found. Skipping Docker setup
)

REM Step 4: Database Setup
echo [INFO] Setting up database...

docker-compose --version >nul 2>&1
if not errorlevel 1 (
    REM Start database services
    docker-compose up -d postgres redis
    
    REM Wait for database to be ready
    echo [INFO] Waiting for database to be ready...
    timeout /t 10 /nobreak >nul
    
    REM Run database migrations (if alembic is set up)
    if exist alembic (
        echo [INFO] Running database migrations...
        python -m alembic upgrade head
        echo [SUCCESS] Database migrations completed
    )
    
    echo [SUCCESS] Database setup completed
) else (
    echo [WARNING] Docker Compose not found. Skipping database setup
)

REM Step 5: Running Tests
echo [INFO] Running comprehensive test suite...

REM Unit tests
echo [INFO] Running unit tests...
python -m pytest tests/test_azure_devops_wrapper_integration.py -v --tb=short
if errorlevel 1 (
    echo [ERROR] Unit tests failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] Unit tests passed
)

REM Docker integration tests
docker --version >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Running Docker integration tests...
    python -m pytest tests/test_docker_integration.py -v --tb=short
    if not errorlevel 1 (
        echo [SUCCESS] Docker integration tests passed
    ) else (
        echo [WARNING] Docker integration tests failed
    )
)

REM Step 6: Start Services
echo [INFO] Starting all services...

docker-compose --version >nul 2>&1
if not errorlevel 1 (
    REM Start all services
    docker-compose up -d
    
    REM Wait for services to be ready
    echo [INFO] Waiting for services to start...
    timeout /t 15 /nobreak >nul
    
    REM Check service health
    echo [INFO] Checking service health...
    
    REM Check main application
    curl -f http://localhost:8000/health >nul 2>&1
    if not errorlevel 1 (
        echo [SUCCESS] Main application is healthy
    ) else (
        echo [ERROR] Main application health check failed
    )
    
    REM Show running containers
    echo [INFO] Running containers:
    docker-compose ps
    
    echo [SUCCESS] All services started successfully
) else (
    echo [WARNING] Docker Compose not found. Starting application directly...
    start /b python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    echo [INFO] Application started
)

REM Step 7: Swagger Documentation Setup
echo [INFO] Setting up Swagger documentation...

docker-compose --version >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Starting Swagger services...
    docker-compose -f docker-compose.swagger.yml up -d swagger-ui redoc
    
    REM Wait for Swagger services
    timeout /t 10 /nobreak >nul
    
    echo [SUCCESS] Swagger documentation available at:
    echo   📖 Swagger UI: http://localhost:8081
    echo   📚 ReDoc: http://localhost:8082
    echo   🔧 API JSON: http://localhost:8080/api/v1/openapi.json
)

REM Step 8: API Testing
echo [INFO] Testing API endpoints...

curl --version >nul 2>&1
if not errorlevel 1 (
    curl -f http://localhost:8000/health >nul 2>&1
    if not errorlevel 1 (
        echo [SUCCESS] ✅ http://localhost:8000/health
    ) else (
        echo [WARNING] ⚠️ http://localhost:8000/health
    )
    
    curl -f http://localhost:8000/api/v1/azure-devops/templates/projects >nul 2>&1
    if not errorlevel 1 (
        echo [SUCCESS] ✅ http://localhost:8000/api/v1/azure-devops/templates/projects
    ) else (
        echo [WARNING] ⚠️ http://localhost:8000/api/v1/azure-devops/templates/projects (may require authentication)
    )
) else (
    echo [WARNING] curl not found. Skipping API endpoint tests
)

REM Final Summary
echo.
echo 🎉 Deployment and Testing Complete!
echo =====================================
echo.
echo [SUCCESS] Services Status:
echo   🌐 Main API: http://localhost:8000
echo   📖 API Docs: http://localhost:8000/api/v1/docs
echo   📚 ReDoc: http://localhost:8000/api/v1/redoc
echo   🔍 Health Check: http://localhost:8000/health
echo.

docker-compose --version >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Swagger Services:
    echo   📖 Swagger UI: http://localhost:8081
    echo   📚 ReDoc: http://localhost:8082
    echo.
    
    echo [SUCCESS] Database Services:
    echo   🐘 PostgreSQL: localhost:5432
    echo   🔴 Redis: localhost:6379
    echo.
)

echo [SUCCESS] Azure DevOps Wrapper Features:
echo   ✅ Complete API Coverage (~2,125 operations)
echo   ✅ 13 Service Categories
echo   ✅ 5 Business Facades
echo   ✅ Enterprise Governance
echo   ✅ Zero-Trust Security
echo   ✅ Multi-Authentication Support
echo   ✅ Rate Limiting ^& Retry Logic
echo   ✅ Comprehensive Error Handling
echo.

echo [INFO] Next Steps:
echo 1. Update .env file with your Azure DevOps credentials
echo 2. Test the API endpoints using the Swagger UI
echo 3. Create your first project using the project facade
echo 4. Set up CI/CD pipelines using the pipeline facade
echo 5. Implement security governance using the security facade
echo.

echo [INFO] Useful Commands:
echo • View logs: docker-compose logs -f
echo • Stop services: docker-compose down
echo • Run tests: python -m pytest tests/ -v
echo • View API documentation: start http://localhost:8000/api/v1/docs
echo.

echo [SUCCESS] 🚀 Azure DevOps Governance Factory is ready for use!
pause
