@echo off
REM Quick Test Script for Azure DevOps Governance Factory

echo 🧪 Quick Test - Azure DevOps Governance Factory
echo ================================================

REM Test 1: Python Dependencies
echo [TEST 1] Checking Python dependencies...
python -c "import fastapi, azure.devops, redis, sqlalchemy, pytest; print('✅ Core dependencies available')" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies. Run: pip install -r requirements.txt
    exit /b 1
) else (
    echo ✅ Python dependencies OK
)

REM Test 2: Environment Configuration
echo [TEST 2] Checking environment configuration...
if exist .env (
    echo ✅ .env file exists
) else (
    echo ⚠️ .env file missing. Creating from template...
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env created from template
    ) else (
        echo ❌ No .env.example found
    )
)

REM Test 3: Docker Availability
echo [TEST 3] Checking Docker availability...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Docker not available
) else (
    echo ✅ Docker available
    
    REM Test Docker Compose
    docker-compose --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ Docker Compose not available
    ) else (
        echo ✅ Docker Compose available
    )
)

REM Test 4: Run Basic Unit Tests
echo [TEST 4] Running basic unit tests...
python -m pytest tests/test_azure_devops_wrapper_integration.py::test_wrapper_service_initialization -v --tb=short >nul 2>&1
if errorlevel 1 (
    echo ❌ Basic unit tests failed
    python -m pytest tests/test_azure_devops_wrapper_integration.py::test_wrapper_service_initialization -v --tb=short
) else (
    echo ✅ Basic unit tests passed
)

REM Test 5: FastAPI Application Import
echo [TEST 5] Testing FastAPI application import...
python -c "from src.main import app; print('✅ FastAPI app imports successfully')" 2>nul
if errorlevel 1 (
    echo ❌ FastAPI app import failed
    python -c "from src.main import app; print('✅ FastAPI app imports successfully')"
) else (
    echo ✅ FastAPI application import OK
)

REM Test 6: Azure DevOps Wrapper Import
echo [TEST 6] Testing Azure DevOps wrapper import...
python -c "from src.services.azure_devops_wrapper_service import AzureDevOpsWrapperService; print('✅ Wrapper service imports successfully')" 2>nul
if errorlevel 1 (
    echo ❌ Wrapper service import failed
    python -c "from src.services.azure_devops_wrapper_service import AzureDevOpsWrapperService; print('✅ Wrapper service imports successfully')"
) else (
    echo ✅ Azure DevOps wrapper import OK
)

REM Test 7: Docker Build Test (Optional)
docker --version >nul 2>&1
if not errorlevel 1 (
    echo [TEST 7] Testing Docker build (this may take a while)...
    
    REM Check if Dockerfile exists
    if exist Dockerfile (
        docker build -t test-azure-devops-governance-factory . >build.log 2>&1
        if errorlevel 1 (
            echo ❌ Docker build failed. Check build.log for details
        ) else (
            echo ✅ Docker build successful
            
            REM Clean up test image
            docker rmi test-azure-devops-governance-factory >nul 2>&1
        )
    ) else (
        echo ⚠️ Dockerfile not found
    )
) else (
    echo [TEST 7] Skipping Docker build test (Docker not available)
)

REM Test 8: Quick API Response Test
echo [TEST 8] Testing API configuration...
python -c "
from src.main import app
from fastapi.testclient import TestClient
client = TestClient(app)
try:
    response = client.get('/health')
    if response.status_code == 200:
        print('✅ Health endpoint responds correctly')
    else:
        print('❌ Health endpoint returned:', response.status_code)
except Exception as e:
    print('❌ API test failed:', str(e))
" 2>nul
if errorlevel 1 (
    echo ❌ API configuration test failed
)

echo.
echo 📊 Quick Test Summary
echo ====================

REM Count passed tests
set /a passed=0
set /a total=8

echo ✅ Tests that should pass:
echo   - Python dependencies
echo   - Environment setup  
echo   - FastAPI application
echo   - Wrapper service import
echo   - API configuration

echo.
echo ⚠️ Optional tests (may be skipped):
echo   - Docker availability
echo   - Docker build
echo   - Full unit test suite

echo.
echo 🚀 If all core tests pass, you can run:
echo   deploy-and-test.bat        - Full deployment
echo   docker-compose up          - Start services
echo   python -m pytest tests/ -v - Run full test suite

echo.
echo 📖 Next steps:
echo 1. Update .env with your Azure DevOps credentials
echo 2. Run full deployment: deploy-and-test.bat
echo 3. Open Swagger UI: http://localhost:8000/docs
echo.
pause
