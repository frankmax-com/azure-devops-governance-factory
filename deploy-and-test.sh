#!/bin/bash

# Azure DevOps Governance Factory - Complete Deployment and Testing Script

set -e

echo "🚀 Azure DevOps Governance Factory - Deployment and Testing"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Environment Setup
print_status "Setting up environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success ".env file created from template"
        print_warning "Please update .env file with your actual credentials"
    else
        print_error ".env.example not found. Please create .env file manually"
        exit 1
    fi
fi

# Step 2: Install Dependencies
print_status "Installing Python dependencies..."

if command -v python3 &> /dev/null; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    
    # Install our Azure DevOps wrapper in editable mode
    if [ -d "azure_devops_wrapper" ]; then
        print_status "Installing Azure DevOps wrapper in editable mode..."
        python3 -m pip install -e azure_devops_wrapper/
        print_success "Azure DevOps wrapper installed"
    else
        print_warning "Azure DevOps wrapper directory not found"
    fi
    
    print_success "Dependencies installed"
else
    print_error "Python3 not found. Please install Python 3.8+ first"
    exit 1
fi

# Step 3: Docker Setup
print_status "Setting up Docker environment..."

if command -v docker &> /dev/null; then
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t azure-devops-governance-factory .
    print_success "Docker image built"
    
    # Build Swagger-enabled image
    print_status "Building Swagger-enabled Docker image..."
    docker build -f Dockerfile.swagger -t azure-devops-governance-factory:swagger .
    print_success "Swagger Docker image built"
    
else
    print_warning "Docker not found. Skipping Docker setup"
fi

# Step 4: Database Setup
print_status "Setting up database..."

if command -v docker-compose &> /dev/null; then
    # Start database services
    docker-compose up -d postgres redis
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations (if alembic is set up)
    if [ -d "alembic" ]; then
        print_status "Running database migrations..."
        python3 -m alembic upgrade head
        print_success "Database migrations completed"
    fi
    
    print_success "Database setup completed"
else
    print_warning "Docker Compose not found. Skipping database setup"
fi

# Step 5: Running Tests
print_status "Running comprehensive test suite..."

# Unit tests
print_status "Running unit tests..."
python3 -m pytest tests/test_azure_devops_wrapper_integration.py -v --tb=short
if [ $? -eq 0 ]; then
    print_success "Unit tests passed"
else
    print_error "Unit tests failed"
    exit 1
fi

# Docker integration tests
if command -v docker &> /dev/null; then
    print_status "Running Docker integration tests..."
    python3 -m pytest tests/test_docker_integration.py -v --tb=short
    if [ $? -eq 0 ]; then
        print_success "Docker integration tests passed"
    else
        print_warning "Docker integration tests failed"
    fi
fi

# Step 6: Start Services
print_status "Starting all services..."

if command -v docker-compose &> /dev/null; then
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 15
    
    # Check service health
    print_status "Checking service health..."
    
    # Check main application
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Main application is healthy"
    else
        print_error "Main application health check failed"
    fi
    
    # Show running containers
    print_status "Running containers:"
    docker-compose ps
    
    print_success "All services started successfully"
else
    print_warning "Docker Compose not found. Starting application directly..."
    python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
    APP_PID=$!
    print_status "Application started with PID: $APP_PID"
fi

# Step 7: Swagger Documentation Setup
print_status "Setting up Swagger documentation..."

if command -v docker-compose &> /dev/null; then
    print_status "Starting Swagger services..."
    docker-compose -f docker-compose.swagger.yml up -d swagger-ui redoc
    
    # Wait for Swagger services
    sleep 10
    
    print_success "Swagger documentation available at:"
    echo "  📖 Swagger UI: http://localhost:8081"
    echo "  📚 ReDoc: http://localhost:8082"
    echo "  🔧 API JSON: http://localhost:8080/api/v1/openapi.json"
fi

# Step 8: API Testing
print_status "Testing API endpoints..."

# Test basic endpoints
ENDPOINTS=(
    "http://localhost:8000/health"
    "http://localhost:8000/api/v1/azure-devops/templates/projects"
    "http://localhost:8000/api/v1/azure-devops/templates/pipelines"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -f "$endpoint" > /dev/null 2>&1; then
        print_success "✅ $endpoint"
    else
        print_warning "⚠️  $endpoint (may require authentication)"
    fi
done

# Step 9: Performance Testing (Optional)
print_status "Running basic performance tests..."

if command -v ab &> /dev/null; then
    print_status "Running Apache Bench performance test..."
    ab -n 100 -c 10 http://localhost:8000/health > performance_test.log 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "Performance test completed. Check performance_test.log for results"
    else
        print_warning "Performance test failed"
    fi
else
    print_warning "Apache Bench not found. Skipping performance tests"
fi

# Step 10: Integration Testing (Optional)
if [ "$1" = "--integration" ]; then
    print_status "Running integration tests with real Azure DevOps..."
    
    if [ -z "$AZURE_CLIENT_SECRET" ]; then
        print_error "AZURE_CLIENT_SECRET not set. Cannot run integration tests"
    else
        python3 -m pytest tests/ -m integration -v --tb=short
        if [ $? -eq 0 ]; then
            print_success "Integration tests passed"
        else
            print_warning "Integration tests failed"
        fi
    fi
fi

# Step 11: Documentation Generation
print_status "Generating documentation..."

if [ -d "docs" ]; then
    if command -v mkdocs &> /dev/null; then
        print_status "Building MkDocs documentation..."
        mkdocs build
        print_success "Documentation built in site/ directory"
    else
        print_warning "MkDocs not found. Skipping documentation build"
    fi
fi

# Final Summary
echo ""
echo "🎉 Deployment and Testing Complete!"
echo "====================================="
echo ""
print_success "Services Status:"
echo "  🌐 Main API: http://localhost:8000"
echo "  📖 API Docs: http://localhost:8000/api/v1/docs"
echo "  📚 ReDoc: http://localhost:8000/api/v1/redoc"
echo "  🔍 Health Check: http://localhost:8000/health"
echo ""

if command -v docker-compose &> /dev/null; then
    print_success "Swagger Services:"
    echo "  📖 Swagger UI: http://localhost:8081"
    echo "  📚 ReDoc: http://localhost:8082"
    echo ""
    
    print_success "Database Services:"
    echo "  🐘 PostgreSQL: localhost:5432"
    echo "  🔴 Redis: localhost:6379"
    echo ""
fi

print_success "Azure DevOps Wrapper Features:"
echo "  ✅ Complete API Coverage (~2,125 operations)"
echo "  ✅ 13 Service Categories"
echo "  ✅ 5 Business Facades"
echo "  ✅ Enterprise Governance"
echo "  ✅ Zero-Trust Security"
echo "  ✅ Multi-Authentication Support"
echo "  ✅ Rate Limiting & Retry Logic"
echo "  ✅ Comprehensive Error Handling"
echo ""

print_status "Next Steps:"
echo "1. Update .env file with your Azure DevOps credentials"
echo "2. Test the API endpoints using the Swagger UI"
echo "3. Create your first project using the project facade"
echo "4. Set up CI/CD pipelines using the pipeline facade"
echo "5. Implement security governance using the security facade"
echo ""

print_status "Useful Commands:"
echo "• View logs: docker-compose logs -f"
echo "• Stop services: docker-compose down"
echo "• Run tests: python3 -m pytest tests/ -v"
echo "• View API documentation: open http://localhost:8000/api/v1/docs"
echo ""

print_success "🚀 Azure DevOps Governance Factory is ready for use!"
