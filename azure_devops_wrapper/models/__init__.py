"""
Models package for Azure DevOps Wrapper
"""

# Import all models to make them available at package level
from .common import *
from .core import *
from .git import *
from .work_items import *

__all__ = [
    # Common models
    "AzureDevOpsBaseModel",
    "IdentityRef", 
    "TeamProjectReference",
    "ProcessReference",
    "ReferenceLinks",
    "WebApiTeamRef",
    "GraphSubjectBase",
    "AccessLevel",
    "GroupLicenseRule",
    "Extension",
    "OperationStatus",
    "OperationReference",
    "JsonPatchOperation",
    "VssJsonCollectionWrapper",
    "PagedList",
    
    # Core models
    "ProjectState",
    "ProjectVisibility", 
    "TeamProject",
    "TeamProjectCollection",
    "WebApiTeam",
    "TeamMember",
    "TeamMembersRef",
    "Process",
    "ProcessType",
    "ExtensionState",
    "InstalledExtension",
    "OrganizationInfo",
    "AccountInfo",
    "ProjectProperty",
    "ProjectProperties",
    "ProjectCreateRequest",
    "TeamCreateRequest",
    "ProjectUpdateRequest",
    "ProjectsResponse",
    "TeamsResponse",
    "ProcessesResponse",
    "ExtensionsResponse",
    
    # Git models
    "GitRepository",
    "GitRef",
    "GitCommitRef",
    "ChangeType",
    "GitChange",
    "GitObjectType",
    "GitItem",
    "PullRequestStatus",
    "GitPullRequest",
    "Vote",
    "IdentityRefWithVote",
    "GitPush",
    "GitRefUpdate",
    "GitCommitComment",
    "GitPullRequestThread",
    "GitPullRequestComment",
    "WebApiTagDefinition",
    "GitImportRequest",
    "GitRepositoryCreateOptions",
    "GitPullRequestCreateRequest",
    "GitRefUpdateRequest",
    "GitRepositoriesResponse",
    "GitRefsResponse",
    "GitCommitsResponse",
    "GitPullRequestsResponse",
    
    # Work Items models
    "WorkItemType",
    "WorkItemFieldType",
    "WorkItemFieldUsage",
    "WorkItemField",
    "WorkItem",
    "WorkItemRelationType",
    "WorkItemRelation",
    "WorkItemUpdate",
    "WorkItemComment",
    "WorkItemQueryType",
    "WorkItemQuery",
    "WorkItemQueryResult",
    "WorkItemStateTransition",
    "WorkItemStateColor",
    "WorkItemTypeFieldInstance",
    "WorkItemClassificationNode",
    "WorkItemUpdateRequest",
    "WorkItemBatchRequest",
    "WorkItemsResponse",
    "WorkItemTypesResponse",
    "WorkItemFieldsResponse",
    "WorkItemQueriesResponse"
]
