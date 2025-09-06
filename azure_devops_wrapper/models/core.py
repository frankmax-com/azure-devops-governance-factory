"""
Models for Core Azure DevOps entities (Projects, Teams, Processes, etc.)
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import Field, validator

from .common import (
    AzureDevOpsBaseModel,
    IdentityRef,
    TeamProjectReference,
    ProcessReference,
    ReferenceLinks,
    WebApiTeamRef,
    ID_FIELD,
    NAME_FIELD,
    URL_FIELD,
    CREATED_DATE_FIELD,
    MODIFIED_DATE_FIELD,
    CREATED_BY_FIELD,
    MODIFIED_BY_FIELD
)


class ProjectState(Enum):
    """Project state enumeration."""
    DELETING = "deleting"
    NEW = "new"
    WELL_FORMED = "wellFormed"
    CREATE_PENDING = "createPending"
    CHANGING = "changing"
    DELETE_PENDING = "deletePending"


class ProjectVisibility(Enum):
    """Project visibility enumeration."""
    PRIVATE = "private"
    PUBLIC = "public"


class TeamProject(AzureDevOpsBaseModel):
    """Team project model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    description: Optional[str] = None
    url: Optional[str] = URL_FIELD
    state: Optional[ProjectState] = None
    revision: Optional[int] = None
    visibility: Optional[ProjectVisibility] = None
    last_update_time: Optional[datetime] = Field(None, alias="lastUpdateTime")
    
    # Capabilities
    capabilities: Optional[Dict[str, Any]] = None
    
    # Default team
    default_team: Optional[WebApiTeamRef] = Field(None, alias="defaultTeam")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class TeamProjectCollection(AzureDevOpsBaseModel):
    """Team project collection model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    url: Optional[str] = URL_FIELD
    state: Optional[str] = None


class WebApiTeam(AzureDevOpsBaseModel):
    """Team model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    url: Optional[str] = URL_FIELD
    description: Optional[str] = None
    identity_url: Optional[str] = Field(None, alias="identityUrl")
    project_name: Optional[str] = Field(None, alias="projectName")
    project_id: Optional[str] = Field(None, alias="projectId")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class TeamMember(AzureDevOpsBaseModel):
    """Team member model."""
    
    identity: IdentityRef
    is_team_admin: Optional[bool] = Field(None, alias="isTeamAdmin")


class TeamMembersRef(AzureDevOpsBaseModel):
    """Team members reference."""
    
    members: List[IdentityRef]
    total_count: Optional[int] = Field(None, alias="totalCount")


class Process(AzureDevOpsBaseModel):
    """Process model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    description: Optional[str] = None
    url: Optional[str] = URL_FIELD
    is_default: Optional[bool] = Field(None, alias="isDefault")
    type: Optional[str] = None
    
    # Customization settings
    customization_type: Optional[str] = Field(None, alias="customizationType")
    
    # Parent process (for inherited processes)
    parent_process_type_id: Optional[str] = Field(None, alias="parentProcessTypeId")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class ProcessType(Enum):
    """Process type enumeration."""
    SYSTEM = "system"
    CUSTOM = "custom"
    INHERITED = "inherited"


class ExtensionState(Enum):
    """Extension state enumeration."""
    NONE = "none"
    DISABLED = "disabled"
    ENABLED = "enabled"
    WARNING = "warning"
    ERROR = "error"


class InstalledExtension(AzureDevOpsBaseModel):
    """Installed extension model."""
    
    extension_id: str = Field(alias="extensionId")
    extension_name: str = Field(alias="extensionName")
    publisher_id: str = Field(alias="publisherId")
    publisher_name: str = Field(alias="publisherName")
    version: str
    registration_id: Optional[str] = Field(None, alias="registrationId")
    
    # State and flags
    install_state: Optional[ExtensionState] = Field(None, alias="installState")
    flags: Optional[List[str]] = None
    
    # Installation info
    installed_by: Optional[IdentityRef] = Field(None, alias="installedBy")
    last_published: Optional[datetime] = Field(None, alias="lastPublished")
    
    # Contributions
    contributions: Optional[List[Dict[str, Any]]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class OrganizationInfo(AzureDevOpsBaseModel):
    """Organization information model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    url: Optional[str] = URL_FIELD
    
    # Location and region
    location: Optional[str] = None
    region: Optional[str] = None
    
    # Timestamps
    created_date: Optional[datetime] = CREATED_DATE_FIELD
    last_changed_date: Optional[datetime] = Field(None, alias="lastChangedDate")


class AccountInfo(AzureDevOpsBaseModel):
    """Account information model."""
    
    account_id: str = Field(alias="accountId")
    account_name: str = Field(alias="accountName")
    account_uri: Optional[str] = Field(None, alias="accountUri")
    organization_name: Optional[str] = Field(None, alias="organizationName")
    
    # Properties
    properties: Optional[Dict[str, Any]] = None


class ProjectProperty(AzureDevOpsBaseModel):
    """Project property model."""
    
    name: str = NAME_FIELD
    value: Any


class ProjectProperties(AzureDevOpsBaseModel):
    """Project properties collection."""
    
    count: int
    value: List[ProjectProperty]


# Create operation models
class ProjectCreateRequest(AzureDevOpsBaseModel):
    """Request model for creating a project."""
    
    name: str = NAME_FIELD
    description: Optional[str] = None
    visibility: ProjectVisibility = ProjectVisibility.PRIVATE
    capabilities: Optional[Dict[str, Dict[str, str]]] = None
    
    @validator('capabilities', pre=True, always=True)
    def set_default_capabilities(cls, v):
        if v is None:
            return {
                "versioncontrol": {"sourceControlType": "Git"},
                "processTemplate": {"templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"}  # Basic process
            }
        return v


class TeamCreateRequest(AzureDevOpsBaseModel):
    """Request model for creating a team."""
    
    name: str = NAME_FIELD
    description: Optional[str] = None


class ProjectUpdateRequest(AzureDevOpsBaseModel):
    """Request model for updating a project."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[ProjectVisibility] = None


# Response wrapper models
class ProjectsResponse(AzureDevOpsBaseModel):
    """Response model for projects list."""
    
    count: int
    value: List[TeamProject]


class TeamsResponse(AzureDevOpsBaseModel):
    """Response model for teams list."""
    
    count: int
    value: List[WebApiTeam]


class ProcessesResponse(AzureDevOpsBaseModel):
    """Response model for processes list."""
    
    count: int
    value: List[Process]


class ExtensionsResponse(AzureDevOpsBaseModel):
    """Response model for extensions list."""
    
    count: int
    value: List[InstalledExtension]
