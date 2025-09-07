"""
Azure DevOps Routes Package
"""

# Try to import the azure devops wrapper routes
try:
    from .azure_devops_enhanced import router as azure_devops_enhanced_router
    from .azure_devops_wrapper_direct import router as azure_devops_wrapper_direct_router
    routes_available = True
    print("✅ Azure DevOps wrapper routes successfully imported")
except ImportError as e:
    print(f"❌ Azure DevOps wrapper routes import failed: {e}")
    routes_available = False
    azure_devops_enhanced_router = None
    azure_devops_wrapper_direct_router = None

__all__ = [
    "azure_devops_enhanced_router",
    "azure_devops_wrapper_direct_router",
    "routes_available"
]
