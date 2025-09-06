"""
Notification service for Azure DevOps - Subscriptions, Events, Notification Management, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    NotificationSubscription, NotificationEvent, NotificationChannel,
    NotificationDeliveryPreference, NotificationEventType, NotificationStatistic,
    NotificationDiagnostic, NotificationSubscriptionTemplate, NotificationFilter,
    NotificationRole, NotificationScope, NotificationDeliveryResult
)


class NotificationService:
    """Service for Notification operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Subscriptions
    async def list_subscriptions(
        self,
        target_id: Optional[str] = None,
        subscriber_id: Optional[str] = None,
        query_flags: Optional[str] = None
    ) -> List[NotificationSubscription]:
        """
        List notification subscriptions.
        
        Args:
            target_id: Target ID to filter subscriptions
            subscriber_id: Subscriber ID to filter subscriptions
            query_flags: Query flags for additional data
            
        Returns:
            List of subscriptions
        """
        params = {}
        if target_id:
            params['targetId'] = target_id
        if subscriber_id:
            params['subscriberId'] = subscriber_id
        if query_flags:
            params['queryFlags'] = query_flags
        
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions"
        response_data = await self.client.get_json(endpoint, params=params)
        
        subscriptions = []
        for subscription_data in response_data.get("value", []):
            subscriptions.append(NotificationSubscription(**subscription_data))
        
        return subscriptions
    
    async def get_subscription(
        self,
        subscription_id: str,
        query_flags: Optional[str] = None
    ) -> NotificationSubscription:
        """
        Get a specific notification subscription.
        
        Args:
            subscription_id: Subscription ID
            query_flags: Query flags for additional data
            
        Returns:
            Subscription details
        """
        params = {}
        if query_flags:
            params['queryFlags'] = query_flags
        
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions/{subscription_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return NotificationSubscription(**response_data)
    
    async def create_subscription(
        self,
        subscription_data: Dict[str, Any]
    ) -> NotificationSubscription:
        """
        Create a new notification subscription.
        
        Args:
            subscription_data: Subscription configuration
            
        Returns:
            Created subscription
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions"
        response_data = await self.client.post_json(endpoint, data=subscription_data)
        return NotificationSubscription(**response_data)
    
    async def update_subscription(
        self,
        subscription_id: str,
        subscription_data: Dict[str, Any]
    ) -> NotificationSubscription:
        """
        Update a notification subscription.
        
        Args:
            subscription_id: Subscription ID
            subscription_data: Updated subscription data
            
        Returns:
            Updated subscription
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions/{subscription_id}"
        response_data = await self.client.put_json(endpoint, data=subscription_data)
        return NotificationSubscription(**response_data)
    
    async def delete_subscription(
        self,
        subscription_id: str
    ) -> None:
        """
        Delete a notification subscription.
        
        Args:
            subscription_id: Subscription ID
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions/{subscription_id}"
        await self.client.delete(endpoint)
    
    async def enable_subscription(
        self,
        subscription_id: str
    ) -> NotificationSubscription:
        """
        Enable a disabled subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Updated subscription
        """
        subscription_data = {"status": "enabled"}
        return await self.update_subscription(subscription_id, subscription_data)
    
    async def disable_subscription(
        self,
        subscription_id: str
    ) -> NotificationSubscription:
        """
        Disable a subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Updated subscription
        """
        subscription_data = {"status": "disabled"}
        return await self.update_subscription(subscription_id, subscription_data)
    
    # Event Types
    async def list_event_types(
        self,
        publisher_id: Optional[str] = None
    ) -> List[NotificationEventType]:
        """
        List available notification event types.
        
        Args:
            publisher_id: Filter by publisher ID
            
        Returns:
            List of event types
        """
        params = {}
        if publisher_id:
            params['publisherId'] = publisher_id
        
        endpoint = f"{self.client.organization}/_apis/notification/eventtypes"
        response_data = await self.client.get_json(endpoint, params=params)
        
        event_types = []
        for event_type_data in response_data.get("value", []):
            event_types.append(NotificationEventType(**event_type_data))
        
        return event_types
    
    async def get_event_type(
        self,
        event_type_id: str
    ) -> NotificationEventType:
        """
        Get a specific event type.
        
        Args:
            event_type_id: Event type ID
            
        Returns:
            Event type details
        """
        endpoint = f"{self.client.organization}/_apis/notification/eventtypes/{event_type_id}"
        response_data = await self.client.get_json(endpoint)
        return NotificationEventType(**response_data)
    
    # Subscription Templates
    async def list_subscription_templates(
        self) -> List[NotificationSubscriptionTemplate]:
        """
        List notification subscription templates.
        
        Returns:
            List of subscription templates
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptiontemplates"
        response_data = await self.client.get_json(endpoint)
        
        templates = []
        for template_data in response_data.get("value", []):
            templates.append(NotificationSubscriptionTemplate(**template_data))
        
        return templates
    
    async def get_subscription_template(
        self,
        template_id: str
    ) -> NotificationSubscriptionTemplate:
        """
        Get a specific subscription template.
        
        Args:
            template_id: Template ID
            
        Returns:
            Subscription template
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptiontemplates/{template_id}"
        response_data = await self.client.get_json(endpoint)
        return NotificationSubscriptionTemplate(**response_data)
    
    # Delivery Preferences
    async def get_delivery_preferences(
        self,
        subscriber_id: str
    ) -> List[NotificationDeliveryPreference]:
        """
        Get delivery preferences for a subscriber.
        
        Args:
            subscriber_id: Subscriber ID
            
        Returns:
            List of delivery preferences
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscribers/{subscriber_id}/deliverypreferences"
        response_data = await self.client.get_json(endpoint)
        
        preferences = []
        for preference_data in response_data.get("value", []):
            preferences.append(NotificationDeliveryPreference(**preference_data))
        
        return preferences
    
    async def update_delivery_preferences(
        self,
        subscriber_id: str,
        preferences: List[Dict[str, Any]]
    ) -> List[NotificationDeliveryPreference]:
        """
        Update delivery preferences for a subscriber.
        
        Args:
            subscriber_id: Subscriber ID
            preferences: Updated preferences
            
        Returns:
            Updated preferences
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscribers/{subscriber_id}/deliverypreferences"
        response_data = await self.client.put_json(endpoint, data=preferences)
        
        updated_preferences = []
        for preference_data in response_data.get("value", []):
            updated_preferences.append(NotificationDeliveryPreference(**preference_data))
        
        return updated_preferences
    
    # Events and Diagnostics
    async def list_events(
        self,
        max_created_date: Optional[datetime] = None,
        min_created_date: Optional[datetime] = None,
        publisher_id: Optional[str] = None,
        event_type: Optional[str] = None,
        skip: int = 0,
        top: int = 100
    ) -> List[NotificationEvent]:
        """
        List notification events.
        
        Args:
            max_created_date: Maximum creation date
            min_created_date: Minimum creation date
            publisher_id: Filter by publisher
            event_type: Filter by event type
            skip: Number of events to skip
            top: Number of events to return
            
        Returns:
            List of events
        """
        params = {
            '$skip': skip,
            '$top': top
        }
        if max_created_date:
            params['maxCreatedDate'] = max_created_date.isoformat()
        if min_created_date:
            params['minCreatedDate'] = min_created_date.isoformat()
        if publisher_id:
            params['publisherId'] = publisher_id
        if event_type:
            params['eventType'] = event_type
        
        endpoint = f"{self.client.organization}/_apis/notification/events"
        response_data = await self.client.get_json(endpoint, params=params)
        
        events = []
        for event_data in response_data.get("value", []):
            events.append(NotificationEvent(**event_data))
        
        return events
    
    async def get_event(
        self,
        event_id: str
    ) -> NotificationEvent:
        """
        Get a specific notification event.
        
        Args:
            event_id: Event ID
            
        Returns:
            Event details
        """
        endpoint = f"{self.client.organization}/_apis/notification/events/{event_id}"
        response_data = await self.client.get_json(endpoint)
        return NotificationEvent(**response_data)
    
    async def get_event_diagnostics(
        self,
        event_id: str
    ) -> List[NotificationDiagnostic]:
        """
        Get diagnostics for a notification event.
        
        Args:
            event_id: Event ID
            
        Returns:
            List of diagnostics
        """
        endpoint = f"{self.client.organization}/_apis/notification/events/{event_id}/diagnostics"
        response_data = await self.client.get_json(endpoint)
        
        diagnostics = []
        for diagnostic_data in response_data.get("value", []):
            diagnostics.append(NotificationDiagnostic(**diagnostic_data))
        
        return diagnostics
    
    async def get_subscription_diagnostics(
        self,
        subscription_id: str
    ) -> List[NotificationDiagnostic]:
        """
        Get diagnostics for a subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            List of diagnostics
        """
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions/{subscription_id}/diagnostics"
        response_data = await self.client.get_json(endpoint)
        
        diagnostics = []
        for diagnostic_data in response_data.get("value", []):
            diagnostics.append(NotificationDiagnostic(**diagnostic_data))
        
        return diagnostics
    
    # Statistics
    async def get_notification_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[NotificationStatistic]:
        """
        Get notification statistics.
        
        Args:
            start_date: Start date for statistics
            end_date: End date for statistics
            
        Returns:
            List of statistics
        """
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        
        endpoint = f"{self.client.organization}/_apis/notification/statistics"
        response_data = await self.client.get_json(endpoint, params=params)
        
        statistics = []
        for stat_data in response_data.get("value", []):
            statistics.append(NotificationStatistic(**stat_data))
        
        return statistics
    
    # Channels
    async def list_notification_channels(
        self,
        subscriber_id: Optional[str] = None
    ) -> List[NotificationChannel]:
        """
        List notification channels.
        
        Args:
            subscriber_id: Filter by subscriber
            
        Returns:
            List of channels
        """
        params = {}
        if subscriber_id:
            params['subscriberId'] = subscriber_id
        
        endpoint = f"{self.client.organization}/_apis/notification/channels"
        response_data = await self.client.get_json(endpoint, params=params)
        
        channels = []
        for channel_data in response_data.get("value", []):
            channels.append(NotificationChannel(**channel_data))
        
        return channels
    
    async def create_notification_channel(
        self,
        channel_data: Dict[str, Any]
    ) -> NotificationChannel:
        """
        Create a notification channel.
        
        Args:
            channel_data: Channel configuration
            
        Returns:
            Created channel
        """
        endpoint = f"{self.client.organization}/_apis/notification/channels"
        response_data = await self.client.post_json(endpoint, data=channel_data)
        return NotificationChannel(**response_data)
    
    async def update_notification_channel(
        self,
        channel_id: str,
        channel_data: Dict[str, Any]
    ) -> NotificationChannel:
        """
        Update a notification channel.
        
        Args:
            channel_id: Channel ID
            channel_data: Updated channel data
            
        Returns:
            Updated channel
        """
        endpoint = f"{self.client.organization}/_apis/notification/channels/{channel_id}"
        response_data = await self.client.put_json(endpoint, data=channel_data)
        return NotificationChannel(**response_data)
    
    async def delete_notification_channel(
        self,
        channel_id: str
    ) -> None:
        """
        Delete a notification channel.
        
        Args:
            channel_id: Channel ID
        """
        endpoint = f"{self.client.organization}/_apis/notification/channels/{channel_id}"
        await self.client.delete(endpoint)
    
    # Delivery Results
    async def get_delivery_results(
        self,
        subscription_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[NotificationDeliveryResult]:
        """
        Get delivery results for a subscription.
        
        Args:
            subscription_id: Subscription ID
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            List of delivery results
        """
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        
        endpoint = f"{self.client.organization}/_apis/notification/subscriptions/{subscription_id}/deliveryresults"
        response_data = await self.client.get_json(endpoint, params=params)
        
        results = []
        for result_data in response_data.get("value", []):
            results.append(NotificationDeliveryResult(**result_data))
        
        return results
    
    # Utility Methods
    async def create_work_item_subscription(
        self,
        subscriber_id: str,
        project_id: Optional[str] = None,
        work_item_type: Optional[str] = None,
        area_path: Optional[str] = None,
        channel_type: str = "email",
        channel_address: Optional[str] = None
    ) -> NotificationSubscription:
        """
        Create a work item notification subscription.
        
        Args:
            subscriber_id: Subscriber ID
            project_id: Project to monitor
            work_item_type: Work item type filter
            area_path: Area path filter
            channel_type: Notification channel type
            channel_address: Channel address (email, etc.)
            
        Returns:
            Created subscription
        """
        # Build filter conditions
        filter_conditions = []
        
        if project_id:
            filter_conditions.append({
                "fieldName": "Project",
                "operator": "=",
                "value": project_id
            })
        
        if work_item_type:
            filter_conditions.append({
                "fieldName": "Work Item Type",
                "operator": "=",
                "value": work_item_type
            })
        
        if area_path:
            filter_conditions.append({
                "fieldName": "Area Path",
                "operator": "under",
                "value": area_path
            })
        
        subscription_data = {
            "description": "Work item notification subscription",
            "filter": {
                "type": "Expression",
                "criteria": {
                    "clauses": filter_conditions
                }
            },
            "eventType": "ms.vss-work.workitem-changed-event",
            "subscriber": {
                "id": subscriber_id
            },
            "channel": {
                "type": channel_type,
                "address": channel_address or subscriber_id
            }
        }
        
        return await self.create_subscription(subscription_data)
    
    async def create_build_subscription(
        self,
        subscriber_id: str,
        project_id: Optional[str] = None,
        definition_id: Optional[str] = None,
        build_status: Optional[str] = None,
        channel_type: str = "email",
        channel_address: Optional[str] = None
    ) -> NotificationSubscription:
        """
        Create a build notification subscription.
        
        Args:
            subscriber_id: Subscriber ID
            project_id: Project to monitor
            definition_id: Build definition ID
            build_status: Build status filter (completed, failed, etc.)
            channel_type: Notification channel type
            channel_address: Channel address
            
        Returns:
            Created subscription
        """
        filter_conditions = []
        
        if project_id:
            filter_conditions.append({
                "fieldName": "Project",
                "operator": "=",
                "value": project_id
            })
        
        if definition_id:
            filter_conditions.append({
                "fieldName": "Build Definition",
                "operator": "=",
                "value": definition_id
            })
        
        if build_status:
            filter_conditions.append({
                "fieldName": "Build Status",
                "operator": "=",
                "value": build_status
            })
        
        subscription_data = {
            "description": "Build notification subscription",
            "filter": {
                "type": "Expression",
                "criteria": {
                    "clauses": filter_conditions
                }
            },
            "eventType": "ms.vss-build.build-status-changed-event",
            "subscriber": {
                "id": subscriber_id
            },
            "channel": {
                "type": channel_type,
                "address": channel_address or subscriber_id
            }
        }
        
        return await self.create_subscription(subscription_data)
    
    async def create_git_subscription(
        self,
        subscriber_id: str,
        project_id: Optional[str] = None,
        repository_id: Optional[str] = None,
        branch_name: Optional[str] = None,
        event_type: str = "git.push",
        channel_type: str = "email",
        channel_address: Optional[str] = None
    ) -> NotificationSubscription:
        """
        Create a Git notification subscription.
        
        Args:
            subscriber_id: Subscriber ID
            project_id: Project to monitor
            repository_id: Repository ID
            branch_name: Branch name filter
            event_type: Git event type
            channel_type: Notification channel type
            channel_address: Channel address
            
        Returns:
            Created subscription
        """
        filter_conditions = []
        
        if project_id:
            filter_conditions.append({
                "fieldName": "Project",
                "operator": "=",
                "value": project_id
            })
        
        if repository_id:
            filter_conditions.append({
                "fieldName": "Repository",
                "operator": "=",
                "value": repository_id
            })
        
        if branch_name:
            filter_conditions.append({
                "fieldName": "Branch",
                "operator": "=",
                "value": branch_name
            })
        
        subscription_data = {
            "description": "Git notification subscription",
            "filter": {
                "type": "Expression",
                "criteria": {
                    "clauses": filter_conditions
                }
            },
            "eventType": f"ms.vss-code.{event_type}-event",
            "subscriber": {
                "id": subscriber_id
            },
            "channel": {
                "type": channel_type,
                "address": channel_address or subscriber_id
            }
        }
        
        return await self.create_subscription(subscription_data)
    
    async def get_user_subscriptions(
        self,
        user_id: str,
        include_disabled: bool = False
    ) -> List[NotificationSubscription]:
        """
        Get all subscriptions for a specific user.
        
        Args:
            user_id: User ID
            include_disabled: Include disabled subscriptions
            
        Returns:
            List of user subscriptions
        """
        subscriptions = await self.list_subscriptions(subscriber_id=user_id)
        
        if not include_disabled:
            subscriptions = [s for s in subscriptions if s.status != "disabled"]
        
        return subscriptions
    
    async def get_project_subscriptions(
        self,
        project_id: str
    ) -> List[NotificationSubscription]:
        """
        Get all subscriptions for a specific project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of project subscriptions
        """
        # This would require filtering subscriptions based on their filters
        # For now, get all subscriptions and filter client-side
        all_subscriptions = await self.list_subscriptions()
        
        project_subscriptions = []
        for subscription in all_subscriptions:
            # Check if subscription filter includes this project
            if hasattr(subscription, 'filter') and subscription.filter:
                # This is a simplified check - real implementation would need
                # to parse the filter criteria properly
                if project_id in str(subscription.filter):
                    project_subscriptions.append(subscription)
        
        return project_subscriptions
    
    async def bulk_create_subscriptions(
        self,
        subscriptions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Create multiple subscriptions in bulk.
        
        Args:
            subscriptions: List of subscription configurations
            
        Returns:
            Creation results
        """
        results = []
        
        for sub_data in subscriptions:
            result = {
                "subscription_data": sub_data,
                "success": False,
                "error": None,
                "subscription": None
            }
            
            try:
                subscription = await self.create_subscription(sub_data)
                result["success"] = True
                result["subscription"] = subscription
            except Exception as e:
                result["error"] = str(e)
            
            results.append(result)
        
        return results
    
    async def get_notification_summary(
        self,
        subscriber_id: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get a summary of notification activity.
        
        Args:
            subscriber_id: Filter by subscriber
            days: Number of days to include
            
        Returns:
            Notification summary
        """
        end_date = datetime.utcnow()
        start_date = end_date.replace(day=end_date.day - days) if days < end_date.day else end_date.replace(month=end_date.month - 1)
        
        summary = {
            "period": f"{days} days",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_subscriptions": 0,
            "active_subscriptions": 0,
            "disabled_subscriptions": 0,
            "total_events": 0,
            "delivery_success_rate": 0.0,
            "top_event_types": [],
            "subscriptions": [],
            "statistics": []
        }
        
        try:
            # Get subscriptions
            subscriptions = await self.list_subscriptions(subscriber_id=subscriber_id)
            summary["subscriptions"] = subscriptions
            summary["total_subscriptions"] = len(subscriptions)
            summary["active_subscriptions"] = len([s for s in subscriptions if s.status == "enabled"])
            summary["disabled_subscriptions"] = len([s for s in subscriptions if s.status == "disabled"])
            
            # Get events
            events = await self.list_events(
                min_created_date=start_date,
                max_created_date=end_date,
                top=1000
            )
            summary["total_events"] = len(events)
            
            # Analyze event types
            event_type_counts = {}
            for event in events:
                event_type = getattr(event, 'event_type', 'unknown')
                event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            summary["top_event_types"] = sorted(
                event_type_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            # Get statistics
            statistics = await self.get_notification_statistics(start_date, end_date)
            summary["statistics"] = statistics
            
            # Calculate success rate
            if statistics:
                total_deliveries = sum(getattr(s, 'delivery_count', 0) for s in statistics)
                successful_deliveries = sum(getattr(s, 'success_count', 0) for s in statistics)
                if total_deliveries > 0:
                    summary["delivery_success_rate"] = successful_deliveries / total_deliveries
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
