"""
Models for Work Item Tracking entities
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pydantic import Field, validator

from .common import (
    AzureDevOpsBaseModel,
    IdentityRef,
    TeamProjectReference,
    ReferenceLinks,
    ID_FIELD,
    NAME_FIELD,
    URL_FIELD,
    CREATED_DATE_FIELD,
    MODIFIED_DATE_FIELD,
    CREATED_BY_FIELD,
    MODIFIED_BY_FIELD
)


class WorkItemType(AzureDevOpsBaseModel):
    """Work item type model."""
    
    name: str = NAME_FIELD
    reference_name: str = Field(alias="referenceName")
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    is_disabled: Optional[bool] = Field(None, alias="isDisabled")
    
    # XML definition
    xml_form: Optional[str] = Field(None, alias="xmlForm")
    
    # Fields
    field_instances: Optional[List["WorkItemTypeFieldInstance"]] = Field(None, alias="fieldInstances")
    
    # Transitions
    transitions: Optional[Dict[str, List["WorkItemStateTransition"]]] = None
    
    # States
    states: Optional[List["WorkItemStateColor"]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class WorkItemFieldType(Enum):
    """Work item field type enumeration."""
    STRING = "string"
    INTEGER = "integer"
    DATETIME = "dateTime"
    PLAIN_TEXT = "plainText"
    HTML = "html"
    TREE_PATH = "treePath"
    HISTORY = "history"
    DOUBLE = "double"
    GUID = "guid"
    BOOLEAN = "boolean"
    IDENTITY = "identity"
    PICK_LIST_STRING = "picklistString"
    PICK_LIST_INTEGER = "picklistInteger"
    PICK_LIST_DOUBLE = "picklistDouble"


class WorkItemFieldUsage(Enum):
    """Work item field usage enumeration."""
    NONE = "none"
    WORK_ITEM = "workItem"
    WORK_ITEM_LINK = "workItemLink"
    TREE = "tree"
    WORK_ITEM_TYPE_EXTENSION = "workItemTypeExtension"


class WorkItemField(AzureDevOpsBaseModel):
    """Work item field model."""
    
    name: str = NAME_FIELD
    reference_name: str = Field(alias="referenceName")
    description: Optional[str] = None
    type: WorkItemFieldType
    usage: Optional[WorkItemFieldUsage] = None
    read_only: Optional[bool] = Field(None, alias="readOnly")
    can_sort_by: Optional[bool] = Field(None, alias="canSortBy")
    is_queryable: Optional[bool] = Field(None, alias="isQueryable")
    is_identity: Optional[bool] = Field(None, alias="isIdentity")
    is_picklist: Optional[bool] = Field(None, alias="isPicklist")
    is_picklist_suggested: Optional[bool] = Field(None, alias="isPicklistSuggested")
    
    # Supported operations
    supported_operations: Optional[List[Dict[str, Any]]] = Field(None, alias="supportedOperations")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class WorkItem(AzureDevOpsBaseModel):
    """Work item model."""
    
    id: Optional[int] = None
    rev: Optional[int] = None
    fields: Optional[Dict[str, Any]] = None
    relations: Optional[List["WorkItemRelation"]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD
    
    # Common field helpers
    @property
    def title(self) -> Optional[str]:
        return self.fields.get("System.Title") if self.fields else None
    
    @property
    def work_item_type(self) -> Optional[str]:
        return self.fields.get("System.WorkItemType") if self.fields else None
    
    @property
    def state(self) -> Optional[str]:
        return self.fields.get("System.State") if self.fields else None
    
    @property
    def assigned_to(self) -> Optional[str]:
        assigned = self.fields.get("System.AssignedTo") if self.fields else None
        if isinstance(assigned, dict):
            return assigned.get("displayName")
        return assigned
    
    @property
    def area_path(self) -> Optional[str]:
        return self.fields.get("System.AreaPath") if self.fields else None
    
    @property
    def iteration_path(self) -> Optional[str]:
        return self.fields.get("System.IterationPath") if self.fields else None
    
    @property
    def created_date(self) -> Optional[datetime]:
        date_str = self.fields.get("System.CreatedDate") if self.fields else None
        if date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return None
    
    @property
    def changed_date(self) -> Optional[datetime]:
        date_str = self.fields.get("System.ChangedDate") if self.fields else None
        if date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return None


class WorkItemRelationType(Enum):
    """Work item relation type enumeration."""
    PARENT = "System.LinkTypes.Hierarchy-Forward"
    CHILD = "System.LinkTypes.Hierarchy-Reverse"
    RELATED = "System.LinkTypes.Related"
    DUPLICATE = "System.LinkTypes.Duplicate-Forward"
    DUPLICATE_OF = "System.LinkTypes.Duplicate-Reverse"
    PREDECESSOR = "System.LinkTypes.Dependency-Forward"
    SUCCESSOR = "System.LinkTypes.Dependency-Reverse"
    TESTED_BY = "Microsoft.VSTS.Common.TestedBy-Forward"
    TESTS = "Microsoft.VSTS.Common.TestedBy-Reverse"


class WorkItemRelation(AzureDevOpsBaseModel):
    """Work item relation model."""
    
    rel: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


class WorkItemUpdate(AzureDevOpsBaseModel):
    """Work item update/revision model."""
    
    id: Optional[int] = None
    work_item_id: Optional[int] = Field(None, alias="workItemId")
    rev: Optional[int] = None
    revised_by: Optional[IdentityRef] = Field(None, alias="revisedBy")
    revised_date: Optional[datetime] = Field(None, alias="revisedDate")
    fields: Optional[Dict[str, Dict[str, Any]]] = None
    relations: Optional[Dict[str, List[WorkItemRelation]]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class WorkItemComment(AzureDevOpsBaseModel):
    """Work item comment model."""
    
    id: Optional[int] = None
    text: Optional[str] = None
    created_by: Optional[IdentityRef] = Field(None, alias="createdBy")
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    modified_by: Optional[IdentityRef] = Field(None, alias="modifiedBy")
    modified_date: Optional[datetime] = Field(None, alias="modifiedDate")
    
    # Format
    format: Optional[str] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class WorkItemQueryType(Enum):
    """Work item query type enumeration."""
    FLAT = "flat"
    TREE = "tree"
    ONE_HOP = "oneHop"


class WorkItemQuery(AzureDevOpsBaseModel):
    """Work item query model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    path: Optional[str] = None
    created_by: Optional[IdentityRef] = Field(None, alias="createdBy")
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    last_modified_by: Optional[IdentityRef] = Field(None, alias="lastModifiedBy")
    last_modified_date: Optional[datetime] = Field(None, alias="lastModifiedDate")
    query_type: Optional[WorkItemQueryType] = Field(None, alias="queryType")
    wiql: Optional[str] = None
    
    # Flags
    is_folder: Optional[bool] = Field(None, alias="isFolder")
    is_public: Optional[bool] = Field(None, alias="isPublic")
    is_deleted: Optional[bool] = Field(None, alias="isDeleted")
    
    # Hierarchy
    has_children: Optional[bool] = Field(None, alias="hasChildren")
    children: Optional[List["WorkItemQuery"]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class WorkItemQueryResult(AzureDevOpsBaseModel):
    """Work item query result model."""
    
    query_type: WorkItemQueryType = Field(alias="queryType")
    query_result_type: Optional[str] = Field(None, alias="queryResultType")
    as_of: Optional[datetime] = Field(None, alias="asOf")
    columns: Optional[List[Dict[str, Any]]] = None
    sort_columns: Optional[List[Dict[str, Any]]] = Field(None, alias="sortColumns")
    work_items: Optional[List[Dict[str, int]]] = Field(None, alias="workItems")
    work_item_relations: Optional[List[Dict[str, Any]]] = Field(None, alias="workItemRelations")


class WorkItemStateTransition(AzureDevOpsBaseModel):
    """Work item state transition model."""
    
    to: str
    actions: Optional[List[str]] = None


class WorkItemStateColor(AzureDevOpsBaseModel):
    """Work item state color model."""
    
    name: str = NAME_FIELD
    color: str
    category: Optional[str] = None


class WorkItemTypeFieldInstance(AzureDevOpsBaseModel):
    """Work item type field instance model."""
    
    field: WorkItemField
    help_text: Optional[str] = Field(None, alias="helpText")
    always_required: Optional[bool] = Field(None, alias="alwaysRequired")
    dependent_fields: Optional[List[Dict[str, Any]]] = Field(None, alias="dependentFields")
    
    # Default value
    default_value: Optional[Any] = Field(None, alias="defaultValue")
    
    # Allowed values
    allowed_values: Optional[List[str]] = Field(None, alias="allowedValues")


class WorkItemClassificationNode(AzureDevOpsBaseModel):
    """Work item classification node (Area/Iteration) model."""
    
    id: int = ID_FIELD
    name: str = NAME_FIELD
    structure_type: Optional[str] = Field(None, alias="structureType")
    has_children: Optional[bool] = Field(None, alias="hasChildren")
    children: Optional[List["WorkItemClassificationNode"]] = None
    path: Optional[str] = None
    
    # Attributes for iterations
    attributes: Optional[Dict[str, Any]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


# Request/Update models
class WorkItemUpdateRequest(AzureDevOpsBaseModel):
    """Request model for updating work items using JSON Patch."""
    
    operations: List[Dict[str, Any]]
    
    @classmethod
    def add_field(cls, field: str, value: Any) -> Dict[str, Any]:
        """Create operation to add/update a field."""
        return {
            "op": "add",
            "path": f"/fields/{field}",
            "value": value
        }
    
    @classmethod
    def remove_field(cls, field: str) -> Dict[str, Any]:
        """Create operation to remove a field."""
        return {
            "op": "remove",
            "path": f"/fields/{field}"
        }
    
    @classmethod
    def add_relation(cls, relation_type: str, url: str, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create operation to add a relation."""
        relation = {
            "rel": relation_type,
            "url": url
        }
        if attributes:
            relation["attributes"] = attributes
        
        return {
            "op": "add",
            "path": "/relations/-",
            "value": relation
        }


class WorkItemBatchRequest(AzureDevOpsBaseModel):
    """Batch request for work item operations."""
    
    requests: List[Dict[str, Any]]


# Response wrapper models
class WorkItemsResponse(AzureDevOpsBaseModel):
    """Response model for work items list."""
    
    count: int
    value: List[WorkItem]


class WorkItemTypesResponse(AzureDevOpsBaseModel):
    """Response model for work item types list."""
    
    count: int
    value: List[WorkItemType]


class WorkItemFieldsResponse(AzureDevOpsBaseModel):
    """Response model for work item fields list."""
    
    count: int
    value: List[WorkItemField]


class WorkItemQueriesResponse(AzureDevOpsBaseModel):
    """Response model for work item queries list."""
    
    count: int
    value: List[WorkItemQuery]


# Update forward references
WorkItemQuery.update_forward_refs()
WorkItemClassificationNode.update_forward_refs()
