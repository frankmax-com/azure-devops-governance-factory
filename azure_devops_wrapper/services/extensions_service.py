"""
Extensions service for Azure DevOps - Marketplace Extensions, Installations, Management, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    Extension, ExtensionManifest, ExtensionInstallation, ExtensionRequest,
    ExtensionState, ExtensionPolicy, ExtensionEvent, ExtensionData,
    ExtensionLicense, ExtensionRating, ExtensionReview, ExtensionStatistic,
    ExtensionVersion, ExtensionCategory, ExtensionPublisher
)


class ExtensionsService:
    """Service for Extensions (Marketplace) operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
        # Extensions API uses different base URLs for different operations
        self.marketplace_base_url = "https://marketplace.visualstudio.com/_apis"
        self.extensionmanagement_base_url = "https://extmgmt.dev.azure.com"
    
    async def _make_marketplace_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the Marketplace API."""
        original_base_url = self.client.base_url
        self.client.base_url = self.marketplace_base_url
        try:
            if method.upper() == "GET":
                return await self.client.get_json(endpoint, **kwargs)
            elif method.upper() == "POST":
                return await self.client.post_json(endpoint, **kwargs)
            elif method.upper() == "PATCH":
                return await self.client.patch_json(endpoint, **kwargs)
            elif method.upper() == "DELETE":
                return await self.client.delete(endpoint, **kwargs)
            elif method.upper() == "PUT":
                return await self.client.put_json(endpoint, **kwargs)
        finally:
            self.client.base_url = original_base_url
    
    async def _make_extension_mgmt_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the Extension Management API."""
        original_base_url = self.client.base_url
        self.client.base_url = self.extensionmanagement_base_url
        try:
            if method.upper() == "GET":
                return await self.client.get_json(endpoint, **kwargs)
            elif method.upper() == "POST":
                return await self.client.post_json(endpoint, **kwargs)
            elif method.upper() == "PATCH":
                return await self.client.patch_json(endpoint, **kwargs)
            elif method.upper() == "DELETE":
                return await self.client.delete(endpoint, **kwargs)
            elif method.upper() == "PUT":
                return await self.client.put_json(endpoint, **kwargs)
        finally:
            self.client.base_url = original_base_url
    
    # Marketplace Extensions Discovery
    async def search_extensions(
        self,
        search_text: Optional[str] = None,
        target: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        page_size: int = 50,
        page_number: int = 1
    ) -> List[Extension]:
        """
        Search for extensions in the marketplace.
        
        Args:
            search_text: Search query text
            target: Target platform (e.g., Microsoft.VisualStudio.Services)
            category: Extension category
            sort_by: Sort field (installs, rating, name, etc.)
            sort_order: Sort order (asc, desc)
            page_size: Number of results per page
            page_number: Page number
            
        Returns:
            List of extensions
        """
        filters = []
        if search_text:
            filters.append({
                "criteria": [{"filterType": 10, "value": search_text}]
            })
        if target:
            filters.append({
                "criteria": [{"filterType": 8, "value": target}]
            })
        if category:
            filters.append({
                "criteria": [{"filterType": 5, "value": category}]
            })
        
        query_data = {
            "filters": filters,
            "flags": 914,  # Standard flags for extension data
            "assetTypes": [],
            "sortBy": [{"sortBy": sort_by or "installs", "sortOrder": sort_order or "desc"}],
            "pageSize": page_size,
            "pageNumber": page_number
        }
        
        endpoint = "public/gallery/extensionquery"
        response_data = await self._make_marketplace_request("POST", endpoint, data=query_data)
        
        extensions = []
        if "results" in response_data and len(response_data["results"]) > 0:
            for ext_data in response_data["results"][0].get("extensions", []):
                extensions.append(Extension(**ext_data))
        
        return extensions
    
    async def get_extension_details(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> Extension:
        """
        Get detailed information about a specific extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Specific version (optional)
            
        Returns:
            Extension details
        """
        endpoint = f"public/gallery/publishers/{publisher_name}/extensions/{extension_name}"
        if version:
            endpoint += f"/{version}"
        
        response_data = await self._make_marketplace_request("GET", endpoint)
        return Extension(**response_data)
    
    async def get_extension_versions(
        self,
        publisher_name: str,
        extension_name: str
    ) -> List[ExtensionVersion]:
        """
        Get all versions of an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            
        Returns:
            List of extension versions
        """
        extension = await self.get_extension_details(publisher_name, extension_name)
        return extension.versions or []
    
    async def get_extension_manifest(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> ExtensionManifest:
        """
        Get the manifest for an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Specific version
            
        Returns:
            Extension manifest
        """
        endpoint = f"public/gallery/publishers/{publisher_name}/extensions/{extension_name}"
        if version:
            endpoint += f"/{version}"
        endpoint += "/manifest"
        
        response_data = await self._make_marketplace_request("GET", endpoint)
        return ExtensionManifest(**response_data)
    
    # Extension Installation Management
    async def list_installed_extensions(
        self,
        include_disabled: bool = True,
        include_errors: bool = True,
        include_installation_issues: bool = True
    ) -> List[ExtensionInstallation]:
        """
        List extensions installed in the organization.
        
        Args:
            include_disabled: Include disabled extensions
            include_errors: Include extensions with errors
            include_installation_issues: Include extensions with installation issues
            
        Returns:
            List of installed extensions
        """
        params = {
            "includeDisabledExtensions": include_disabled,
            "includeErrors": include_errors,
            "includeInstallationIssues": include_installation_issues
        }
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensions"
        response_data = await self.client.get_json(endpoint, params=params)
        
        installations = []
        for installation_data in response_data.get("value", []):
            installations.append(ExtensionInstallation(**installation_data))
        
        return installations
    
    async def get_installed_extension(
        self,
        publisher_name: str,
        extension_name: str
    ) -> ExtensionInstallation:
        """
        Get details about an installed extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            
        Returns:
            Installed extension details
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        response_data = await self.client.get_json(endpoint)
        return ExtensionInstallation(**response_data)
    
    async def install_extension(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> ExtensionInstallation:
        """
        Install an extension in the organization.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Specific version to install
            
        Returns:
            Installation result
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        if version:
            endpoint += f"/{version}"
        
        response_data = await self.client.post_json(endpoint, data={})
        return ExtensionInstallation(**response_data)
    
    async def uninstall_extension(
        self,
        publisher_name: str,
        extension_name: str,
        reason: Optional[str] = None
    ) -> None:
        """
        Uninstall an extension from the organization.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            reason: Reason for uninstallation
        """
        params = {}
        if reason:
            params["reason"] = reason
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        await self.client.delete(endpoint, params=params)
    
    async def update_extension(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> ExtensionInstallation:
        """
        Update an installed extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Target version
            
        Returns:
            Updated installation
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        if version:
            endpoint += f"/{version}"
        
        response_data = await self.client.patch_json(endpoint, data={})
        return ExtensionInstallation(**response_data)
    
    async def enable_extension(
        self,
        publisher_name: str,
        extension_name: str
    ) -> ExtensionInstallation:
        """
        Enable a disabled extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            
        Returns:
            Updated installation
        """
        extension_data = {"installState": {"flags": "none"}}
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        response_data = await self.client.patch_json(endpoint, data=extension_data)
        return ExtensionInstallation(**response_data)
    
    async def disable_extension(
        self,
        publisher_name: str,
        extension_name: str,
        reason: Optional[str] = None
    ) -> ExtensionInstallation:
        """
        Disable an installed extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            reason: Reason for disabling
            
        Returns:
            Updated installation
        """
        extension_data = {"installState": {"flags": "disabled"}}
        if reason:
            extension_data["installState"]["lastUpdateTime"] = datetime.utcnow().isoformat()
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}"
        response_data = await self.client.patch_json(endpoint, data=extension_data)
        return ExtensionInstallation(**response_data)
    
    # Extension Requests
    async def list_extension_requests(
        self,
        include_requests: bool = True,
        include_events: bool = False
    ) -> List[ExtensionRequest]:
        """
        List extension installation requests.
        
        Args:
            include_requests: Include pending requests
            include_events: Include request events
            
        Returns:
            List of extension requests
        """
        params = {
            "includeRequests": include_requests,
            "includeEvents": include_events
        }
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/extensionrequests"
        response_data = await self.client.get_json(endpoint, params=params)
        
        requests = []
        for request_data in response_data.get("value", []):
            requests.append(ExtensionRequest(**request_data))
        
        return requests
    
    async def create_extension_request(
        self,
        publisher_name: str,
        extension_name: str,
        justification: Optional[str] = None
    ) -> ExtensionRequest:
        """
        Create a request to install an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            justification: Justification for the request
            
        Returns:
            Created request
        """
        request_data = {
            "extensionName": extension_name,
            "publisherName": publisher_name
        }
        if justification:
            request_data["message"] = justification
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/extensionrequests"
        response_data = await self.client.post_json(endpoint, data=request_data)
        return ExtensionRequest(**response_data)
    
    async def approve_extension_request(
        self,
        request_id: str,
        message: Optional[str] = None
    ) -> ExtensionRequest:
        """
        Approve an extension installation request.
        
        Args:
            request_id: Request ID
            message: Approval message
            
        Returns:
            Updated request
        """
        request_data = {"state": "approved"}
        if message:
            request_data["message"] = message
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/extensionrequests/{request_id}"
        response_data = await self.client.patch_json(endpoint, data=request_data)
        return ExtensionRequest(**response_data)
    
    async def reject_extension_request(
        self,
        request_id: str,
        message: Optional[str] = None
    ) -> ExtensionRequest:
        """
        Reject an extension installation request.
        
        Args:
            request_id: Request ID
            message: Rejection message
            
        Returns:
            Updated request
        """
        request_data = {"state": "rejected"}
        if message:
            request_data["message"] = message
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/extensionrequests/{request_id}"
        response_data = await self.client.patch_json(endpoint, data=request_data)
        return ExtensionRequest(**response_data)
    
    # Extension Policies
    async def get_extension_policy(
        self,
        publisher_name: str,
        extension_name: str
    ) -> ExtensionPolicy:
        """
        Get policy settings for an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            
        Returns:
            Extension policy
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/policies/{publisher_name}/{extension_name}"
        response_data = await self.client.get_json(endpoint)
        return ExtensionPolicy(**response_data)
    
    async def set_extension_policy(
        self,
        publisher_name: str,
        extension_name: str,
        policy: Dict[str, Any]
    ) -> ExtensionPolicy:
        """
        Set policy for an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            policy: Policy configuration
            
        Returns:
            Updated policy
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/policies/{publisher_name}/{extension_name}"
        response_data = await self.client.put_json(endpoint, data=policy)
        return ExtensionPolicy(**response_data)
    
    # Extension Data
    async def get_extension_data(
        self,
        publisher_name: str,
        extension_name: str,
        scope: Optional[str] = None,
        collection: Optional[str] = None
    ) -> List[ExtensionData]:
        """
        Get data stored by an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            scope: Data scope
            collection: Data collection
            
        Returns:
            Extension data
        """
        params = {}
        if scope:
            params["scope"] = scope
        if collection:
            params["collection"] = collection
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}/data"
        response_data = await self.client.get_json(endpoint, params=params)
        
        data_items = []
        for data_item in response_data.get("value", []):
            data_items.append(ExtensionData(**data_item))
        
        return data_items
    
    async def set_extension_data(
        self,
        publisher_name: str,
        extension_name: str,
        scope: str,
        collection: str,
        data: Dict[str, Any]
    ) -> ExtensionData:
        """
        Set data for an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            scope: Data scope
            collection: Data collection
            data: Data to store
            
        Returns:
            Stored data
        """
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/installedextensionsbyname/{publisher_name}/{extension_name}/data/{scope}/{collection}"
        response_data = await self.client.put_json(endpoint, data=data)
        return ExtensionData(**response_data)
    
    # Extension Events and Audit
    async def get_extension_events(
        self,
        publisher_name: Optional[str] = None,
        extension_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ExtensionEvent]:
        """
        Get extension-related events.
        
        Args:
            publisher_name: Filter by publisher
            extension_name: Filter by extension
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            List of extension events
        """
        params = {}
        if publisher_name:
            params["publisherName"] = publisher_name
        if extension_name:
            params["extensionName"] = extension_name
        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
        
        endpoint = f"{self.client.organization}/_apis/extensionmanagement/events"
        response_data = await self.client.get_json(endpoint, params=params)
        
        events = []
        for event_data in response_data.get("value", []):
            events.append(ExtensionEvent(**event_data))
        
        return events
    
    # Extension Statistics
    async def get_extension_statistics(
        self,
        publisher_name: str,
        extension_name: str
    ) -> List[ExtensionStatistic]:
        """
        Get statistics for an extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            
        Returns:
            Extension statistics
        """
        endpoint = f"public/gallery/publishers/{publisher_name}/extensions/{extension_name}/stats"
        response_data = await self._make_marketplace_request("GET", endpoint)
        
        statistics = []
        for stat_data in response_data.get("statistics", []):
            statistics.append(ExtensionStatistic(**stat_data))
        
        return statistics
    
    # Utility Methods
    async def find_extension_by_name(
        self,
        name: str,
        publisher: Optional[str] = None
    ) -> Optional[Extension]:
        """
        Find an extension by name.
        
        Args:
            name: Extension name or display name
            publisher: Publisher name filter
            
        Returns:
            Extension if found
        """
        try:
            extensions = await self.search_extensions(search_text=name)
            for extension in extensions:
                if extension.extension_name == name or extension.display_name == name:
                    if not publisher or extension.publisher.publisher_name == publisher:
                        return extension
        except Exception:
            pass
        
        return None
    
    async def get_popular_extensions(
        self,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Extension]:
        """
        Get popular extensions from the marketplace.
        
        Args:
            category: Category filter
            limit: Number of extensions to return
            
        Returns:
            List of popular extensions
        """
        return await self.search_extensions(
            category=category,
            sort_by="installs",
            sort_order="desc",
            page_size=limit
        )
    
    async def get_recently_updated_extensions(
        self,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Extension]:
        """
        Get recently updated extensions.
        
        Args:
            category: Category filter
            limit: Number of extensions to return
            
        Returns:
            List of recently updated extensions
        """
        return await self.search_extensions(
            category=category,
            sort_by="lastUpdated",
            sort_order="desc",
            page_size=limit
        )
    
    async def check_extension_compatibility(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if an extension is compatible with current Azure DevOps version.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Specific version
            
        Returns:
            Compatibility information
        """
        compatibility = {
            "compatible": False,
            "extension": None,
            "issues": []
        }
        
        try:
            extension = await self.get_extension_details(publisher_name, extension_name, version)
            compatibility["extension"] = extension
            
            # Check if extension targets Azure DevOps Services
            if extension.targets:
                for target in extension.targets:
                    if "Microsoft.VisualStudio.Services" in target.get("target", ""):
                        compatibility["compatible"] = True
                        break
            
            if not compatibility["compatible"]:
                compatibility["issues"].append("Extension does not target Azure DevOps Services")
            
        except Exception as e:
            compatibility["issues"].append(f"Error checking compatibility: {str(e)}")
        
        return compatibility
    
    async def get_organization_extension_summary(self) -> Dict[str, Any]:
        """
        Get a summary of extensions in the organization.
        
        Returns:
            Extension summary
        """
        summary = {
            "installed_extensions": [],
            "pending_requests": [],
            "total_installed": 0,
            "total_pending": 0,
            "enabled_count": 0,
            "disabled_count": 0,
            "error_count": 0
        }
        
        try:
            # Get installed extensions
            installed = await self.list_installed_extensions()
            summary["installed_extensions"] = installed
            summary["total_installed"] = len(installed)
            
            for extension in installed:
                if hasattr(extension, 'install_state'):
                    if extension.install_state.flags == "none":
                        summary["enabled_count"] += 1
                    elif "disabled" in extension.install_state.flags:
                        summary["disabled_count"] += 1
                    if hasattr(extension.install_state, 'installation_issues') and extension.install_state.installation_issues:
                        summary["error_count"] += 1
            
            # Get pending requests
            requests = await self.list_extension_requests()
            pending_requests = [r for r in requests if r.state == "pending"]
            summary["pending_requests"] = pending_requests
            summary["total_pending"] = len(pending_requests)
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
    
    async def bulk_install_extensions(
        self,
        extensions: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Install multiple extensions in bulk.
        
        Args:
            extensions: List of extension dictionaries with publisher and name
            
        Returns:
            Installation results
        """
        results = []
        
        for ext in extensions:
            publisher = ext.get("publisher")
            name = ext.get("name")
            version = ext.get("version")
            
            result = {
                "publisher": publisher,
                "name": name,
                "version": version,
                "success": False,
                "error": None,
                "installation": None
            }
            
            try:
                installation = await self.install_extension(publisher, name, version)
                result["success"] = True
                result["installation"] = installation
            except Exception as e:
                result["error"] = str(e)
            
            results.append(result)
        
        return results
