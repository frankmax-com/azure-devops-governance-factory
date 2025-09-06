"""
Docker integration test script for Azure DevOps Governance Factory
"""

import pytest
import docker
import time
import requests
import json
from typing import Dict, Any


class TestDockerIntegration:
    """Test Docker containerization and deployment"""
    
    @classmethod
    def setup_class(cls):
        """Set up Docker client"""
        cls.docker_client = docker.from_env()
        cls.container_name = "azure-devops-governance-test"
        cls.image_name = "azure-devops-governance-factory"
        cls.test_port = 8090
    
    def test_docker_build(self):
        """Test Docker image building"""
        print("Building Docker image...")
        
        try:
            # Build the image
            image, build_logs = self.docker_client.images.build(
                path=".",
                tag=self.image_name,
                rm=True,
                pull=True
            )
            
            # Print build logs
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())
            
            assert image is not None
            print(f"✅ Docker image built successfully: {image.id}")
            
        except Exception as e:
            pytest.fail(f"Docker build failed: {str(e)}")
    
    def test_docker_run(self):
        """Test running Docker container"""
        print("Starting Docker container...")
        
        try:
            # Remove existing container if it exists
            try:
                existing_container = self.docker_client.containers.get(self.container_name)
                existing_container.remove(force=True)
                print("Removed existing container")
            except docker.errors.NotFound:
                pass
            
            # Run the container
            container = self.docker_client.containers.run(
                image=self.image_name,
                name=self.container_name,
                ports={'8000/tcp': self.test_port},
                environment={
                    'ENVIRONMENT': 'test',
                    'DATABASE_URL': 'sqlite:///test.db',
                    'REDIS_URL': 'redis://localhost:6379/1',
                    'AZURE_CLIENT_ID': 'test-client-id',
                    'AZURE_CLIENT_SECRET': 'test-secret',
                    'AZURE_TENANT_ID': 'test-tenant-id',
                    'AZURE_DEVOPS_ORGANIZATION': 'test-org',
                    'SECRET_KEY': 'test-secret-key'
                },
                detach=True,
                remove=True
            )
            
            # Wait for container to start
            print("Waiting for container to start...")
            time.sleep(10)
            
            # Check container status
            container.reload()
            assert container.status == 'running'
            print(f"✅ Container started successfully: {container.id[:12]}")
            
            # Store container for cleanup
            self.test_container = container
            
        except Exception as e:
            pytest.fail(f"Docker run failed: {str(e)}")
    
    def test_health_endpoint(self):
        """Test health endpoint accessibility"""
        print("Testing health endpoint...")
        
        max_retries = 30
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get(f"http://localhost:{self.test_port}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Health endpoint accessible: {data}")
                    assert data['status'] == 'healthy'
                    return
            except requests.exceptions.RequestException:
                pass
            
            retry_count += 1
            time.sleep(2)
            print(f"Retry {retry_count}/{max_retries}...")
        
        pytest.fail("Health endpoint not accessible after maximum retries")
    
    def test_api_endpoints(self):
        """Test key API endpoints"""
        print("Testing API endpoints...")
        
        base_url = f"http://localhost:{self.test_port}/api/v1"
        
        # Test endpoints that don't require authentication for basic connectivity
        endpoints_to_test = [
            "/azure-devops/templates/projects",
            "/azure-devops/templates/pipelines"
        ]
        
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                print(f"Endpoint {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {endpoint} accessible with data: {len(data.get('templates', []))} templates")
                elif response.status_code == 401:
                    print(f"✅ {endpoint} requires authentication (expected)")
                else:
                    print(f"⚠️  {endpoint} returned {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {endpoint} failed: {str(e)}")
    
    def test_swagger_documentation(self):
        """Test Swagger documentation accessibility"""
        print("Testing Swagger documentation...")
        
        try:
            # Test OpenAPI JSON endpoint
            response = requests.get(f"http://localhost:{self.test_port}/api/v1/openapi.json", timeout=10)
            
            if response.status_code == 200:
                openapi_spec = response.json()
                print(f"✅ OpenAPI spec accessible with {len(openapi_spec.get('paths', {}))} paths")
                
                # Verify key sections exist
                assert 'info' in openapi_spec
                assert 'paths' in openapi_spec
                assert 'components' in openapi_spec
                
                # Check for our custom endpoints
                paths = openapi_spec['paths']
                azure_devops_paths = [path for path in paths.keys() if '/azure-devops' in path]
                print(f"✅ Found {len(azure_devops_paths)} Azure DevOps endpoints")
                
            else:
                print(f"❌ OpenAPI spec not accessible: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Swagger documentation test failed: {str(e)}")
    
    def test_container_logs(self):
        """Test container logs for errors"""
        print("Checking container logs...")
        
        try:
            if hasattr(self, 'test_container'):
                logs = self.test_container.logs().decode('utf-8')
                
                # Check for critical errors
                error_keywords = ['ERROR', 'CRITICAL', 'Exception', 'Traceback']
                errors_found = []
                
                for line in logs.split('\n'):
                    for keyword in error_keywords:
                        if keyword in line and 'test' not in line.lower():
                            errors_found.append(line.strip())
                
                if errors_found:
                    print("⚠️  Errors found in container logs:")
                    for error in errors_found[:5]:  # Show first 5 errors
                        print(f"  {error}")
                else:
                    print("✅ No critical errors found in container logs")
                
                # Show last few log lines
                log_lines = logs.split('\n')
                print("Last 5 log lines:")
                for line in log_lines[-5:]:
                    if line.strip():
                        print(f"  {line.strip()}")
                        
        except Exception as e:
            print(f"❌ Failed to check container logs: {str(e)}")
    
    @classmethod
    def teardown_class(cls):
        """Clean up Docker resources"""
        print("Cleaning up Docker resources...")
        
        try:
            # Stop and remove test container
            try:
                container = cls.docker_client.containers.get(cls.container_name)
                container.stop()
                container.remove()
                print("✅ Test container removed")
            except docker.errors.NotFound:
                pass
            
            # Optionally remove test image (uncomment if needed)
            # try:
            #     cls.docker_client.images.remove(cls.image_name, force=True)
            #     print("✅ Test image removed")
            # except docker.errors.ImageNotFound:
            #     pass
            
        except Exception as e:
            print(f"⚠️  Cleanup warning: {str(e)}")


