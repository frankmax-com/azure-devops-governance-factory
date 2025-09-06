"""
Azure DevOps Facades - Business Layer Abstractions

This module provides high-level business operation abstractions that combine
multiple Azure DevOps services for common enterprise workflows.
"""

from .project_facade import ProjectFacade
from .pipeline_facade import PipelineFacade
from .security_facade import SecurityFacade
from .integration_facade import IntegrationFacade
from .governance_facade import GovernanceFacade

__all__ = [
    'ProjectFacade',
    'PipelineFacade', 
    'SecurityFacade',
    'IntegrationFacade',
    'GovernanceFacade'
]
