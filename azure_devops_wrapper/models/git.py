"""
Models for Git-related entities (Repositories, Commits, Pull Requests, etc.)
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


class GitRepository(AzureDevOpsBaseModel):
    """Git repository model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    url: Optional[str] = URL_FIELD
    project: Optional[TeamProjectReference] = None
    default_branch: Optional[str] = Field(None, alias="defaultBranch")
    size: Optional[int] = None
    remote_url: Optional[str] = Field(None, alias="remoteUrl")
    ssh_url: Optional[str] = Field(None, alias="sshUrl")
    web_url: Optional[str] = Field(None, alias="webUrl")
    
    # Flags
    is_fork: Optional[bool] = Field(None, alias="isFork")
    is_disabled: Optional[bool] = Field(None, alias="isDisabled")
    
    # Parent repository (for forks)
    parent_repository: Optional["GitRepository"] = Field(None, alias="parentRepository")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class GitRef(AzureDevOpsBaseModel):
    """Git reference (branch/tag) model."""
    
    name: str = NAME_FIELD
    object_id: str = Field(alias="objectId")
    url: Optional[str] = URL_FIELD
    creator: Optional[IdentityRef] = None
    is_locked: Optional[bool] = Field(None, alias="isLocked")
    is_locked_by: Optional[IdentityRef] = Field(None, alias="isLockedBy")


