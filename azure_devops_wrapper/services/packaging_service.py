"""
Packaging service for Azure DevOps - Feeds, Packages, Artifacts, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    Feed, Package, PackageVersion, FeedPermission, FeedView, PackageMetrics,
    PackageDependency, RecycleBinPackage, PackageVersionProvenanceEntry,
    FeedsResponse, PackagesResponse, PackageVersionsResponse, FeedPermissionsResponse,
    FeedViewsResponse, RecycleBinPackagesResponse
)


class PackagingService:
    """Service for Package Management operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Feeds
    async def list_feeds(
        self,
        project: Optional[str] = None,
        feed_role: Optional[str] = None,
        include_deleted_upstreams: Optional[bool] = None
    ) -> List[Feed]:
        """
        List feeds in the organization or project.
        
        Args:
            project: Project ID or name (if None, lists organization feeds)
            feed_role: Feed role filter
            include_deleted_upstreams: Include deleted upstreams
            
        Returns:
            List of feeds
        """
        params = {}
        if feed_role:
            params['feedRole'] = feed_role
        if include_deleted_upstreams:
            params['includeDeletedUpstreams'] = include_deleted_upstreams
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds"
        else:
            endpoint = "packaging/feeds"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = FeedsResponse(**response_data)
        return response.value
    
    async def get_feed(
        self,
        feed_id: str,
        project: Optional[str] = None,
        include_deleted_upstreams: Optional[bool] = None
    ) -> Feed:
        """
        Get a specific feed.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            include_deleted_upstreams: Include deleted upstreams
            
        Returns:
            Feed details
        """
        params = {}
        if include_deleted_upstreams:
            params['includeDeletedUpstreams'] = include_deleted_upstreams
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return Feed(**response_data)
    
    async def create_feed(
        self,
        feed_data: Dict[str, Any],
        project: Optional[str] = None
    ) -> Feed:
        """
        Create a new feed.
        
        Args:
            feed_data: Feed creation data
            project: Project ID or name
            
        Returns:
            Created feed
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds"
        else:
            endpoint = "packaging/feeds"
        
        response_data = await self.client.post_json(endpoint, data=feed_data)
        return Feed(**response_data)
    
    async def update_feed(
        self,
        feed_id: str,
        feed_data: Dict[str, Any],
        project: Optional[str] = None
    ) -> Feed:
        """
        Update a feed.
        
        Args:
            feed_id: Feed ID or name
            feed_data: Feed update data
            project: Project ID or name
            
        Returns:
            Updated feed
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}"
        
        response_data = await self.client.patch_json(endpoint, data=feed_data)
        return Feed(**response_data)
    
    async def delete_feed(
        self,
        feed_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a feed.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}"
        
        await self.client.delete(endpoint)
    
    # Packages
    async def list_packages(
        self,
        feed_id: str,
        project: Optional[str] = None,
        protocol_type: Optional[str] = None,
        package_name_query: Optional[str] = None,
        normalized_package_name: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        include_description: Optional[bool] = None,
        get_top_package_versions: Optional[bool] = None,
        is_listed: Optional[bool] = None,
        is_cached: Optional[bool] = None,
        direct_upstream_id: Optional[str] = None
    ) -> List[Package]:
        """
        List packages in a feed.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            protocol_type: Protocol type filter (npm, nuget, pypi, etc.)
            package_name_query: Package name query
            normalized_package_name: Normalized package name
            top: Maximum number of packages
            skip: Number of packages to skip
            include_deleted: Include deleted packages
            include_description: Include package description
            get_top_package_versions: Get top package versions
            is_listed: Listed packages filter
            is_cached: Cached packages filter
            direct_upstream_id: Direct upstream ID filter
            
        Returns:
            List of packages
        """
        params = {}
        if protocol_type:
            params['protocolType'] = protocol_type
        if package_name_query:
            params['packageNameQuery'] = package_name_query
        if normalized_package_name:
            params['normalizedPackageName'] = normalized_package_name
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        if include_deleted:
            params['includeDeleted'] = include_deleted
        if include_description:
            params['includeDescription'] = include_description
        if get_top_package_versions:
            params['getTopPackageVersions'] = get_top_package_versions
        if is_listed is not None:
            params['isListed'] = is_listed
        if is_cached is not None:
            params['isCached'] = is_cached
        if direct_upstream_id:
            params['directUpstreamId'] = direct_upstream_id
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = PackagesResponse(**response_data)
        return response.value
    
    async def get_package(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None,
        include_all_versions: Optional[bool] = None,
        include_deleted: Optional[bool] = None,
        include_description: Optional[bool] = None
    ) -> Package:
        """
        Get a specific package.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
            include_all_versions: Include all versions
            include_deleted: Include deleted versions
            include_description: Include package description
            
        Returns:
            Package details
        """
        params = {}
        if include_all_versions:
            params['includeAllVersions'] = include_all_versions
        if include_deleted:
            params['includeDeleted'] = include_deleted
        if include_description:
            params['includeDescription'] = include_description
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return Package(**response_data)
    
    async def delete_package(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a package from the feed.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}"
        
        await self.client.delete(endpoint)
    
    # Package Versions
    async def list_package_versions(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None,
        include_deleted: Optional[bool] = None,
        is_listed: Optional[bool] = None,
        is_release: Optional[bool] = None
    ) -> List[PackageVersion]:
        """
        List versions of a package.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
            include_deleted: Include deleted versions
            is_listed: Listed versions filter
            is_release: Release versions filter
            
        Returns:
            List of package versions
        """
        params = {}
        if include_deleted:
            params['includeDeleted'] = include_deleted
        if is_listed is not None:
            params['isListed'] = is_listed
        if is_release is not None:
            params['isRelease'] = is_release
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/versions"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/versions"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = PackageVersionsResponse(**response_data)
        return response.value
    
    async def get_package_version(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        project: Optional[str] = None,
        show_deleted: Optional[bool] = None
    ) -> PackageVersion:
        """
        Get a specific package version.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            project: Project ID or name
            show_deleted: Show deleted version
            
        Returns:
            Package version details
        """
        params = {}
        if show_deleted:
            params['showDeleted'] = show_deleted
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return PackageVersion(**response_data)
    
    async def update_package_version(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        package_version_details: Dict[str, Any],
        project: Optional[str] = None
    ) -> PackageVersion:
        """
        Update a package version.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            package_version_details: Package version update data
            project: Project ID or name
            
        Returns:
            Updated package version
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        
        response_data = await self.client.patch_json(endpoint, data=package_version_details)
        return PackageVersion(**response_data)
    
    async def delete_package_version(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a package version.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        
        await self.client.delete(endpoint)
    
    async def restore_package_version_from_recycle_bin(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        project: Optional[str] = None
    ) -> None:
        """
        Restore a package version from recycle bin.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/versions/{package_version}"
        
        restore_data = {"deleted": False}
        await self.client.patch_json(endpoint, data=restore_data)
    
    # Feed Permissions
    async def get_feed_permissions(
        self,
        feed_id: str,
        project: Optional[str] = None,
        include_ids: Optional[bool] = None,
        exclude_inherited_permissions: Optional[bool] = None,
        include_deleted_feeds: Optional[bool] = None
    ) -> List[FeedPermission]:
        """
        Get feed permissions.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            include_ids: Include identity IDs
            exclude_inherited_permissions: Exclude inherited permissions
            include_deleted_feeds: Include deleted feeds
            
        Returns:
            List of feed permissions
        """
        params = {}
        if include_ids:
            params['includeIds'] = include_ids
        if exclude_inherited_permissions:
            params['excludeInheritedPermissions'] = exclude_inherited_permissions
        if include_deleted_feeds:
            params['includeDeletedFeeds'] = include_deleted_feeds
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/permissions"
        else:
            endpoint = f"packaging/feeds/{feed_id}/permissions"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = FeedPermissionsResponse(**response_data)
        return response.value
    
    async def set_feed_permissions(
        self,
        feed_id: str,
        permissions: List[Dict[str, Any]],
        project: Optional[str] = None
    ) -> List[FeedPermission]:
        """
        Set feed permissions.
        
        Args:
            feed_id: Feed ID or name
            permissions: List of permission settings
            project: Project ID or name
            
        Returns:
            List of updated feed permissions
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/permissions"
        else:
            endpoint = f"packaging/feeds/{feed_id}/permissions"
        
        response_data = await self.client.patch_json(endpoint, data=permissions)
        return [FeedPermission(**perm) for perm in response_data.get('value', [])]
    
    # Feed Views
    async def list_feed_views(
        self,
        feed_id: str,
        project: Optional[str] = None
    ) -> List[FeedView]:
        """
        List feed views.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            
        Returns:
            List of feed views
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/views"
        else:
            endpoint = f"packaging/feeds/{feed_id}/views"
        
        response_data = await self.client.get_json(endpoint)
        response = FeedViewsResponse(**response_data)
        return response.value
    
    async def get_feed_view(
        self,
        feed_id: str,
        view_id: str,
        project: Optional[str] = None
    ) -> FeedView:
        """
        Get a specific feed view.
        
        Args:
            feed_id: Feed ID or name
            view_id: View ID or name
            project: Project ID or name
            
        Returns:
            Feed view details
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/views/{view_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/views/{view_id}"
        
        response_data = await self.client.get_json(endpoint)
        return FeedView(**response_data)
    
    async def create_feed_view(
        self,
        feed_id: str,
        view_data: Dict[str, Any],
        project: Optional[str] = None
    ) -> FeedView:
        """
        Create a feed view.
        
        Args:
            feed_id: Feed ID or name
            view_data: View creation data
            project: Project ID or name
            
        Returns:
            Created feed view
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/views"
        else:
            endpoint = f"packaging/feeds/{feed_id}/views"
        
        response_data = await self.client.post_json(endpoint, data=view_data)
        return FeedView(**response_data)
    
    async def update_feed_view(
        self,
        feed_id: str,
        view_id: str,
        view_data: Dict[str, Any],
        project: Optional[str] = None
    ) -> FeedView:
        """
        Update a feed view.
        
        Args:
            feed_id: Feed ID or name
            view_id: View ID or name
            view_data: View update data
            project: Project ID or name
            
        Returns:
            Updated feed view
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/views/{view_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/views/{view_id}"
        
        response_data = await self.client.patch_json(endpoint, data=view_data)
        return FeedView(**response_data)
    
    async def delete_feed_view(
        self,
        feed_id: str,
        view_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a feed view.
        
        Args:
            feed_id: Feed ID or name
            view_id: View ID or name
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/views/{view_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/views/{view_id}"
        
        await self.client.delete(endpoint)
    
    # Recycle Bin
    async def list_recycle_bin_packages(
        self,
        feed_id: str,
        project: Optional[str] = None,
        protocol_type: Optional[str] = None,
        package_name_query: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[RecycleBinPackage]:
        """
        List packages in the recycle bin.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            protocol_type: Protocol type filter
            package_name_query: Package name query
            top: Maximum number of packages
            skip: Number of packages to skip
            
        Returns:
            List of recycle bin packages
        """
        params = {}
        if protocol_type:
            params['protocolType'] = protocol_type
        if package_name_query:
            params['packageNameQuery'] = package_name_query
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/recyclebin/packages"
        else:
            endpoint = f"packaging/feeds/{feed_id}/recyclebin/packages"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = RecycleBinPackagesResponse(**response_data)
        return response.value
    
    async def restore_package_from_recycle_bin(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Restore a package from the recycle bin.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/recyclebin/packages/{package_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/recyclebin/packages/{package_id}"
        
        restore_data = {"deleted": False}
        await self.client.patch_json(endpoint, data=restore_data)
    
    async def permanently_delete_package(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None
    ) -> None:
        """
        Permanently delete a package from recycle bin.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/recyclebin/packages/{package_id}"
        else:
            endpoint = f"packaging/feeds/{feed_id}/recyclebin/packages/{package_id}"
        
        await self.client.delete(endpoint)
    
    # Package Metrics
    async def get_package_metrics(
        self,
        feed_id: str,
        package_id: str,
        project: Optional[str] = None
    ) -> PackageMetrics:
        """
        Get package download metrics.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            project: Project ID or name
            
        Returns:
            Package metrics
        """
        if project:
            endpoint = f"projects/{project}/packaging/feeds/{feed_id}/packages/{package_id}/metrics"
        else:
            endpoint = f"packaging/feeds/{feed_id}/packages/{package_id}/metrics"
        
        response_data = await self.client.get_json(endpoint)
        return PackageMetrics(**response_data)
    
    # Utility methods
    async def promote_package_to_view(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        view_id: str,
        project: Optional[str] = None
    ) -> PackageVersion:
        """
        Promote a package version to a view.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            view_id: View ID to promote to
            project: Project ID or name
            
        Returns:
            Updated package version
        """
        promotion_data = {
            "views": {
                "op": "add",
                "path": f"/views/{view_id}",
                "value": view_id
            }
        }
        
        return await self.update_package_version(
            feed_id=feed_id,
            package_id=package_id,
            package_version=package_version,
            package_version_details=promotion_data,
            project=project
        )
    
    async def deprecate_package_version(
        self,
        feed_id: str,
        package_id: str,
        package_version: str,
        project: Optional[str] = None,
        message: Optional[str] = None
    ) -> PackageVersion:
        """
        Deprecate a package version.
        
        Args:
            feed_id: Feed ID or name
            package_id: Package ID
            package_version: Package version
            project: Project ID or name
            message: Deprecation message
            
        Returns:
            Updated package version
        """
        deprecation_data = {
            "isDeprecated": True
        }
        if message:
            deprecation_data["deprecationMessage"] = message
        
        return await self.update_package_version(
            feed_id=feed_id,
            package_id=package_id,
            package_version=package_version,
            package_version_details=deprecation_data,
            project=project
        )
    
    async def get_feed_summary(
        self,
        feed_id: str,
        project: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a feed.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            
        Returns:
            Feed summary with packages, views, and permissions
        """
        # Get the feed details
        feed = await self.get_feed(feed_id=feed_id, project=project)
        
        # Get packages
        try:
            packages = await self.list_packages(feed_id=feed_id, project=project, top=100)
        except Exception:
            packages = []
        
        # Get views
        try:
            views = await self.list_feed_views(feed_id=feed_id, project=project)
        except Exception:
            views = []
        
        # Get permissions
        try:
            permissions = await self.get_feed_permissions(feed_id=feed_id, project=project)
        except Exception:
            permissions = []
        
        # Get recycle bin count
        try:
            recycle_bin_packages = await self.list_recycle_bin_packages(
                feed_id=feed_id, 
                project=project, 
                top=1
            )
            recycle_bin_count = len(recycle_bin_packages)
        except Exception:
            recycle_bin_count = 0
        
        return {
            "feed": feed,
            "packages": packages,
            "views": views,
            "permissions": permissions,
            "summary": {
                "feed_id": feed_id,
                "feed_name": feed.name,
                "package_count": len(packages),
                "view_count": len(views),
                "permission_count": len(permissions),
                "recycle_bin_count": recycle_bin_count,
                "capabilities": feed.capabilities if hasattr(feed, 'capabilities') else []
            }
        }
    
    async def iterate_packages(
        self,
        feed_id: str,
        project: Optional[str] = None,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[Package, None]:
        """
        Iterate through all packages in a feed.
        
        Args:
            feed_id: Feed ID or name
            project: Project ID or name
            page_size: Number of packages per page
            
        Yields:
            Packages one by one
        """
        async def request_func(**params):
            packages = await self.list_packages(
                feed_id=feed_id,
                project=project,
                top=page_size,
                **params,
                **kwargs
            )
            return {"value": packages, "count": len(packages)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for package in paginator.iterate_items():
            yield package
