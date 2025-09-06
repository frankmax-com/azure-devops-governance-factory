"""
Security service for Azure DevOps - Permissions, Access Control Lists, Security Namespaces, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    SecurityNamespace, AccessControlList, AccessControlEntry, PermissionEvaluationBatch,
    SecurityToken, IdentityDescriptor, ActionDefinition, PermissionEvaluation,
    SecurityNamespacesResponse, AccessControlListsResponse, AccessControlEntriesResponse
)


class SecurityService:
    """Service for Security and Permissions operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Security Namespaces
    async def list_security_namespaces(
        self,
        local_only: Optional[bool] = None
    ) -> List[SecurityNamespace]:
        """
        List security namespaces.
        
        Args:
            local_only: Only local namespaces
            
        Returns:
            List of security namespaces
        """
        params = {}
        if local_only:
            params['localOnly'] = local_only
        
        endpoint = "securitynamespaces"
        response_data = await self.client.get_json(endpoint, params=params)
        response = SecurityNamespacesResponse(**response_data)
        return response.value
    
    async def get_security_namespace(
        self,
        namespace_id: str,
        local_only: Optional[bool] = None
    ) -> SecurityNamespace:
        """
        Get a specific security namespace.
        
        Args:
            namespace_id: Security namespace ID
            local_only: Only local namespace
            
        Returns:
            Security namespace details
        """
        params = {}
        if local_only:
            params['localOnly'] = local_only
        
        endpoint = f"securitynamespaces/{namespace_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return SecurityNamespace(**response_data)
    
    # Access Control Lists (ACLs)
    async def query_access_control_lists(
        self,
        security_namespace_id: str,
        token: Optional[str] = None,
        descriptors: Optional[List[str]] = None,
        include_extended_info: Optional[bool] = None,
        recurse: Optional[bool] = None
    ) -> List[AccessControlList]:
        """
        Query access control lists.
        
        Args:
            security_namespace_id: Security namespace ID
            token: Security token
            descriptors: Identity descriptors
            include_extended_info: Include extended information
            recurse: Recurse through hierarchy
            
        Returns:
            List of access control lists
        """
        params = {}
        if token:
            params['token'] = token
        if descriptors:
            params['descriptors'] = ','.join(descriptors)
        if include_extended_info:
            params['includeExtendedInfo'] = include_extended_info
        if recurse:
            params['recurse'] = recurse
        
        endpoint = f"accesscontrollists/{security_namespace_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        response = AccessControlListsResponse(**response_data)
        return response.value
    
    async def set_access_control_lists(
        self,
        security_namespace_id: str,
        access_control_lists: List[Dict[str, Any]]
    ) -> None:
        """
        Set access control lists.
        
        Args:
            security_namespace_id: Security namespace ID
            access_control_lists: List of ACL data
        """
        endpoint = f"accesscontrollists/{security_namespace_id}"
        await self.client.post_json(endpoint, data=access_control_lists)
    
    async def remove_access_control_lists(
        self,
        security_namespace_id: str,
        tokens: Optional[str] = None,
        descriptors: Optional[str] = None
    ) -> bool:
        """
        Remove access control lists.
        
        Args:
            security_namespace_id: Security namespace ID
            tokens: Security tokens to remove
            descriptors: Identity descriptors to remove
            
        Returns:
            Success status
        """
        params = {}
        if tokens:
            params['tokens'] = tokens
        if descriptors:
            params['descriptors'] = descriptors
        
        endpoint = f"accesscontrollists/{security_namespace_id}"
        response_data = await self.client.delete_json(endpoint, params=params)
        return response_data.get('value', False)
    
    # Access Control Entries (ACEs)
    async def query_access_control_entries(
        self,
        security_namespace_id: str,
        token: Optional[str] = None,
        descriptors: Optional[List[str]] = None
    ) -> List[AccessControlEntry]:
        """
        Query access control entries.
        
        Args:
            security_namespace_id: Security namespace ID
            token: Security token
            descriptors: Identity descriptors
            
        Returns:
            List of access control entries
        """
        params = {}
        if token:
            params['token'] = token
        if descriptors:
            params['descriptors'] = ','.join(descriptors)
        
        endpoint = f"accesscontrolentries/{security_namespace_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        response = AccessControlEntriesResponse(**response_data)
        return response.value
    
    async def set_access_control_entries(
        self,
        security_namespace_id: str,
        access_control_entries: List[Dict[str, Any]]
    ) -> List[AccessControlEntry]:
        """
        Set access control entries.
        
        Args:
            security_namespace_id: Security namespace ID
            access_control_entries: List of ACE data
            
        Returns:
            List of updated access control entries
        """
        endpoint = f"accesscontrolentries/{security_namespace_id}"
        response_data = await self.client.post_json(endpoint, data=access_control_entries)
        return [AccessControlEntry(**ace) for ace in response_data.get('value', [])]
    
    async def remove_access_control_entries(
        self,
        security_namespace_id: str,
        tokens: Optional[str] = None,
        descriptors: Optional[str] = None
    ) -> bool:
        """
        Remove access control entries.
        
        Args:
            security_namespace_id: Security namespace ID
            tokens: Security tokens to remove
            descriptors: Identity descriptors to remove
            
        Returns:
            Success status
        """
        params = {}
        if tokens:
            params['tokens'] = tokens
        if descriptors:
            params['descriptors'] = descriptors
        
        endpoint = f"accesscontrolentries/{security_namespace_id}"
        response_data = await self.client.delete_json(endpoint, params=params)
        return response_data.get('value', False)
    
    # Permission Evaluation
    async def has_permissions(
        self,
        security_namespace_id: str,
        permissions: int,
        tokens: Optional[str] = None,
        always_allow_administrators: Optional[bool] = None,
        delay_bind: Optional[bool] = None
    ) -> List[bool]:
        """
        Check if the current user has specific permissions.
        
        Args:
            security_namespace_id: Security namespace ID
            permissions: Permission bits to check
            tokens: Security tokens
            always_allow_administrators: Always allow administrators
            delay_bind: Delay bind
            
        Returns:
            List of permission results
        """
        params = {
            'permissions': permissions
        }
        if tokens:
            params['tokens'] = tokens
        if always_allow_administrators:
            params['alwaysAllowAdministrators'] = always_allow_administrators
        if delay_bind:
            params['delayBind'] = delay_bind
        
        endpoint = f"permissions/{security_namespace_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return response_data.get('value', [])
    
    async def has_permissions_batch(
        self,
        evaluation_batch: Dict[str, Any]
    ) -> List[PermissionEvaluation]:
        """
        Check permissions for multiple subjects and tokens in batch.
        
        Args:
            evaluation_batch: Batch evaluation request
            
        Returns:
            List of permission evaluations
        """
        endpoint = "permissions"
        response_data = await self.client.post_json(endpoint, data=evaluation_batch)
        evaluations = response_data.get('evaluations', [])
        return [PermissionEvaluation(**evaluation) for evaluation in evaluations]
    
    async def remove_permission(
        self,
        security_namespace_id: str,
        permissions: int,
        tokens: Optional[str] = None,
        descriptor: Optional[str] = None
    ) -> bool:
        """
        Remove permissions for a security token.
        
        Args:
            security_namespace_id: Security namespace ID
            permissions: Permission bits to remove
            tokens: Security tokens
            descriptor: Identity descriptor
            
        Returns:
            Success status
        """
        params = {
            'permissions': permissions
        }
        if tokens:
            params['tokens'] = tokens
        if descriptor:
            params['descriptor'] = descriptor
        
        endpoint = f"permissions/{security_namespace_id}"
        response_data = await self.client.delete_json(endpoint, params=params)
        return response_data.get('value', False)
    
    # Project-level security methods
    async def get_project_security_namespace(
        self,
        project: str
    ) -> Optional[SecurityNamespace]:
        """
        Get the project-level security namespace.
        
        Args:
            project: Project ID or name
            
        Returns:
            Project security namespace or None
        """
        namespaces = await self.list_security_namespaces()
        for namespace in namespaces:
            if namespace.name == "Project" or "Project" in namespace.display_name:
                return namespace
        return None
    
    async def get_project_permissions(
        self,
        project: str,
        subject_descriptor: str
    ) -> List[AccessControlEntry]:
        """
        Get permissions for a subject in a project.
        
        Args:
            project: Project ID or name
            subject_descriptor: Subject identity descriptor
            
        Returns:
            List of access control entries
        """
        # Get project security namespace
        namespace = await self.get_project_security_namespace(project)
        if not namespace:
            return []
        
        # Project token format is typically: $PROJECT:vstfs:///Classification/TeamProject/{project-id}
        project_token = f"$PROJECT:vstfs:///Classification/TeamProject/{project}"
        
        return await self.query_access_control_entries(
            security_namespace_id=namespace.namespace_id,
            token=project_token,
            descriptors=[subject_descriptor]
        )
    
    async def grant_project_permission(
        self,
        project: str,
        subject_descriptor: str,
        permission_bit: int,
        allow: bool = True
    ) -> bool:
        """
        Grant or deny a project permission to a subject.
        
        Args:
            project: Project ID or name
            subject_descriptor: Subject identity descriptor
            permission_bit: Permission bit to grant/deny
            allow: True to allow, False to deny
            
        Returns:
            Success status
        """
        namespace = await self.get_project_security_namespace(project)
        if not namespace:
            return False
        
        project_token = f"$PROJECT:vstfs:///Classification/TeamProject/{project}"
        
        ace_data = {
            "token": project_token,
            "merge": True,
            "accessControlEntries": [{
                "descriptor": subject_descriptor,
                "allow": permission_bit if allow else 0,
                "deny": 0 if allow else permission_bit
            }]
        }
        
        try:
            await self.set_access_control_lists(
                security_namespace_id=namespace.namespace_id,
                access_control_lists=[ace_data]
            )
            return True
        except Exception:
            return False
    
    # Repository-level security methods
    async def get_repository_security_namespace(self) -> Optional[SecurityNamespace]:
        """
        Get the Git repository security namespace.
        
        Returns:
            Repository security namespace or None
        """
        namespaces = await self.list_security_namespaces()
        for namespace in namespaces:
            if "Git Repositories" in namespace.display_name or namespace.name == "Git Repositories":
                return namespace
        return None
    
    async def get_repository_permissions(
        self,
        project: str,
        repository_id: str,
        subject_descriptor: str,
        branch_name: Optional[str] = None
    ) -> List[AccessControlEntry]:
        """
        Get permissions for a subject on a repository.
        
        Args:
            project: Project ID or name
            repository_id: Repository ID
            subject_descriptor: Subject identity descriptor
            branch_name: Specific branch name (optional)
            
        Returns:
            List of access control entries
        """
        namespace = await self.get_repository_security_namespace()
        if not namespace:
            return []
        
        # Repository token format
        if branch_name:
            repo_token = f"repoV2/{project}/{repository_id}/refs/heads/{branch_name}"
        else:
            repo_token = f"repoV2/{project}/{repository_id}"
        
        return await self.query_access_control_entries(
            security_namespace_id=namespace.namespace_id,
            token=repo_token,
            descriptors=[subject_descriptor]
        )
    
    async def grant_repository_permission(
        self,
        project: str,
        repository_id: str,
        subject_descriptor: str,
        permission_bit: int,
        allow: bool = True,
        branch_name: Optional[str] = None
    ) -> bool:
        """
        Grant or deny a repository permission to a subject.
        
        Args:
            project: Project ID or name
            repository_id: Repository ID
            subject_descriptor: Subject identity descriptor
            permission_bit: Permission bit to grant/deny
            allow: True to allow, False to deny
            branch_name: Specific branch name (optional)
            
        Returns:
            Success status
        """
        namespace = await self.get_repository_security_namespace()
        if not namespace:
            return False
        
        if branch_name:
            repo_token = f"repoV2/{project}/{repository_id}/refs/heads/{branch_name}"
        else:
            repo_token = f"repoV2/{project}/{repository_id}"
        
        ace_data = {
            "token": repo_token,
            "merge": True,
            "accessControlEntries": [{
                "descriptor": subject_descriptor,
                "allow": permission_bit if allow else 0,
                "deny": 0 if allow else permission_bit
            }]
        }
        
        try:
            await self.set_access_control_lists(
                security_namespace_id=namespace.namespace_id,
                access_control_lists=[ace_data]
            )
            return True
        except Exception:
            return False
    
    # Build pipeline security methods
    async def get_build_security_namespace(self) -> Optional[SecurityNamespace]:
        """
        Get the build pipeline security namespace.
        
        Returns:
            Build security namespace or None
        """
        namespaces = await self.list_security_namespaces()
        for namespace in namespaces:
            if "Build" in namespace.display_name or namespace.name == "Build":
                return namespace
        return None
    
    async def get_build_definition_permissions(
        self,
        project: str,
        definition_id: str,
        subject_descriptor: str
    ) -> List[AccessControlEntry]:
        """
        Get permissions for a subject on a build definition.
        
        Args:
            project: Project ID or name
            definition_id: Build definition ID
            subject_descriptor: Subject identity descriptor
            
        Returns:
            List of access control entries
        """
        namespace = await self.get_build_security_namespace()
        if not namespace:
            return []
        
        # Build definition token format
        build_token = f"{project}/{definition_id}"
        
        return await self.query_access_control_entries(
            security_namespace_id=namespace.namespace_id,
            token=build_token,
            descriptors=[subject_descriptor]
        )
    
    async def grant_build_definition_permission(
        self,
        project: str,
        definition_id: str,
        subject_descriptor: str,
        permission_bit: int,
        allow: bool = True
    ) -> bool:
        """
        Grant or deny a build definition permission to a subject.
        
        Args:
            project: Project ID or name
            definition_id: Build definition ID
            subject_descriptor: Subject identity descriptor
            permission_bit: Permission bit to grant/deny
            allow: True to allow, False to deny
            
        Returns:
            Success status
        """
        namespace = await self.get_build_security_namespace()
        if not namespace:
            return False
        
        build_token = f"{project}/{definition_id}"
        
        ace_data = {
            "token": build_token,
            "merge": True,
            "accessControlEntries": [{
                "descriptor": subject_descriptor,
                "allow": permission_bit if allow else 0,
                "deny": 0 if allow else permission_bit
            }]
        }
        
        try:
            await self.set_access_control_lists(
                security_namespace_id=namespace.namespace_id,
                access_control_lists=[ace_data]
            )
            return True
        except Exception:
            return False
    
    # Utility methods
    async def get_effective_permissions(
        self,
        security_namespace_id: str,
        token: str,
        subject_descriptor: str
    ) -> Dict[str, Any]:
        """
        Get effective permissions for a subject on a token.
        
        Args:
            security_namespace_id: Security namespace ID
            token: Security token
            subject_descriptor: Subject identity descriptor
            
        Returns:
            Effective permissions summary
        """
        # Get ACEs for the subject
        aces = await self.query_access_control_entries(
            security_namespace_id=security_namespace_id,
            token=token,
            descriptors=[subject_descriptor]
        )
        
        # Get the security namespace for permission definitions
        namespace = await self.get_security_namespace(security_namespace_id)
        
        effective_permissions = {
            "subject": subject_descriptor,
            "token": token,
            "namespace": namespace.display_name if namespace else "Unknown",
            "permissions": {},
            "allow_bits": 0,
            "deny_bits": 0
        }
        
        if aces:
            ace = aces[0]  # Take the first ACE
            effective_permissions["allow_bits"] = ace.allow
            effective_permissions["deny_bits"] = ace.deny
            
            # Map permission bits to action names if namespace has actions
            if namespace and namespace.actions:
                for action in namespace.actions:
                    permission_name = action.display_name or action.name
                    bit_value = action.bit
                    
                    if ace.allow & bit_value:
                        effective_permissions["permissions"][permission_name] = "Allow"
                    elif ace.deny & bit_value:
                        effective_permissions["permissions"][permission_name] = "Deny"
                    else:
                        effective_permissions["permissions"][permission_name] = "Not Set"
        
        return effective_permissions
    
    async def check_user_permission(
        self,
        security_namespace_id: str,
        token: str,
        permission_bit: int,
        subject_descriptor: Optional[str] = None
    ) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            security_namespace_id: Security namespace ID
            token: Security token
            permission_bit: Permission bit to check
            subject_descriptor: Subject descriptor (current user if None)
            
        Returns:
            True if user has permission
        """
        try:
            permissions = await self.has_permissions(
                security_namespace_id=security_namespace_id,
                permissions=permission_bit,
                tokens=token
            )
            return permissions[0] if permissions else False
        except Exception:
            return False
    
    async def get_security_summary(
        self,
        project: str,
        subject_descriptor: str
    ) -> Dict[str, Any]:
        """
        Get a comprehensive security summary for a subject in a project.
        
        Args:
            project: Project ID or name
            subject_descriptor: Subject identity descriptor
            
        Returns:
            Security summary with permissions across namespaces
        """
        summary = {
            "subject": subject_descriptor,
            "project": project,
            "permissions": {},
            "namespace_count": 0
        }
        
        # Get all security namespaces
        namespaces = await self.list_security_namespaces()
        summary["namespace_count"] = len(namespaces)
        
        # Check key namespaces
        key_namespaces = [
            ("Project", f"$PROJECT:vstfs:///Classification/TeamProject/{project}"),
            ("Git Repositories", f"repoV2/{project}"),
            ("Build", project),
            ("ReleaseManagement", project)
        ]
        
        for namespace_name, token in key_namespaces:
            # Find the namespace
            namespace = None
            for ns in namespaces:
                if namespace_name in ns.display_name or ns.name == namespace_name:
                    namespace = ns
                    break
            
            if namespace:
                try:
                    effective_perms = await self.get_effective_permissions(
                        security_namespace_id=namespace.namespace_id,
                        token=token,
                        subject_descriptor=subject_descriptor
                    )
                    summary["permissions"][namespace_name] = effective_perms
                except Exception:
                    summary["permissions"][namespace_name] = {"error": "Could not retrieve permissions"}
        
        return summary
    
    async def copy_permissions(
        self,
        security_namespace_id: str,
        source_token: str,
        target_token: str,
        subject_descriptor: str
    ) -> bool:
        """
        Copy permissions from one token to another for a subject.
        
        Args:
            security_namespace_id: Security namespace ID
            source_token: Source security token
            target_token: Target security token
            subject_descriptor: Subject identity descriptor
            
        Returns:
            Success status
        """
        try:
            # Get source permissions
            source_aces = await self.query_access_control_entries(
                security_namespace_id=security_namespace_id,
                token=source_token,
                descriptors=[subject_descriptor]
            )
            
            if not source_aces:
                return True  # Nothing to copy
            
            source_ace = source_aces[0]
            
            # Set permissions on target token
            ace_data = {
                "token": target_token,
                "merge": True,
                "accessControlEntries": [{
                    "descriptor": subject_descriptor,
                    "allow": source_ace.allow,
                    "deny": source_ace.deny
                }]
            }
            
            await self.set_access_control_lists(
                security_namespace_id=security_namespace_id,
                access_control_lists=[ace_data]
            )
            
            return True
        except Exception:
            return False
