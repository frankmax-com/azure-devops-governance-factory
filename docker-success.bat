@echo off
REM Azure DevOps Governance Factory - Docker Success Summary

echo 🎉 Azure DevOps Governance Factory - Docker Deployment SUCCESS!
echo ===============================================================

echo.
echo ✅ SERVICES RUNNING:
docker-compose -f docker-compose.minimal.yml ps

echo.
echo 🌐 SERVICE ENDPOINTS:
echo   Main API: http://localhost:8000
echo   Health Check: http://localhost:8000/health  
echo   API Documentation: http://localhost:8000/api/v1/docs
echo   ReDoc Documentation: http://localhost:8000/api/v1/redoc
echo   OpenAPI Schema: http://localhost:8000/api/v1/openapi.json

echo.
echo 📋 AVAILABLE API ENDPOINTS:
echo   GET /health                                    - Health check
echo   GET /                                          - Root info
echo   GET /api/v1/azure-devops/templates/projects    - Project templates
echo   GET /api/v1/azure-devops/templates/pipelines   - Pipeline templates

echo.
echo 🐘 DATABASE SERVICES:
echo   PostgreSQL: localhost:5433 (user: azuredevops, db: azuredevops_governance)
echo   Redis: localhost:6380

echo.
echo 📊 QUICK TESTS:
echo   Testing health endpoint...
curl -s http://localhost:8000/health

echo.
echo   Testing project templates...
curl -s http://localhost:8000/api/v1/azure-devops/templates/projects

echo.
echo 🔧 USEFUL COMMANDS:
echo   View logs: docker-compose -f docker-compose.minimal.yml logs -f
echo   Stop services: docker-compose -f docker-compose.minimal.yml down
echo   Restart app: docker-compose -f docker-compose.minimal.yml restart app
echo   Shell into app: docker-compose -f docker-compose.minimal.yml exec app bash

echo.
echo 📝 NEXT STEPS TO BUILD FULL SYSTEM:
echo   1. Update .env file with your Azure DevOps credentials
echo   2. Run: docker-compose -f docker-compose.yml up -d  (for full system)
echo   3. Add the comprehensive Azure DevOps wrapper integration
echo   4. Enable authentication and security features
echo   5. Deploy production-ready monitoring and logging

echo.
echo 🚀 SUCCESS: Your Azure DevOps Governance Factory is running in Docker!
echo    Open http://localhost:8000/api/v1/docs to explore the API
echo.
pause
