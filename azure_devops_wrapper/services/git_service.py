"""
Git service for Azure DevOps - Repositories, Pull Requests, Commits, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator
from ..core import HTTPClient, create_paginator
from ..models import (
    GitRepository, GitRef, GitCommitRef, GitPullRequest, GitPush, GitItem,
    GitPullRequestCreateRequest, GitRepositoryCreateOptions, GitRefUpdateRequest,
    GitRepositoriesResponse, GitRefsResponse, GitCommitsResponse, GitPullRequestsResponse,
    GitPullRequestThread, GitPullRequestComment, GitCommitComment, Vote, IdentityRefWithVote
)


class GitService:
    """Service for Git operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Repositories
    async def list_repositories(
        self,
        project: Optional[str] = None,
        include_links: Optional[bool] = None,
        include_all_urls: Optional[bool] = None,
        include_hidden: Optional[bool] = None
    ) -> List[GitRepository]:
        """
        List Git repositories.
        
        Args:
            project: Project ID or name (if None, lists all repositories)
            include_links: Include repository links
            include_all_urls: Include all repository URLs
            include_hidden: Include hidden repositories
            
        Returns:
            List of Git repositories
        """
        params = {}
        if include_links:
            params['includeLinks'] = include_links
        if include_all_urls:
            params['includeAllUrls'] = include_all_urls
        if include_hidden:
            params['includeHidden'] = include_hidden
        
        endpoint = "git/repositories"
        if project:
            endpoint = f"projects/{project}/git/repositories"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = GitRepositoriesResponse(**response_data)
        return response.value
    
    async def get_repository(
        self,
        repository_id: str,
        project: Optional[str] = None
    ) -> GitRepository:
        """
        Get a specific repository.
        
        Args:
            repository_id: Repository ID or name
            project: Project ID or name
            
        Returns:
            Git repository details
        """
        endpoint = f"git/repositories/{repository_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}"
        
        response_data = await self.client.get_json(endpoint)
        return GitRepository(**response_data)
    
    async def create_repository(
        self,
        repository_options: GitRepositoryCreateOptions,
        project: Optional[str] = None
    ) -> GitRepository:
        """
        Create a new Git repository.
        
        Args:
            repository_options: Repository creation options
            project: Project ID or name
            
        Returns:
            Created repository details
        """
        endpoint = "git/repositories"
        if project:
            endpoint = f"projects/{project}/git/repositories"
        
        response_data = await self.client.post_json(
            endpoint,
            data=repository_options.dict_exclude_none()
        )
        return GitRepository(**response_data)
    
    async def update_repository(
        self,
        repository_id: str,
        repository_update: Dict[str, Any],
        project: Optional[str] = None
    ) -> GitRepository:
        """
        Update a repository.
        
        Args:
            repository_id: Repository ID
            repository_update: Repository update data
            project: Project ID or name
            
        Returns:
            Updated repository details
        """
        endpoint = f"git/repositories/{repository_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}"
        
        response_data = await self.client.patch_json(endpoint, data=repository_update)
        return GitRepository(**response_data)
    
    async def delete_repository(
        self,
        repository_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a repository.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
        """
        endpoint = f"git/repositories/{repository_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}"
        
        await self.client.delete(endpoint)
    
    # Refs (Branches and Tags)
    async def list_refs(
        self,
        repository_id: str,
        project: Optional[str] = None,
        filter: Optional[str] = None,
        include_links: Optional[bool] = None,
        include_statuses: Optional[bool] = None,
        include_my_branches: Optional[bool] = None,
        latest_statuses_only: Optional[bool] = None,
        peel_tags: Optional[bool] = None
    ) -> List[GitRef]:
        """
        List Git references (branches and tags).
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            filter: Ref filter (e.g., 'heads' for branches, 'tags' for tags)
            include_links: Include ref links
            include_statuses: Include ref statuses
            include_my_branches: Include user's branches
            latest_statuses_only: Include only latest statuses
            peel_tags: Peel tags
            
        Returns:
            List of Git references
        """
        params = {}
        if filter:
            params['filter'] = filter
        if include_links:
            params['includeLinks'] = include_links
        if include_statuses:
            params['includeStatuses'] = include_statuses
        if include_my_branches:
            params['includeMyBranches'] = include_my_branches
        if latest_statuses_only:
            params['latestStatusesOnly'] = latest_statuses_only
        if peel_tags:
            params['peelTags'] = peel_tags
        
        endpoint = f"git/repositories/{repository_id}/refs"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/refs"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = GitRefsResponse(**response_data)
        return response.value
    
    async def get_branches(
        self,
        repository_id: str,
        project: Optional[str] = None,
        **kwargs
    ) -> List[GitRef]:
        """
        Get repository branches.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            
        Returns:
            List of branches
        """
        return await self.list_refs(
            repository_id=repository_id,
            project=project,
            filter="heads",
            **kwargs
        )
    
    async def get_tags(
        self,
        repository_id: str,
        project: Optional[str] = None,
        **kwargs
    ) -> List[GitRef]:
        """
        Get repository tags.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            
        Returns:
            List of tags
        """
        return await self.list_refs(
            repository_id=repository_id,
            project=project,
            filter="tags",
            **kwargs
        )
    
    async def update_refs(
        self,
        repository_id: str,
        ref_updates: List[GitRefUpdateRequest],
        project: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Update Git references.
        
        Args:
            repository_id: Repository ID
            ref_updates: List of ref update requests
            project: Project ID or name
            
        Returns:
            List of update results
        """
        endpoint = f"git/repositories/{repository_id}/refs"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/refs"
        
        update_data = [update.dict_exclude_none() for update in ref_updates]
        response_data = await self.client.post_json(endpoint, data=update_data)
        return response_data.get('value', [])
    
    # Commits
    async def list_commits(
        self,
        repository_id: str,
        project: Optional[str] = None,
        search_criteria: Optional[Dict[str, Any]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[GitCommitRef]:
        """
        List commits in a repository.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            search_criteria: Search criteria for filtering commits
            top: Maximum number of commits to return
            skip: Number of commits to skip
            
        Returns:
            List of commits
        """
        params = {}
        if search_criteria:
            params.update(search_criteria)
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        endpoint = f"git/repositories/{repository_id}/commits"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/commits"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = GitCommitsResponse(**response_data)
        return response.value
    
    async def get_commit(
        self,
        repository_id: str,
        commit_id: str,
        project: Optional[str] = None,
        change_count: Optional[int] = None
    ) -> GitCommitRef:
        """
        Get a specific commit.
        
        Args:
            repository_id: Repository ID
            commit_id: Commit ID
            project: Project ID or name
            change_count: Number of changes to include
            
        Returns:
            Commit details
        """
        params = {}
        if change_count:
            params['changeCount'] = change_count
        
        endpoint = f"git/repositories/{repository_id}/commits/{commit_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/commits/{commit_id}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return GitCommitRef(**response_data)
    
    # Pull Requests
    async def list_pull_requests(
        self,
        repository_id: str,
        project: Optional[str] = None,
        search_criteria: Optional[Dict[str, Any]] = None,
        max_comment_length: Optional[int] = None,
        skip: Optional[int] = None,
        top: Optional[int] = None
    ) -> List[GitPullRequest]:
        """
        List pull requests.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            search_criteria: Search criteria for filtering PRs
            max_comment_length: Maximum comment length to include
            skip: Number of PRs to skip
            top: Maximum number of PRs to return
            
        Returns:
            List of pull requests
        """
        params = {}
        if search_criteria:
            params.update(search_criteria)
        if max_comment_length:
            params['maxCommentLength'] = max_comment_length
        if skip:
            params['$skip'] = skip
        if top:
            params['$top'] = top
        
        endpoint = f"git/repositories/{repository_id}/pullrequests"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = GitPullRequestsResponse(**response_data)
        return response.value
    
    async def get_pull_request(
        self,
        repository_id: str,
        pull_request_id: int,
        project: Optional[str] = None,
        max_comment_length: Optional[int] = None,
        skip: Optional[int] = None,
        top: Optional[int] = None,
        include_commits: Optional[bool] = None,
        include_work_item_refs: Optional[bool] = None
    ) -> GitPullRequest:
        """
        Get a specific pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            project: Project ID or name
            max_comment_length: Maximum comment length
            skip: Number of items to skip
            top: Maximum number of items
            include_commits: Include commits
            include_work_item_refs: Include work item references
            
        Returns:
            Pull request details
        """
        params = {}
        if max_comment_length:
            params['maxCommentLength'] = max_comment_length
        if skip:
            params['$skip'] = skip
        if top:
            params['$top'] = top
        if include_commits:
            params['includeCommits'] = include_commits
        if include_work_item_refs:
            params['includeWorkItemRefs'] = include_work_item_refs
        
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return GitPullRequest(**response_data)
    
    async def create_pull_request(
        self,
        repository_id: str,
        pull_request: GitPullRequestCreateRequest,
        project: Optional[str] = None,
        supports_iterations: Optional[bool] = None
    ) -> GitPullRequest:
        """
        Create a new pull request.
        
        Args:
            repository_id: Repository ID
            pull_request: Pull request creation data
            project: Project ID or name
            supports_iterations: Support iterations
            
        Returns:
            Created pull request
        """
        params = {}
        if supports_iterations:
            params['supportsIterations'] = supports_iterations
        
        endpoint = f"git/repositories/{repository_id}/pullrequests"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests"
        
        response_data = await self.client.post_json(
            endpoint,
            data=pull_request.dict_exclude_none(),
            params=params
        )
        return GitPullRequest(**response_data)
    
    async def update_pull_request(
        self,
        repository_id: str,
        pull_request_id: int,
        pull_request_update: Dict[str, Any],
        project: Optional[str] = None
    ) -> GitPullRequest:
        """
        Update a pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            pull_request_update: Pull request update data
            project: Project ID or name
            
        Returns:
            Updated pull request
        """
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}"
        
        response_data = await self.client.patch_json(endpoint, data=pull_request_update)
        return GitPullRequest(**response_data)
    
    async def abandon_pull_request(
        self,
        repository_id: str,
        pull_request_id: int,
        project: Optional[str] = None
    ) -> GitPullRequest:
        """
        Abandon a pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            project: Project ID or name
            
        Returns:
            Abandoned pull request
        """
        return await self.update_pull_request(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            pull_request_update={"status": "abandoned"},
            project=project
        )
    
    async def complete_pull_request(
        self,
        repository_id: str,
        pull_request_id: int,
        project: Optional[str] = None,
        completion_options: Optional[Dict[str, Any]] = None
    ) -> GitPullRequest:
        """
        Complete a pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            project: Project ID or name
            completion_options: Completion options
            
        Returns:
            Completed pull request
        """
        update_data = {"status": "completed"}
        if completion_options:
            update_data["completionOptions"] = completion_options
        
        return await self.update_pull_request(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            pull_request_update=update_data,
            project=project
        )
    
    # Pull Request Reviewers
    async def get_pull_request_reviewers(
        self,
        repository_id: str,
        pull_request_id: int,
        project: Optional[str] = None
    ) -> List[IdentityRefWithVote]:
        """
        Get pull request reviewers.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            project: Project ID or name
            
        Returns:
            List of reviewers with votes
        """
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers"
        
        response_data = await self.client.get_json(endpoint)
        reviewers = response_data.get('value', [])
        return [IdentityRefWithVote(**reviewer) for reviewer in reviewers]
    
    async def add_pull_request_reviewer(
        self,
        repository_id: str,
        pull_request_id: int,
        reviewer_id: str,
        project: Optional[str] = None,
        vote: Optional[Vote] = None,
        is_required: Optional[bool] = None
    ) -> IdentityRefWithVote:
        """
        Add a reviewer to a pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            reviewer_id: Reviewer ID
            project: Project ID or name
            vote: Initial vote
            is_required: Whether reviewer is required
            
        Returns:
            Added reviewer
        """
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers/{reviewer_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers/{reviewer_id}"
        
        data = {}
        if vote is not None:
            data['vote'] = vote.value
        if is_required is not None:
            data['isRequired'] = is_required
        
        response_data = await self.client.put_json(endpoint, data=data)
        return IdentityRefWithVote(**response_data)
    
    async def remove_pull_request_reviewer(
        self,
        repository_id: str,
        pull_request_id: int,
        reviewer_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Remove a reviewer from a pull request.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            reviewer_id: Reviewer ID
            project: Project ID or name
        """
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers/{reviewer_id}"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}/reviewers/{reviewer_id}"
        
        await self.client.delete(endpoint)
    
    # Pull Request Threads and Comments
    async def get_pull_request_threads(
        self,
        repository_id: str,
        pull_request_id: int,
        project: Optional[str] = None,
        iteration: Optional[int] = None,
        base_iteration: Optional[int] = None
    ) -> List[GitPullRequestThread]:
        """
        Get pull request threads.
        
        Args:
            repository_id: Repository ID
            pull_request_id: Pull request ID
            project: Project ID or name
            iteration: Iteration number
            base_iteration: Base iteration number
            
        Returns:
            List of pull request threads
        """
        params = {}
        if iteration:
            params['$iteration'] = iteration
        if base_iteration:
            params['$baseIteration'] = base_iteration
        
        endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}/threads"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/pullrequests/{pull_request_id}/threads"
        
        response_data = await self.client.get_json(endpoint, params=params)
        threads = response_data.get('value', [])
        return [GitPullRequestThread(**thread) for thread in threads]
    
    # Items and Content
    async def get_item(
        self,
        repository_id: str,
        path: str,
        project: Optional[str] = None,
        scope_path: Optional[str] = None,
        recursion_level: Optional[str] = None,
        include_content_metadata: Optional[bool] = None,
        latest_processed_change: Optional[bool] = None,
        download: Optional[bool] = None,
        version_descriptor: Optional[Dict[str, Any]] = None
    ) -> GitItem:
        """
        Get a Git item (file or folder).
        
        Args:
            repository_id: Repository ID
            path: Item path
            project: Project ID or name
            scope_path: Scope path
            recursion_level: Recursion level (none, onelevel, full)
            include_content_metadata: Include content metadata
            latest_processed_change: Latest processed change
            download: Download content
            version_descriptor: Version descriptor
            
        Returns:
            Git item
        """
        params = {"path": path}
        if scope_path:
            params['scopePath'] = scope_path
        if recursion_level:
            params['recursionLevel'] = recursion_level
        if include_content_metadata:
            params['includeContentMetadata'] = include_content_metadata
        if latest_processed_change:
            params['latestProcessedChange'] = latest_processed_change
        if download:
            params['download'] = download
        if version_descriptor:
            params.update(version_descriptor)
        
        endpoint = f"git/repositories/{repository_id}/items"
        if project:
            endpoint = f"projects/{project}/git/repositories/{repository_id}/items"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return GitItem(**response_data)
    
    # Utility methods
    async def get_all_repositories(self, project: Optional[str] = None, **kwargs) -> List[GitRepository]:
        """
        Get all repositories using pagination.
        
        Args:
            project: Project ID or name
            
        Returns:
            List of all repositories
        """
        return await self.list_repositories(project=project, **kwargs)
    
    async def iterate_commits(
        self,
        repository_id: str,
        project: Optional[str] = None,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[GitCommitRef, None]:
        """
        Iterate through all commits in a repository.
        
        Args:
            repository_id: Repository ID
            project: Project ID or name
            page_size: Number of commits per page
            
        Yields:
            Commits one by one
        """
        async def request_func(**params):
            commits = await self.list_commits(
                repository_id=repository_id,
                project=project,
                **params
            )
            return {"value": commits, "count": len(commits)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for commit in paginator.iterate_items(**kwargs):
            yield commit