class GitCommitRef(AzureDevOpsBaseModel):
    """Git commit reference model."""
    
    commit_id: str = Field(alias="commitId")
    url: Optional[str] = URL_FIELD
    author: Optional[IdentityRef] = None
    committer: Optional[IdentityRef] = None
    comment: Optional[str] = None
    comment_truncated: Optional[bool] = Field(None, alias="commentTruncated")
    
    # Timestamps
    author_date: Optional[datetime] = Field(None, alias="author.date")
    committer_date: Optional[datetime] = Field(None, alias="committer.date")
    
    # Changes
    change_counts: Optional[Dict[str, int]] = Field(None, alias="changeCounts")
    changes: Optional[List["GitChange"]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class ChangeType(Enum):
    """Git change type enumeration."""
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    RENAME = "rename"
    UNDELETE = "undelete"
    BRANCH = "branch"
    MERGE = "merge"
    ENCODING = "encoding"
    NONE = "none"


class GitChange(AzureDevOpsBaseModel):
    """Git change model."""
    
    change_type: ChangeType = Field(alias="changeType")
    item: Optional["GitItem"] = None
    new_content: Optional[Dict[str, Any]] = Field(None, alias="newContent")
    source_server_item: Optional[str] = Field(None, alias="sourceServerItem")
    url: Optional[str] = URL_FIELD


class GitObjectType(Enum):
    """Git object type enumeration."""
    BAD = "bad"
    COMMIT = "commit"
    TREE = "tree"
    BLOB = "blob"
    TAG = "tag"
    EXT2 = "ext2"
    OFSDELTA = "ofsDelta"
    REFDELTA = "refDelta"


class GitItem(AzureDevOpsBaseModel):
    """Git item (file/folder) model."""
    
    object_id: str = Field(alias="objectId")
    git_object_type: GitObjectType = Field(alias="gitObjectType")
    commit_id: str = Field(alias="commitId")
    path: str
    is_folder: Optional[bool] = Field(None, alias="isFolder")
    content_metadata: Optional[Dict[str, Any]] = Field(None, alias="contentMetadata")
    url: Optional[str] = URL_FIELD
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class PullRequestStatus(Enum):
    """Pull request status enumeration."""
    NOT_SET = "notSet"
    ACTIVE = "active"
    ABANDONED = "abandoned"
    COMPLETED = "completed"
    ALL = "all"


class GitPullRequest(AzureDevOpsBaseModel):
    """Git pull request model."""
    
    pull_request_id: int = Field(alias="pullRequestId")
    code_review_id: Optional[int] = Field(None, alias="codeReviewId")
    status: PullRequestStatus
    created_by: IdentityRef = CREATED_BY_FIELD
    creation_date: datetime = CREATED_DATE_FIELD
    closed_date: Optional[datetime] = Field(None, alias="closedDate")
    title: str
    description: Optional[str] = None
    source_ref_name: str = Field(alias="sourceRefName")
    target_ref_name: str = Field(alias="targetRefName")
    merge_status: Optional[str] = Field(None, alias="mergeStatus")
    merge_id: Optional[str] = Field(None, alias="mergeId")
    
    # Repository
    repository: GitRepository
    
    # Reviewers
    reviewers: Optional[List["IdentityRefWithVote"]] = None
    
    # Work items
    work_item_refs: Optional[List[Dict[str, Any]]] = Field(None, alias="workItemRefs")
    
    # Labels
    labels: Optional[List["WebApiTagDefinition"]] = None
    
    # Auto-complete
    auto_complete_set_by: Optional[IdentityRef] = Field(None, alias="autoCompleteSetBy")
    
    # Completion options
    completion_options: Optional[Dict[str, Any]] = Field(None, alias="completionOptions")
    completion_queue_time: Optional[datetime] = Field(None, alias="completionQueueTime")
    
    # Artifacts
    artifacts: Optional[List[Dict[str, Any]]] = None
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class Vote(Enum):
    """Pull request vote enumeration."""
    APPROVED = 10
    APPROVED_WITH_SUGGESTIONS = 5
    NO_VOTE = 0
    WAITING_FOR_AUTHOR = -5
    REJECTED = -10


class IdentityRefWithVote(IdentityRef):
    """Identity reference with vote."""
    
    vote: Optional[Vote] = None
    is_required: Optional[bool] = Field(None, alias="isRequired")
    is_container: Optional[bool] = Field(None, alias="isContainer")
    has_declined: Optional[bool] = Field(None, alias="hasDeclined")


class GitPush(AzureDevOpsBaseModel):
    """Git push model."""
    
    push_id: int = Field(alias="pushId")
    date: datetime
    pushed_by: IdentityRef = Field(alias="pushedBy")
    
    # Commits
    commits: Optional[List[GitCommitRef]] = None
    
    # References updated
    ref_updates: Optional[List["GitRefUpdate"]] = Field(None, alias="refUpdates")
    
    # Repository
    repository: GitRepository
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")
    url: Optional[str] = URL_FIELD


class GitRefUpdate(AzureDevOpsBaseModel):
    """Git reference update model."""
    
    name: str = NAME_FIELD
    old_object_id: str = Field(alias="oldObjectId")
    new_object_id: str = Field(alias="newObjectId")
    repository_id: Optional[str] = Field(None, alias="repositoryId")


class GitCommitComment(AzureDevOpsBaseModel):
    """Git commit comment model."""
    
    comment_id: int = Field(alias="commentId")
    content: str
    author: IdentityRef
    published_date: datetime = Field(alias="publishedDate")
    last_updated_date: Optional[datetime] = Field(None, alias="lastUpdatedDate")
    last_content_updated_date: Optional[datetime] = Field(None, alias="lastContentUpdatedDate")
    
    # Comment type and threading
    comment_type: Optional[str] = Field(None, alias="commentType")
    parent_comment_id: Optional[int] = Field(None, alias="parentCommentId")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class GitPullRequestThread(AzureDevOpsBaseModel):
    """Git pull request thread model."""
    
    id: int
    published_date: datetime = Field(alias="publishedDate")
    last_updated_date: Optional[datetime] = Field(None, alias="lastUpdatedDate")
    comments: Optional[List["GitPullRequestComment"]] = None
    status: Optional[str] = None
    thread_context: Optional[Dict[str, Any]] = Field(None, alias="threadContext")
    
    # Properties
    properties: Optional[Dict[str, Any]] = None
    
    # Identities
    identities: Optional[Dict[str, IdentityRef]] = None


class GitPullRequestComment(AzureDevOpsBaseModel):
    """Git pull request comment model."""
    
    id: int
    parent_comment_id: Optional[int] = Field(None, alias="parentCommentId")
    author: IdentityRef
    content: str
    published_date: datetime = Field(alias="publishedDate")
    last_updated_date: Optional[datetime] = Field(None, alias="lastUpdatedDate")
    last_content_updated_date: Optional[datetime] = Field(None, alias="lastContentUpdatedDate")
    comment_type: Optional[str] = Field(None, alias="commentType")
    
    # Usage status
    uses_parent_comment_date: Optional[bool] = Field(None, alias="usesParentCommentDate")
    
    # Links
    links: Optional[ReferenceLinks] = Field(None, alias="_links")


class WebApiTagDefinition(AzureDevOpsBaseModel):
    """Tag definition model."""
    
    id: str = ID_FIELD
    name: str = NAME_FIELD
    url: Optional[str] = URL_FIELD
    active: Optional[bool] = None


class GitImportRequest(AzureDevOpsBaseModel):
    """Git import request model."""
    
    import_request_id: Optional[int] = Field(None, alias="importRequestId")
    detailed_status: Optional[Dict[str, Any]] = Field(None, alias="detailedStatus")
    import_request_source: Optional[Dict[str, Any]] = Field(None, alias="importRequestSource")
    repository: Optional[GitRepository] = None
    status: Optional[str] = None
    url: Optional[str] = URL_FIELD


# Create/Update request models
class GitRepositoryCreateOptions(AzureDevOpsBaseModel):
    """Options for creating a Git repository."""
    
    name: str = NAME_FIELD
    project: Optional[TeamProjectReference] = None
    parent_repository: Optional[GitRepository] = Field(None, alias="parentRepository")


class GitPullRequestCreateRequest(AzureDevOpsBaseModel):
    """Request model for creating a pull request."""
    
    source_ref_name: str = Field(alias="sourceRefName")
    target_ref_name: str = Field(alias="targetRefName")
    title: str
    description: Optional[str] = None
    reviewers: Optional[List[IdentityRef]] = None
    work_item_refs: Optional[List[Dict[str, str]]] = Field(None, alias="workItemRefs")
    
    @validator('source_ref_name', 'target_ref_name')
    def validate_ref_names(cls, v):
        if not v.startswith('refs/heads/'):
            return f'refs/heads/{v}'
        return v


class GitRefUpdateRequest(AzureDevOpsBaseModel):
    """Request model for updating Git references."""
    
    name: str = NAME_FIELD
    old_object_id: str = Field(alias="oldObjectId")
    new_object_id: str = Field(alias="newObjectId")


# Response wrapper models
class GitRepositoriesResponse(AzureDevOpsBaseModel):
    """Response model for repositories list."""
    
    count: int
    value: List[GitRepository]


class GitRefsResponse(AzureDevOpsBaseModel):
    """Response model for Git refs list."""
    
    count: int
    value: List[GitRef]


class GitCommitsResponse(AzureDevOpsBaseModel):
    """Response model for Git commits list."""
    
    count: int
    value: List[GitCommitRef]


class GitPullRequestsResponse(AzureDevOpsBaseModel):
    """Response model for pull requests list."""
    
    count: int
    value: List[GitPullRequest]


# Update forward references
GitRepository.update_forward_refs()
GitPullRequest.update_forward_refs()
GitCommitRef.update_forward_refs()
GitChange.update_forward_refs()
GitPush.update_forward_refs()
GitPullRequestThread.update_forward_refs()
