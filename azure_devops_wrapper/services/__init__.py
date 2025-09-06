"""
Service client initialization - imports all service clients.
"""

from .core_service import CoreService
from .git_service import GitService
from .work_items_service import WorkItemsService
from .build_service import BuildService
from .pipelines_service import PipelinesService
from .release_service import ReleaseService
from .test_service import TestService
from .packaging_service import PackagingService

__all__ = [
    "CoreService",
    "GitService", 
    "WorkItemsService",
    "BuildService",
    "PipelinesService",
    "ReleaseService",
    "TestService",
    "PackagingService"
]
