"""
Graph service for Azure DevOps - Users, Groups, Memberships, Identity Management, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    GraphUser, GraphGroup, GraphMember, GraphMembership, GraphDescriptor,
    GraphSubject, GraphScope, GraphServicePrincipal, GraphProviderInfo,
    GraphUsersResponse, GraphGroupsResponse, GraphMembersResponse,
    GraphMembershipsResponse, GraphSubjectsResponse
)


class GraphService:
    """Service for Graph (Identity) operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
        # Graph API uses a different base URL
        self.graph_base_url = "https://vssps.dev.azure.com"
    
    async def _make_graph_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the Graph API."""
        # Temporarily switch to graph API base URL
        original_base_url = self.client.base_url
        self.client.base_url = self.graph_base_url
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
            # Restore original base URL
            self.client.base_url = original_base_url
    
    # Users
    async def list_users(
        self,
        scope_descriptor: Optional[str] = None,
        subject_types: Optional[List[str]] = None,
        continuation_token: Optional[str] = None
    ) -> List[GraphUser]:
        """
        List users in the organization or scope.
        
        Args:
            scope_descriptor: Scope descriptor to filter users
            subject_types: Subject types filter
            continuation_token: Continuation token for pagination
            
        Returns:
            List of users
        """
        params = {}
        if scope_descriptor:
            params['scopeDescriptor'] = scope_descriptor
        if subject_types:
            params['subjectTypes'] = ','.join(subject_types)
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = "graph/users"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        response = GraphUsersResponse(**response_data)
        return response.value
    
    async def get_user(
        self,
        user_descriptor: str
    ) -> GraphUser:
        """
        Get a specific user.
        
        Args:
            user_descriptor: User descriptor
            
        Returns:
            User details
        """
        endpoint = f"graph/users/{user_descriptor}"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphUser(**response_data)
    
    async def create_user(
        self,
        creation_context: Dict[str, Any]
    ) -> GraphUser:
        """
        Create a new user.
        
        Args:
            creation_context: User creation context
            
        Returns:
            Created user
        """
        endpoint = "graph/users"
        response_data = await self._make_graph_request("POST", endpoint, data=creation_context)
        return GraphUser(**response_data)
    
    async def update_user(
        self,
        user_descriptor: str,
        user_update_data: Dict[str, Any]
    ) -> GraphUser:
        """
        Update a user.
        
        Args:
            user_descriptor: User descriptor
            user_update_data: User update data
            
        Returns:
            Updated user
        """
        endpoint = f"graph/users/{user_descriptor}"
        response_data = await self._make_graph_request("PATCH", endpoint, data=user_update_data)
        return GraphUser(**response_data)
    
    async def delete_user(
        self,
        user_descriptor: str
    ) -> None:
        """
        Delete a user.
        
        Args:
            user_descriptor: User descriptor
        """
        endpoint = f"graph/users/{user_descriptor}"
        await self._make_graph_request("DELETE", endpoint)
    
    # Groups
    async def list_groups(
        self,
        scope_descriptor: Optional[str] = None,
        subject_types: Optional[List[str]] = None,
        continuation_token: Optional[str] = None
    ) -> List[GraphGroup]:
        """
        List groups in the organization or scope.
        
        Args:
            scope_descriptor: Scope descriptor to filter groups
            subject_types: Subject types filter
            continuation_token: Continuation token for pagination
            
        Returns:
            List of groups
        """
        params = {}
        if scope_descriptor:
            params['scopeDescriptor'] = scope_descriptor
        if subject_types:
            params['subjectTypes'] = ','.join(subject_types)
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = "graph/groups"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        response = GraphGroupsResponse(**response_data)
        return response.value
    
    async def get_group(
        self,
        group_descriptor: str
    ) -> GraphGroup:
        """
        Get a specific group.
        
        Args:
            group_descriptor: Group descriptor
            
        Returns:
            Group details
        """
        endpoint = f"graph/groups/{group_descriptor}"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphGroup(**response_data)
    
    async def create_group(
        self,
        creation_context: Dict[str, Any]
    ) -> GraphGroup:
        """
        Create a new group.
        
        Args:
            creation_context: Group creation context
            
        Returns:
            Created group
        """
        endpoint = "graph/groups"
        response_data = await self._make_graph_request("POST", endpoint, data=creation_context)
        return GraphGroup(**response_data)
    
    async def update_group(
        self,
        group_descriptor: str,
        group_update_data: Dict[str, Any]
    ) -> GraphGroup:
        """
        Update a group.
        
        Args:
            group_descriptor: Group descriptor
            group_update_data: Group update data
            
        Returns:
            Updated group
        """
        endpoint = f"graph/groups/{group_descriptor}"
        response_data = await self._make_graph_request("PATCH", endpoint, data=group_update_data)
        return GraphGroup(**response_data)
    
    async def delete_group(
        self,
        group_descriptor: str
    ) -> None:
        """
        Delete a group.
        
        Args:
            group_descriptor: Group descriptor
        """
        endpoint = f"graph/groups/{group_descriptor}"
        await self._make_graph_request("DELETE", endpoint)
    
    # Memberships
    async def list_memberships(
        self,
        subject_descriptor: str,
        direction: Optional[str] = None,
        depth: Optional[int] = None
    ) -> List[GraphMembership]:
        """
        List memberships for a subject.
        
        Args:
            subject_descriptor: Subject descriptor
            direction: Direction (up, down)
            depth: Depth of traversal
            
        Returns:
            List of memberships
        """
        params = {}
        if direction:
            params['direction'] = direction
        if depth:
            params['depth'] = depth
        
        endpoint = f"graph/memberships/{subject_descriptor}"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        response = GraphMembershipsResponse(**response_data)
        return response.value
    
    async def add_membership(
        self,
        subject_descriptor: str,
        container_descriptor: str
    ) -> GraphMembership:
        """
        Add a subject to a container (group).
        
        Args:
            subject_descriptor: Subject to add
            container_descriptor: Container (group) to add to
            
        Returns:
            Created membership
        """
        endpoint = f"graph/memberships/{subject_descriptor}/{container_descriptor}"
        response_data = await self._make_graph_request("PUT", endpoint, data={})
        return GraphMembership(**response_data)
    
    async def remove_membership(
        self,
        subject_descriptor: str,
        container_descriptor: str
    ) -> None:
        """
        Remove a subject from a container (group).
        
        Args:
            subject_descriptor: Subject to remove
            container_descriptor: Container (group) to remove from
        """
        endpoint = f"graph/memberships/{subject_descriptor}/{container_descriptor}"
        await self._make_graph_request("DELETE", endpoint)
    
    async def check_membership_existence(
        self,
        subject_descriptor: str,
        container_descriptor: str
    ) -> bool:
        """
        Check if a membership exists.
        
        Args:
            subject_descriptor: Subject descriptor
            container_descriptor: Container descriptor
            
        Returns:
            True if membership exists
        """
        endpoint = f"graph/memberships/{subject_descriptor}/{container_descriptor}"
        try:
            await self._make_graph_request("GET", endpoint)
            return True
        except Exception:
            return False
    
    # Members
    async def list_group_members(
        self,
        group_descriptor: str,
        direction: Optional[str] = None,
        depth: Optional[int] = None
    ) -> List[GraphMember]:
        """
        List members of a group.
        
        Args:
            group_descriptor: Group descriptor
            direction: Direction (up, down)
            depth: Depth of traversal
            
        Returns:
            List of group members
        """
        params = {}
        if direction:
            params['direction'] = direction
        if depth:
            params['depth'] = depth
        
        endpoint = f"graph/groups/{group_descriptor}/members"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        response = GraphMembersResponse(**response_data)
        return response.value
    
    # Service Principals
    async def list_service_principals(
        self,
        continuation_token: Optional[str] = None
    ) -> List[GraphServicePrincipal]:
        """
        List service principals.
        
        Args:
            continuation_token: Continuation token for pagination
            
        Returns:
            List of service principals
        """
        params = {}
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = "graph/serviceprincipals"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        service_principals = response_data.get('value', [])
        return [GraphServicePrincipal(**sp) for sp in service_principals]
    
    async def get_service_principal(
        self,
        service_principal_descriptor: str
    ) -> GraphServicePrincipal:
        """
        Get a specific service principal.
        
        Args:
            service_principal_descriptor: Service principal descriptor
            
        Returns:
            Service principal details
        """
        endpoint = f"graph/serviceprincipals/{service_principal_descriptor}"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphServicePrincipal(**response_data)
    
    async def create_service_principal(
        self,
        creation_context: Dict[str, Any]
    ) -> GraphServicePrincipal:
        """
        Create a service principal.
        
        Args:
            creation_context: Service principal creation context
            
        Returns:
            Created service principal
        """
        endpoint = "graph/serviceprincipals"
        response_data = await self._make_graph_request("POST", endpoint, data=creation_context)
        return GraphServicePrincipal(**response_data)
    
    # Subjects (unified users/groups/service principals)
    async def lookup_subjects(
        self,
        lookup_keys: List[Dict[str, str]]
    ) -> List[GraphSubject]:
        """
        Lookup subjects by various keys.
        
        Args:
            lookup_keys: List of lookup key dictionaries
            
        Returns:
            List of found subjects
        """
        lookup_data = {"lookupKeys": lookup_keys}
        endpoint = "graph/subjectlookup"
        response_data = await self._make_graph_request("POST", endpoint, data=lookup_data)
        response = GraphSubjectsResponse(**response_data)
        return response.value
    
    async def resolve_subject_by_descriptor(
        self,
        subject_descriptor: str
    ) -> GraphSubject:
        """
        Resolve a subject by descriptor.
        
        Args:
            subject_descriptor: Subject descriptor
            
        Returns:
            Resolved subject
        """
        endpoint = f"graph/subjects/{subject_descriptor}"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphSubject(**response_data)
    
    async def query_subjects(
        self,
        query: str,
        subject_kind: Optional[List[str]] = None
    ) -> List[GraphSubject]:
        """
        Query subjects by search terms.
        
        Args:
            query: Search query
            subject_kind: Subject kinds to search
            
        Returns:
            List of matching subjects
        """
        params = {"query": query}
        if subject_kind:
            params['subjectKind'] = ','.join(subject_kind)
        
        endpoint = "graph/subjectquery"
        response_data = await self._make_graph_request("GET", endpoint, params=params)
        subjects = response_data.get('value', [])
        return [GraphSubject(**subject) for subject in subjects]
    
    # Descriptors
    async def get_descriptor(
        self,
        storage_key: str
    ) -> GraphDescriptor:
        """
        Get a descriptor by storage key.
        
        Args:
            storage_key: Storage key
            
        Returns:
            Graph descriptor
        """
        endpoint = f"graph/descriptors/{storage_key}"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphDescriptor(**response_data)
    
    # Provider Info
    async def get_provider_info(
        self,
        user_descriptor: str
    ) -> GraphProviderInfo:
        """
        Get provider information for a user.
        
        Args:
            user_descriptor: User descriptor
            
        Returns:
            Provider information
        """
        endpoint = f"graph/users/{user_descriptor}/providerinfo"
        response_data = await self._make_graph_request("GET", endpoint)
        return GraphProviderInfo(**response_data)
    
    # Utility methods
    async def find_user_by_email(
        self,
        email: str
    ) -> Optional[GraphUser]:
        """
        Find a user by email address.
        
        Args:
            email: Email address
            
        Returns:
            User if found, None otherwise
        """
        lookup_keys = [{"descriptor": f"msa.{email}"}]
        try:
            subjects = await self.lookup_subjects(lookup_keys)
            for subject in subjects:
                if subject.subject_kind == "user":
                    # Convert subject to user
                    user_data = subject.dict()
                    return GraphUser(**user_data)
        except Exception:
            pass
        
        # Fallback to query
        try:
            subjects = await self.query_subjects(query=email, subject_kind=["user"])
            for subject in subjects:
                if hasattr(subject, 'mail_address') and subject.mail_address == email:
                    user_data = subject.dict()
                    return GraphUser(**user_data)
        except Exception:
            pass
        
        return None
    
    async def find_group_by_name(
        self,
        group_name: str,
        scope_descriptor: Optional[str] = None
    ) -> Optional[GraphGroup]:
        """
        Find a group by name.
        
        Args:
            group_name: Group name
            scope_descriptor: Scope to search in
            
        Returns:
            Group if found, None otherwise
        """
        try:
            groups = await self.list_groups(scope_descriptor=scope_descriptor)
            for group in groups:
                if group.display_name == group_name or group.principal_name == group_name:
                    return group
        except Exception:
            pass
        
        return None
    
    async def get_user_groups(
        self,
        user_descriptor: str
    ) -> List[GraphGroup]:
        """
        Get all groups that a user is a member of.
        
        Args:
            user_descriptor: User descriptor
            
        Returns:
            List of groups
        """
        try:
            memberships = await self.list_memberships(
                subject_descriptor=user_descriptor,
                direction="up"
            )
            
            groups = []
            for membership in memberships:
                if membership.container_descriptor:
                    try:
                        # Try to get as group
                        group = await self.get_group(membership.container_descriptor)
                        groups.append(group)
                    except Exception:
                        # Might not be a group
                        continue
            
            return groups
        except Exception:
            return []
    
    async def get_group_users(
        self,
        group_descriptor: str,
        recursive: bool = False
    ) -> List[GraphUser]:
        """
        Get all users in a group.
        
        Args:
            group_descriptor: Group descriptor
            recursive: Include users from nested groups
            
        Returns:
            List of users
        """
        try:
            depth = None if not recursive else 10  # Reasonable recursion limit
            members = await self.list_group_members(
                group_descriptor=group_descriptor,
                direction="down",
                depth=depth
            )
            
            users = []
            for member in members:
                if member.member_descriptor:
                    try:
                        # Try to get as user
                        user = await self.get_user(member.member_descriptor)
                        users.append(user)
                    except Exception:
                        # Might not be a user
                        continue
            
            return users
        except Exception:
            return []
    
    async def add_user_to_group(
        self,
        user_descriptor: str,
        group_descriptor: str
    ) -> bool:
        """
        Add a user to a group.
        
        Args:
            user_descriptor: User descriptor
            group_descriptor: Group descriptor
            
        Returns:
            Success status
        """
        try:
            await self.add_membership(
                subject_descriptor=user_descriptor,
                container_descriptor=group_descriptor
            )
            return True
        except Exception:
            return False
    
    async def remove_user_from_group(
        self,
        user_descriptor: str,
        group_descriptor: str
    ) -> bool:
        """
        Remove a user from a group.
        
        Args:
            user_descriptor: User descriptor
            group_descriptor: Group descriptor
            
        Returns:
            Success status
        """
        try:
            await self.remove_membership(
                subject_descriptor=user_descriptor,
                container_descriptor=group_descriptor
            )
            return True
        except Exception:
            return False
    
    async def get_organization_members(
        self,
        include_service_principals: bool = False
    ) -> Dict[str, Any]:
        """
        Get all members of the organization.
        
        Args:
            include_service_principals: Include service principals
            
        Returns:
            Organization members summary
        """
        summary = {
            "users": [],
            "groups": [],
            "service_principals": [],
            "total_count": 0
        }
        
        try:
            # Get users
            users = await self.list_users()
            summary["users"] = users
            
            # Get groups
            groups = await self.list_groups()
            summary["groups"] = groups
            
            # Get service principals if requested
            if include_service_principals:
                service_principals = await self.list_service_principals()
                summary["service_principals"] = service_principals
            
            summary["total_count"] = len(users) + len(groups) + len(summary["service_principals"])
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
    
    async def get_subject_permissions_summary(
        self,
        subject_descriptor: str
    ) -> Dict[str, Any]:
        """
        Get a summary of a subject's group memberships and permissions.
        
        Args:
            subject_descriptor: Subject descriptor
            
        Returns:
            Permissions summary
        """
        summary = {
            "subject_descriptor": subject_descriptor,
            "subject_type": "unknown",
            "group_memberships": [],
            "direct_groups": [],
            "nested_groups": []
        }
        
        try:
            # Resolve the subject
            subject = await self.resolve_subject_by_descriptor(subject_descriptor)
            summary["subject_type"] = subject.subject_kind
            summary["display_name"] = getattr(subject, 'display_name', 'Unknown')
            
            # Get memberships
            memberships = await self.list_memberships(
                subject_descriptor=subject_descriptor,
                direction="up"
            )
            
            summary["group_memberships"] = memberships
            
            # Separate direct and nested groups
            for membership in memberships:
                if membership.container_descriptor:
                    try:
                        group = await self.get_group(membership.container_descriptor)
                        if hasattr(membership, 'via') and membership.via:
                            summary["nested_groups"].append(group)
                        else:
                            summary["direct_groups"].append(group)
                    except Exception:
                        continue
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
