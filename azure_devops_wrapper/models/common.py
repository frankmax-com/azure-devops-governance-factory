"""
Common base models and utilities for Azure DevOps entities
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class AzureDevOpsBaseModel(BaseModel):
    """Base model for all Azure DevOps entities."""
    
    class Config:
        # Allow extra fields for flexibility with API responses
        extra = "allow"
        # Use enum values instead of names
        use_enum_values = True
        # Allow population by field name or alias
        allow_population_by_field_name = True
        # Validate assignment
        validate_assignment = True
        # Custom JSON encoders
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
    
    def dict_exclude_none(self) -> Dict[str, Any]:
        """Return dict representation excluding None values."""
        return self.dict(exclude_none=True)


class IdentityRef(AzureDevOpsBaseModel):
    """Reference to an identity (user, group, service)."""
    
    id: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    unique_name: Optional[str] = Field(None, alias="uniqueName")
    url: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    descriptor: Optional[str] = None
    
    @property
    def name(self) -> str:
        """Get the best available name for this identity."""
        return self.display_name or self.unique_name or self.id or "Unknown"


class WebApiTeamRef(AzureDevOpsBaseModel):
    """Reference to a team."""
    
    id: str
    name: str
    url: Optional[str] = None


class TeamProjectReference(AzureDevOpsBaseModel):
    """Reference to a team project."""
    
    id: str
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    state: Optional[str] = None
    revision: Optional[int] = None
    visibility: Optional[str] = None
    default_team: Optional[WebApiTeamRef] = Field(None, alias="defaultTeam")


class ProcessReference(AzureDevOpsBaseModel):
    """Reference to a process template."""
    
    id: str
    name: str
    url: Optional[str] = None


class ReferenceLinks(AzureDevOpsBaseModel):
    """Collection of reference links."""
    
    web: Optional[str] = None
    self: Optional[str] = Field(None, alias="self")
    
    class Config:
        # Allow arbitrary field names for dynamic links
        extra = "allow"


class GraphSubjectBase(AzureDevOpsBaseModel):
    """Base class for graph subjects."""
    
    descriptor: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    url: Optional[str] = None
    
    class Config:
        extra = "allow"


class AccessLevel(Enum):
    """Access levels for users."""
    NONE = "none"
    LICENSED = "licensed"
    STAKEHOLDER = "stakeholder"


class GroupLicenseRule(AzureDevOpsBaseModel):
    """Group license rule."""
    
    access_level: Optional[str] = Field(None, alias="accessLevel")
    group_id: Optional[str] = Field(None, alias="groupId")


class Extension(AzureDevOpsBaseModel):
    """Extension reference."""
    
    extension_id: str = Field(alias="extensionId")
    extension_name: str = Field(alias="extensionName")
    account_id: Optional[str] = Field(None, alias="accountId")


class OperationStatus(Enum):
    """Status of an operation."""
    NOT_SET = "notSet"
    QUEUED = "queued"
    IN_PROGRESS = "inProgress"
    CANCELLED = "cancelled"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class OperationReference(AzureDevOpsBaseModel):
    """Reference to an operation."""
    
    id: str
    status: OperationStatus
    url: Optional[str] = None
    plugin_id: Optional[str] = Field(None, alias="pluginId")


class JsonPatchOperation(AzureDevOpsBaseModel):
    """JSON Patch operation for updates."""
    
    op: str  # add, remove, replace, move, copy, test
    path: str
    value: Optional[Any] = None
    from_path: Optional[str] = Field(None, alias="from")


class VssJsonCollectionWrapper(AzureDevOpsBaseModel):
    """Wrapper for VSS JSON collections."""
    
    count: int
    value: List[Any]


class PagedList(AzureDevOpsBaseModel):
    """Paged list response."""
    
    count: Optional[int] = None
    value: List[Any]
    continuation_token: Optional[str] = Field(None, alias="continuationToken")
    
    @property
    def has_more(self) -> bool:
        """Check if there are more items available."""
        return bool(self.continuation_token)


# Common field patterns
ID_FIELD = Field(..., description="Unique identifier")
NAME_FIELD = Field(..., description="Name")
URL_FIELD = Field(None, description="URL")
CREATED_DATE_FIELD = Field(None, description="Creation date", alias="createdDate")
MODIFIED_DATE_FIELD = Field(None, description="Last modified date", alias="lastModifiedDate")
CREATED_BY_FIELD = Field(None, description="Created by", alias="createdBy")
MODIFIED_BY_FIELD = Field(None, description="Last modified by", alias="lastModifiedBy")
