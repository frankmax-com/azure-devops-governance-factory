"""
Work Items service for Azure DevOps - Work Items, Queries, Fields, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    WorkItem, WorkItemField, WorkItemType, WorkItemTemplate, WorkItemQuery,
    WorkItemQueryResult, WorkItemComment, WorkItemUpdate, WorkItemRelation,
    WorkItemsResponse, WorkItemTypesResponse, WorkItemFieldsResponse,
    WorkItemQueriesResponse, WorkItemCommentsResponse
)


class WorkItemsService:
    """Service for Work Items operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Work Items
    async def get_work_item(
        self,
        work_item_id: int,
        project: Optional[str] = None,
        fields: Optional[List[str]] = None,
        as_of: Optional[datetime] = None,
        expand: Optional[str] = None
    ) -> WorkItem:
        """
        Get a work item.
        
        Args:
            work_item_id: Work item ID
            project: Project ID or name
            fields: Specific fields to retrieve
            as_of: Point in time to retrieve work item
            expand: Expand options (relations, fields, links, all)
            
        Returns:
            Work item details
        """
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        if as_of:
            params['asOf'] = as_of.isoformat()
        if expand:
            params['$expand'] = expand
        
        endpoint = f"wit/workitems/{work_item_id}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}"
        
        response_data = await self.client.get_json(endpoint, params=params)
        return WorkItem(**response_data)
    
    async def get_work_items(
        self,
        work_item_ids: List[int],
        project: Optional[str] = None,
        fields: Optional[List[str]] = None,
        as_of: Optional[datetime] = None,
        expand: Optional[str] = None,
        error_policy: Optional[str] = None
    ) -> List[WorkItem]:
        """
        Get multiple work items.
        
        Args:
            work_item_ids: List of work item IDs
            project: Project ID or name
            fields: Specific fields to retrieve
            as_of: Point in time to retrieve work items
            expand: Expand options
            error_policy: Error policy (fail, omit)
            
        Returns:
            List of work items
        """
        params = {
            'ids': ','.join(map(str, work_item_ids))
        }
        if fields:
            params['fields'] = ','.join(fields)
        if as_of:
            params['asOf'] = as_of.isoformat()
        if expand:
            params['$expand'] = expand
        if error_policy:
            params['errorPolicy'] = error_policy
        
        endpoint = "wit/workitems"
        if project:
            endpoint = f"projects/{project}/wit/workitems"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = WorkItemsResponse(**response_data)
        return response.value
    
    async def create_work_item(
        self,
        work_item_type: str,
        fields: Dict[str, Any],
        project: Optional[str] = None,
        validate_only: Optional[bool] = None,
        bypass_rules: Optional[bool] = None,
        suppress_notifications: Optional[bool] = None,
        expand: Optional[str] = None
    ) -> WorkItem:
        """
        Create a new work item.
        
        Args:
            work_item_type: Work item type
            fields: Work item fields
            project: Project ID or name
            validate_only: Only validate, don't create
            bypass_rules: Bypass rules
            suppress_notifications: Suppress notifications
            expand: Expand options
            
        Returns:
            Created work item
        """
        params = {}
        if validate_only:
            params['validateOnly'] = validate_only
        if bypass_rules:
            params['bypassRules'] = bypass_rules
        if suppress_notifications:
            params['suppressNotifications'] = suppress_notifications
        if expand:
            params['$expand'] = expand
        
        # Build JSON Patch operations
        patch_operations = []
        for field_name, field_value in fields.items():
            patch_operations.append({
                "op": "add",
                "path": f"/fields/{field_name}",
                "value": field_value
            })
        
        endpoint = f"wit/workitems/${work_item_type}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/${work_item_type}"
        
        response_data = await self.client.post_json(
            endpoint,
            data=patch_operations,
            params=params,
            content_type="application/json-patch+json"
        )
        return WorkItem(**response_data)
    
    async def update_work_item(
        self,
        work_item_id: int,
        updates: List[Dict[str, Any]],
        project: Optional[str] = None,
        validate_only: Optional[bool] = None,
        bypass_rules: Optional[bool] = None,
        suppress_notifications: Optional[bool] = None,
        expand: Optional[str] = None
    ) -> WorkItem:
        """
        Update a work item using JSON Patch operations.
        
        Args:
            work_item_id: Work item ID
            updates: List of JSON Patch operations
            project: Project ID or name
            validate_only: Only validate, don't update
            bypass_rules: Bypass rules
            suppress_notifications: Suppress notifications
            expand: Expand options
            
        Returns:
            Updated work item
        """
        params = {}
        if validate_only:
            params['validateOnly'] = validate_only
        if bypass_rules:
            params['bypassRules'] = bypass_rules
        if suppress_notifications:
            params['suppressNotifications'] = suppress_notifications
        if expand:
            params['$expand'] = expand
        
        endpoint = f"wit/workitems/{work_item_id}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}"
        
        response_data = await self.client.patch_json(
            endpoint,
            data=updates,
            params=params,
            content_type="application/json-patch+json"
        )
        return WorkItem(**response_data)
    
    async def delete_work_item(
        self,
        work_item_id: int,
        project: Optional[str] = None,
        destroy: Optional[bool] = None
    ) -> WorkItem:
        """
        Delete a work item.
        
        Args:
            work_item_id: Work item ID
            project: Project ID or name
            destroy: Permanently delete
            
        Returns:
            Deleted work item
        """
        params = {}
        if destroy:
            params['destroy'] = destroy
        
        endpoint = f"wit/workitems/{work_item_id}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}"
        
        response_data = await self.client.delete_json(endpoint, params=params)
        return WorkItem(**response_data)
    
    # Work Item Updates/History
    async def get_work_item_updates(
        self,
        work_item_id: int,
        project: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[WorkItemUpdate]:
        """
        Get work item updates/history.
        
        Args:
            work_item_id: Work item ID
            project: Project ID or name
            top: Maximum number of updates
            skip: Number of updates to skip
            
        Returns:
            List of work item updates
        """
        params = {}
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        endpoint = f"wit/workitems/{work_item_id}/updates"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/updates"
        
        response_data = await self.client.get_json(endpoint, params=params)
        updates = response_data.get('value', [])
        return [WorkItemUpdate(**update) for update in updates]
    
    async def get_work_item_update(
        self,
        work_item_id: int,
        update_number: int,
        project: Optional[str] = None
    ) -> WorkItemUpdate:
        """
        Get a specific work item update.
        
        Args:
            work_item_id: Work item ID
            update_number: Update number
            project: Project ID or name
            
        Returns:
            Work item update
        """
        endpoint = f"wit/workitems/{work_item_id}/updates/{update_number}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/updates/{update_number}"
        
        response_data = await self.client.get_json(endpoint)
        return WorkItemUpdate(**response_data)
    
    # Work Item Comments
    async def get_work_item_comments(
        self,
        work_item_id: int,
        project: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        include_deleted: Optional[bool] = None,
        expand: Optional[str] = None,
        order: Optional[str] = None
    ) -> List[WorkItemComment]:
        """
        Get work item comments.
        
        Args:
            work_item_id: Work item ID
            project: Project ID or name
            top: Maximum number of comments
            continuation_token: Continuation token for pagination
            include_deleted: Include deleted comments
            expand: Expand options
            order: Sort order (asc, desc)
            
        Returns:
            List of work item comments
        """
        params = {}
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if include_deleted:
            params['includeDeleted'] = include_deleted
        if expand:
            params['$expand'] = expand
        if order:
            params['order'] = order
        
        endpoint = f"wit/workitems/{work_item_id}/comments"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/comments"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = WorkItemCommentsResponse(**response_data)
        return response.comments
    
    async def add_work_item_comment(
        self,
        work_item_id: int,
        comment_text: str,
        project: Optional[str] = None
    ) -> WorkItemComment:
        """
        Add a comment to a work item.
        
        Args:
            work_item_id: Work item ID
            comment_text: Comment text
            project: Project ID or name
            
        Returns:
            Created comment
        """
        endpoint = f"wit/workitems/{work_item_id}/comments"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/comments"
        
        comment_data = {"text": comment_text}
        response_data = await self.client.post_json(endpoint, data=comment_data)
        return WorkItemComment(**response_data)
    
    async def update_work_item_comment(
        self,
        work_item_id: int,
        comment_id: int,
        comment_text: str,
        project: Optional[str] = None
    ) -> WorkItemComment:
        """
        Update a work item comment.
        
        Args:
            work_item_id: Work item ID
            comment_id: Comment ID
            comment_text: Updated comment text
            project: Project ID or name
            
        Returns:
            Updated comment
        """
        endpoint = f"wit/workitems/{work_item_id}/comments/{comment_id}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/comments/{comment_id}"
        
        comment_data = {"text": comment_text}
        response_data = await self.client.patch_json(endpoint, data=comment_data)
        return WorkItemComment(**response_data)
    
    async def delete_work_item_comment(
        self,
        work_item_id: int,
        comment_id: int,
        project: Optional[str] = None
    ) -> None:
        """
        Delete a work item comment.
        
        Args:
            work_item_id: Work item ID
            comment_id: Comment ID
            project: Project ID or name
        """
        endpoint = f"wit/workitems/{work_item_id}/comments/{comment_id}"
        if project:
            endpoint = f"projects/{project}/wit/workitems/{work_item_id}/comments/{comment_id}"
        
        await self.client.delete(endpoint)
    
    # Work Item Types
    async def list_work_item_types(
        self,
        project: str
    ) -> List[WorkItemType]:
        """
        List work item types for a project.
        
        Args:
            project: Project ID or name
            
        Returns:
            List of work item types
        """
        endpoint = f"projects/{project}/wit/workitemtypes"
        response_data = await self.client.get_json(endpoint)
        response = WorkItemTypesResponse(**response_data)
        return response.value
    
    async def get_work_item_type(
        self,
        project: str,
        type_name: str
    ) -> WorkItemType:
        """
        Get a specific work item type.
        
        Args:
            project: Project ID or name
            type_name: Work item type name
            
        Returns:
            Work item type details
        """
        endpoint = f"projects/{project}/wit/workitemtypes/{type_name}"
        response_data = await self.client.get_json(endpoint)
        return WorkItemType(**response_data)
    
    # Work Item Fields
    async def list_fields(
        self,
        project: Optional[str] = None,
        expand: Optional[str] = None
    ) -> List[WorkItemField]:
        """
        List work item fields.
        
        Args:
            project: Project ID or name (if None, gets organization fields)
            expand: Expand options
            
        Returns:
            List of work item fields
        """
        params = {}
        if expand:
            params['$expand'] = expand
        
        endpoint = "wit/fields"
        if project:
            endpoint = f"projects/{project}/wit/fields"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = WorkItemFieldsResponse(**response_data)
        return response.value
    
    async def get_field(
        self,
        field_name_or_ref_name: str,
        project: Optional[str] = None
    ) -> WorkItemField:
        """
        Get a specific work item field.
        
        Args:
            field_name_or_ref_name: Field name or reference name
            project: Project ID or name
            
        Returns:
            Work item field details
        """
        endpoint = f"wit/fields/{field_name_or_ref_name}"
        if project:
            endpoint = f"projects/{project}/wit/fields/{field_name_or_ref_name}"
        
        response_data = await self.client.get_json(endpoint)
        return WorkItemField(**response_data)
    
    # Queries
    async def list_queries(
        self,
        project: str,
        expand: Optional[str] = None,
        depth: Optional[int] = None,
        include_deleted: Optional[bool] = None
    ) -> List[WorkItemQuery]:
        """
        List work item queries.
        
        Args:
            project: Project ID or name
            expand: Expand options
            depth: Query hierarchy depth
            include_deleted: Include deleted queries
            
        Returns:
            List of work item queries
        """
        params = {}
        if expand:
            params['$expand'] = expand
        if depth:
            params['$depth'] = depth
        if include_deleted:
            params['$includeDeleted'] = include_deleted
        
        endpoint = f"projects/{project}/wit/queries"
        response_data = await self.client.get_json(endpoint, params=params)
        queries = response_data.get('value', [])
        return [WorkItemQuery(**query) for query in queries]
    
    async def get_query(
        self,
        project: str,
        query_id: str,
        expand: Optional[str] = None,
        depth: Optional[int] = None,
        include_deleted: Optional[bool] = None
    ) -> WorkItemQuery:
        """
        Get a specific work item query.
        
        Args:
            project: Project ID or name
            query_id: Query ID
            expand: Expand options
            depth: Query hierarchy depth
            include_deleted: Include deleted queries
            
        Returns:
            Work item query details
        """
        params = {}
        if expand:
            params['$expand'] = expand
        if depth:
            params['$depth'] = depth
        if include_deleted:
            params['$includeDeleted'] = include_deleted
        
        endpoint = f"projects/{project}/wit/queries/{query_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return WorkItemQuery(**response_data)
    
    async def run_query_by_id(
        self,
        project: str,
        query_id: str,
        team_context: Optional[str] = None,
        time_precision: Optional[bool] = None,
        top: Optional[int] = None
    ) -> WorkItemQueryResult:
        """
        Run a work item query by ID.
        
        Args:
            project: Project ID or name
            query_id: Query ID
            team_context: Team context
            time_precision: Time precision
            top: Maximum number of results
            
        Returns:
            Query result
        """
        params = {}
        if team_context:
            params['teamContext'] = team_context
        if time_precision:
            params['timePrecision'] = time_precision
        if top:
            params['$top'] = top
        
        endpoint = f"projects/{project}/wit/wiql/{query_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return WorkItemQueryResult(**response_data)
    
    async def run_query_by_wiql(
        self,
        project: str,
        wiql_query: str,
        team_context: Optional[str] = None,
        time_precision: Optional[bool] = None,
        top: Optional[int] = None
    ) -> WorkItemQueryResult:
        """
        Run a work item query using WIQL.
        
        Args:
            project: Project ID or name
            wiql_query: WIQL query string
            team_context: Team context
            time_precision: Time precision
            top: Maximum number of results
            
        Returns:
            Query result
        """
        params = {}
        if team_context:
            params['teamContext'] = team_context
        if time_precision:
            params['timePrecision'] = time_precision
        if top:
            params['$top'] = top
        
        endpoint = f"projects/{project}/wit/wiql"
        query_data = {"query": wiql_query}
        response_data = await self.client.post_json(endpoint, data=query_data, params=params)
        return WorkItemQueryResult(**response_data)
    
    # Relations
    async def get_work_item_relations(
        self,
        work_item_id: int,
        project: Optional[str] = None
    ) -> List[WorkItemRelation]:
        """
        Get work item relations.
        
        Args:
            work_item_id: Work item ID
            project: Project ID or name
            
        Returns:
            List of work item relations
        """
        work_item = await self.get_work_item(
            work_item_id=work_item_id,
            project=project,
            expand="relations"
        )
        return work_item.relations or []
    
    async def add_work_item_relation(
        self,
        work_item_id: int,
        relation_type: str,
        target_url: str,
        project: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> WorkItem:
        """
        Add a relation to a work item.
        
        Args:
            work_item_id: Work item ID
            relation_type: Relation type
            target_url: Target URL
            project: Project ID or name
            attributes: Relation attributes
            
        Returns:
            Updated work item
        """
        relation_data = {
            "rel": relation_type,
            "url": target_url
        }
        if attributes:
            relation_data["attributes"] = attributes
        
        patch_operation = {
            "op": "add",
            "path": "/relations/-",
            "value": relation_data
        }
        
        return await self.update_work_item(
            work_item_id=work_item_id,
            updates=[patch_operation],
            project=project
        )
    
    async def remove_work_item_relation(
        self,
        work_item_id: int,
        relation_index: int,
        project: Optional[str] = None
    ) -> WorkItem:
        """
        Remove a relation from a work item.
        
        Args:
            work_item_id: Work item ID
            relation_index: Index of relation to remove
            project: Project ID or name
            
        Returns:
            Updated work item
        """
        patch_operation = {
            "op": "remove",
            "path": f"/relations/{relation_index}"
        }
        
        return await self.update_work_item(
            work_item_id=work_item_id,
            updates=[patch_operation],
            project=project
        )
    
    # Helper methods for common field updates
    async def update_work_item_fields(
        self,
        work_item_id: int,
        fields: Dict[str, Any],
        project: Optional[str] = None,
        **kwargs
    ) -> WorkItem:
        """
        Update work item fields (convenience method).
        
        Args:
            work_item_id: Work item ID
            fields: Dictionary of field updates
            project: Project ID or name
            
        Returns:
            Updated work item
        """
        patch_operations = []
        for field_name, field_value in fields.items():
            if field_value is None:
                # Remove field
                patch_operations.append({
                    "op": "remove",
                    "path": f"/fields/{field_name}"
                })
            else:
                # Add or update field
                patch_operations.append({
                    "op": "add",
                    "path": f"/fields/{field_name}",
                    "value": field_value
                })
        
        return await self.update_work_item(
            work_item_id=work_item_id,
            updates=patch_operations,
            project=project,
            **kwargs
        )
    
    # Utility methods
    async def search_work_items(
        self,
        project: str,
        search_text: str,
        work_item_types: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        top: Optional[int] = None
    ) -> List[WorkItem]:
        """
        Search work items by text.
        
        Args:
            project: Project ID or name
            search_text: Search text
            work_item_types: Work item types to search
            fields: Fields to return
            top: Maximum number of results
            
        Returns:
            List of matching work items
        """
        # Build WIQL query
        wiql_parts = ["SELECT"]
        if fields:
            wiql_parts.append(f"[{'], ['.join(fields)}]")
        else:
            wiql_parts.append("[System.Id], [System.Title], [System.State]")
        
        wiql_parts.append("FROM workitems")
        
        where_conditions = []
        if work_item_types:
            type_conditions = " OR ".join([f"[System.WorkItemType] = '{wit}'" for wit in work_item_types])
            where_conditions.append(f"({type_conditions})")
        
        if search_text:
            where_conditions.append(f"[System.Title] CONTAINS '{search_text}'")
        
        if where_conditions:
            wiql_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        if top:
            wiql_parts.append(f"ORDER BY [System.Id] DESC")
        
        wiql_query = " ".join(wiql_parts)
        
        # Run query
        result = await self.run_query_by_wiql(
            project=project,
            wiql_query=wiql_query,
            top=top
        )
        
        # Get work items if we have IDs
        if result.work_items:
            work_item_ids = [wi.id for wi in result.work_items if wi.id]
            if work_item_ids:
                return await self.get_work_items(
                    work_item_ids=work_item_ids,
                    project=project,
                    fields=fields
                )
        
        return []
    
    async def iterate_work_items_from_query(
        self,
        project: str,
        query_id: str,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[WorkItem, None]:
        """
        Iterate through work items from a query result.
        
        Args:
            project: Project ID or name
            query_id: Query ID
            page_size: Number of work items per batch
            
        Yields:
            Work items one by one
        """
        # Run the query to get work item IDs
        result = await self.run_query_by_id(project=project, query_id=query_id, **kwargs)
        
        if result.work_items:
            work_item_ids = [wi.id for wi in result.work_items if wi.id]
            
            # Process in batches
            for i in range(0, len(work_item_ids), page_size):
                batch_ids = work_item_ids[i:i + page_size]
                work_items = await self.get_work_items(
                    work_item_ids=batch_ids,
                    project=project
                )
                for work_item in work_items:
                    yield work_item