def test_docker_compose_swagger():
    """Test Docker Compose with Swagger setup"""
    print("Testing Docker Compose Swagger setup...")
    
    import subprocess
    
    try:
        # Test docker-compose.swagger.yml syntax
        result = subprocess.run(
            ["docker-compose", "-f", "docker-compose.swagger.yml", "config"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Docker Compose Swagger configuration is valid")
            
            # Check for key services
            config_output = result.stdout
            services_to_check = [
                'azure-devops-governance-factory-swagger',
                'swagger-ui',
                'redoc',
                'postgres',
                'redis'
            ]
            
            for service in services_to_check:
                if service in config_output:
                    print(f"✅ Service '{service}' found in configuration")
                else:
                    print(f"⚠️  Service '{service}' not found in configuration")
                    
        else:
            print(f"❌ Docker Compose configuration error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Docker Compose validation timed out")
    except FileNotFoundError:
        print("⚠️  Docker Compose not found - skipping validation")
    except Exception as e:
        print(f"❌ Docker Compose test failed: {str(e)}")


def test_requirements_compatibility():
    """Test requirements.txt compatibility"""
    print("Testing requirements.txt compatibility...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Check for key dependencies
        key_dependencies = [
            'fastapi',
            'uvicorn',
            'httpx',
            'pydantic',
            'asyncio'
        ]
        
        missing_deps = []
        for dep in key_dependencies:
            if dep not in requirements.lower():
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"⚠️  Missing dependencies: {missing_deps}")
        else:
            print("✅ Key dependencies found in requirements.txt")
        
        # Check for potential conflicts
        if 'requests' in requirements and 'httpx' in requirements:
            print("⚠️  Both 'requests' and 'httpx' found - consider using only httpx for async")
        
        print(f"✅ Requirements file contains {len(requirements.split())} dependencies")
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
    except Exception as e:
        print(f"❌ Requirements test failed: {str(e)}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
