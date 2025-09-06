"""
Service Hooks service for Azure DevOps - Webhooks, Integrations, Service Hook Management, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    ServiceHook, ServiceHookSubscription, ServiceHookConsumer, ServiceHookPublisher,
    ServiceHookEvent, ServiceHookEventType, ServiceHookNotification, ServiceHookInput,
    ServiceHookAction, ServiceHookFilter, ServiceHookConsumerAction, ServiceHookTest,
    ServiceHookHistory, ServiceHookStatistic
)


class ServiceHooksService:
    """Service for Service Hooks (Webhooks/Integrations) operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Service Hook Subscriptions
    async def list_subscriptions(
        self,
        publisher_id: Optional[str] = None,
        event_type: Optional[str] = None,
        consumer_id: Optional[str] = None
    ) -> List[ServiceHookSubscription]:
        """
        List service hook subscriptions.
        
        Args:
            publisher_id: Filter by publisher ID
            event_type: Filter by event type
            consumer_id: Filter by consumer ID
            
        Returns:
            List of service hook subscriptions
        """
        params = {}
        if publisher_id:
            params['publisherId'] = publisher_id
        if event_type:
            params['eventType'] = event_type
        if consumer_id:
            params['consumerId'] = consumer_id
        
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions"
        response_data = await self.client.get_json(endpoint, params=params)
        
        subscriptions = []
        for subscription_data in response_data.get("value", []):
            subscriptions.append(ServiceHookSubscription(**subscription_data))
        
        return subscriptions
    
    async def get_subscription(
        self,
        subscription_id: str
    ) -> ServiceHookSubscription:
        """
        Get a specific service hook subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Service hook subscription details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookSubscription(**response_data)
    
    async def create_subscription(
        self,
        subscription_data: Dict[str, Any]
    ) -> ServiceHookSubscription:
        """
        Create a new service hook subscription.
        
        Args:
            subscription_data: Subscription configuration
            
        Returns:
            Created subscription
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions"
        response_data = await self.client.post_json(endpoint, data=subscription_data)
        return ServiceHookSubscription(**response_data)
    
    async def update_subscription(
        self,
        subscription_id: str,
        subscription_data: Dict[str, Any]
    ) -> ServiceHookSubscription:
        """
        Update a service hook subscription.
        
        Args:
            subscription_id: Subscription ID
            subscription_data: Updated subscription data
            
        Returns:
            Updated subscription
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}"
        response_data = await self.client.put_json(endpoint, data=subscription_data)
        return ServiceHookSubscription(**response_data)
    
    async def delete_subscription(
        self,
        subscription_id: str
    ) -> None:
        """
        Delete a service hook subscription.
        
        Args:
            subscription_id: Subscription ID
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}"
        await self.client.delete(endpoint)
    
    async def enable_subscription(
        self,
        subscription_id: str
    ) -> ServiceHookSubscription:
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
    ) -> ServiceHookSubscription:
        """
        Disable a subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Updated subscription
        """
        subscription_data = {"status": "disabled"}
        return await self.update_subscription(subscription_id, subscription_data)
    
    # Publishers
    async def list_publishers(
        self,
        publisher_id: Optional[str] = None
    ) -> List[ServiceHookPublisher]:
        """
        List service hook publishers.
        
        Args:
            publisher_id: Specific publisher ID to get
            
        Returns:
            List of publishers
        """
        endpoint = f"{self.client.organization}/_apis/hooks/publishers"
        if publisher_id:
            endpoint += f"/{publisher_id}"
            response_data = await self.client.get_json(endpoint)
            return [ServiceHookPublisher(**response_data)]
        else:
            response_data = await self.client.get_json(endpoint)
            publishers = []
            for publisher_data in response_data.get("value", []):
                publishers.append(ServiceHookPublisher(**publisher_data))
            return publishers
    
    async def get_publisher(
        self,
        publisher_id: str
    ) -> ServiceHookPublisher:
        """
        Get a specific service hook publisher.
        
        Args:
            publisher_id: Publisher ID
            
        Returns:
            Publisher details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/publishers/{publisher_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookPublisher(**response_data)
    
    # Event Types
    async def list_event_types(
        self,
        publisher_id: Optional[str] = None
    ) -> List[ServiceHookEventType]:
        """
        List service hook event types.
        
        Args:
            publisher_id: Filter by publisher ID
            
        Returns:
            List of event types
        """
        params = {}
        if publisher_id:
            params['publisherId'] = publisher_id
        
        endpoint = f"{self.client.organization}/_apis/hooks/eventtypes"
        response_data = await self.client.get_json(endpoint, params=params)
        
        event_types = []
        for event_type_data in response_data.get("value", []):
            event_types.append(ServiceHookEventType(**event_type_data))
        
        return event_types
    
    async def get_event_type(
        self,
        publisher_id: str,
        event_type_id: str
    ) -> ServiceHookEventType:
        """
        Get a specific event type for a publisher.
        
        Args:
            publisher_id: Publisher ID
            event_type_id: Event type ID
            
        Returns:
            Event type details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/publishers/{publisher_id}/eventtypes/{event_type_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookEventType(**response_data)
    
    # Consumers
    async def list_consumers(
        self,
        consumer_id: Optional[str] = None
    ) -> List[ServiceHookConsumer]:
        """
        List service hook consumers.
        
        Args:
            consumer_id: Specific consumer ID to get
            
        Returns:
            List of consumers
        """
        endpoint = f"{self.client.organization}/_apis/hooks/consumers"
        if consumer_id:
            endpoint += f"/{consumer_id}"
            response_data = await self.client.get_json(endpoint)
            return [ServiceHookConsumer(**response_data)]
        else:
            response_data = await self.client.get_json(endpoint)
            consumers = []
            for consumer_data in response_data.get("value", []):
                consumers.append(ServiceHookConsumer(**consumer_data))
            return consumers
    
    async def get_consumer(
        self,
        consumer_id: str
    ) -> ServiceHookConsumer:
        """
        Get a specific service hook consumer.
        
        Args:
            consumer_id: Consumer ID
            
        Returns:
            Consumer details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/consumers/{consumer_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookConsumer(**response_data)
    
    async def list_consumer_actions(
        self,
        consumer_id: str
    ) -> List[ServiceHookConsumerAction]:
        """
        List actions for a specific consumer.
        
        Args:
            consumer_id: Consumer ID
            
        Returns:
            List of consumer actions
        """
        endpoint = f"{self.client.organization}/_apis/hooks/consumers/{consumer_id}/actions"
        response_data = await self.client.get_json(endpoint)
        
        actions = []
        for action_data in response_data.get("value", []):
            actions.append(ServiceHookConsumerAction(**action_data))
        
        return actions
    
    async def get_consumer_action(
        self,
        consumer_id: str,
        consumer_action_id: str
    ) -> ServiceHookConsumerAction:
        """
        Get a specific consumer action.
        
        Args:
            consumer_id: Consumer ID
            consumer_action_id: Consumer action ID
            
        Returns:
            Consumer action details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/consumers/{consumer_id}/actions/{consumer_action_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookConsumerAction(**response_data)
    
    # Notifications
    async def list_notifications(
        self,
        subscription_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
        result: Optional[str] = None
    ) -> List[ServiceHookNotification]:
        """
        List service hook notifications.
        
        Args:
            subscription_id: Filter by subscription ID
            start_date: Start date filter
            end_date: End date filter
            status: Status filter (queued, processing, completed, failed)
            result: Result filter (succeeded, failed, filtered)
            
        Returns:
            List of notifications
        """
        params = {}
        if subscription_id:
            params['subscriptionId'] = subscription_id
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        if status:
            params['status'] = status
        if result:
            params['result'] = result
        
        endpoint = f"{self.client.organization}/_apis/hooks/notifications"
        response_data = await self.client.get_json(endpoint, params=params)
        
        notifications = []
        for notification_data in response_data.get("value", []):
            notifications.append(ServiceHookNotification(**notification_data))
        
        return notifications
    
    async def get_notification(
        self,
        notification_id: str
    ) -> ServiceHookNotification:
        """
        Get a specific service hook notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Notification details
        """
        endpoint = f"{self.client.organization}/_apis/hooks/notifications/{notification_id}"
        response_data = await self.client.get_json(endpoint)
        return ServiceHookNotification(**response_data)
    
    async def get_subscription_notifications(
        self,
        subscription_id: str,
        max_results: int = 100
    ) -> List[ServiceHookNotification]:
        """
        Get notifications for a specific subscription.
        
        Args:
            subscription_id: Subscription ID
            max_results: Maximum number of results
            
        Returns:
            List of notifications
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}/notifications"
        params = {'maxResults': max_results}
        response_data = await self.client.get_json(endpoint, params=params)
        
        notifications = []
        for notification_data in response_data.get("value", []):
            notifications.append(ServiceHookNotification(**notification_data))
        
        return notifications
    
    # Testing
    async def test_subscription(
        self,
        subscription_id: str,
        test_data: Optional[Dict[str, Any]] = None
    ) -> ServiceHookTest:
        """
        Test a service hook subscription.
        
        Args:
            subscription_id: Subscription ID
            test_data: Optional test data
            
        Returns:
            Test result
        """
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}/test"
        data = test_data or {}
        response_data = await self.client.post_json(endpoint, data=data)
        return ServiceHookTest(**response_data)
    
    async def test_notification(
        self,
        notification_id: str
    ) -> ServiceHookTest:
        """
        Test a specific notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Test result
        """
        endpoint = f"{self.client.organization}/_apis/hooks/notifications/{notification_id}/test"
        response_data = await self.client.post_json(endpoint, data={})
        return ServiceHookTest(**response_data)
    
    # Statistics
    async def get_subscription_statistics(
        self,
        subscription_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> ServiceHookStatistic:
        """
        Get statistics for a subscription.
        
        Args:
            subscription_id: Subscription ID
            start_date: Start date for statistics
            end_date: End date for statistics
            
        Returns:
            Subscription statistics
        """
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        
        endpoint = f"{self.client.organization}/_apis/hooks/subscriptions/{subscription_id}/statistics"
        response_data = await self.client.get_json(endpoint, params=params)
        return ServiceHookStatistic(**response_data)
    
    async def get_global_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ServiceHookStatistic]:
        """
        Get global service hook statistics.
        
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
        
        endpoint = f"{self.client.organization}/_apis/hooks/statistics"
        response_data = await self.client.get_json(endpoint, params=params)
        
        statistics = []
        for stat_data in response_data.get("value", []):
            statistics.append(ServiceHookStatistic(**stat_data))
        
        return statistics
    
    # Utility Methods
    async def create_webhook_subscription(
        self,
        webhook_url: str,
        event_type: str,
        publisher_id: str = "tfs",
        secret: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        resource_version: str = "1.0"
    ) -> ServiceHookSubscription:
        """
        Create a webhook subscription.
        
        Args:
            webhook_url: Target webhook URL
            event_type: Event type to subscribe to
            publisher_id: Publisher ID (default: tfs)
            secret: Secret for webhook authentication
            filters: Event filters
            resource_version: Resource version
            
        Returns:
            Created subscription
        """
        consumer_inputs = {
            "url": webhook_url,
            "resourceDetailsToSend": "all",
            "messagesToSend": "all",
            "detailedMessagesToSend": "all"
        }
        
        if secret:
            consumer_inputs["basicAuthUsername"] = ""
            consumer_inputs["basicAuthPassword"] = secret
        
        subscription_data = {
            "publisherId": publisher_id,
            "eventType": event_type,
            "consumerId": "webHooks",
            "consumerActionId": "httpRequest",
            "consumerInputs": consumer_inputs,
            "resourceVersion": resource_version
        }
        
        if filters:
            subscription_data["publisherInputs"] = filters
        
        return await self.create_subscription(subscription_data)
    
    async def create_slack_subscription(
        self,
        webhook_url: str,
        event_type: str,
        channel: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> ServiceHookSubscription:
        """
        Create a Slack webhook subscription.
        
        Args:
            webhook_url: Slack webhook URL
            event_type: Event type to subscribe to
            channel: Slack channel (optional)
            filters: Event filters
            
        Returns:
            Created subscription
        """
        consumer_inputs = {
            "url": webhook_url
        }
        
        if channel:
            consumer_inputs["channel"] = channel
        
        subscription_data = {
            "publisherId": "tfs",
            "eventType": event_type,
            "consumerId": "slack",
            "consumerActionId": "postMessage",
            "consumerInputs": consumer_inputs
        }
        
        if filters:
            subscription_data["publisherInputs"] = filters
        
        return await self.create_subscription(subscription_data)
    
    async def create_teams_subscription(
        self,
        webhook_url: str,
        event_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> ServiceHookSubscription:
        """
        Create a Microsoft Teams webhook subscription.
        
        Args:
            webhook_url: Teams webhook URL
            event_type: Event type to subscribe to
            filters: Event filters
            
        Returns:
            Created subscription
        """
        consumer_inputs = {
            "url": webhook_url
        }
        
        subscription_data = {
            "publisherId": "tfs",
            "eventType": event_type,
            "consumerId": "microsoftTeams",
            "consumerActionId": "postMessage",
            "consumerInputs": consumer_inputs
        }
        
        if filters:
            subscription_data["publisherInputs"] = filters
        
        return await self.create_subscription(subscription_data)
    
    async def create_email_subscription(
        self,
        email_addresses: List[str],
        event_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> ServiceHookSubscription:
        """
        Create an email subscription.
        
        Args:
            email_addresses: List of email addresses
            event_type: Event type to subscribe to
            filters: Event filters
            
        Returns:
            Created subscription
        """
        consumer_inputs = {
            "to": ",".join(email_addresses),
            "subject": "Azure DevOps Notification"
        }
        
        subscription_data = {
            "publisherId": "tfs",
            "eventType": event_type,
            "consumerId": "emailHtml",
            "consumerActionId": "sendMail",
            "consumerInputs": consumer_inputs
        }
        
        if filters:
            subscription_data["publisherInputs"] = filters
        
        return await self.create_subscription(subscription_data)
    
    async def get_work_item_filters(
        self,
        project_id: Optional[str] = None,
        work_item_type: Optional[str] = None,
        area_path: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build work item filters for subscriptions.
        
        Args:
            project_id: Project ID
            work_item_type: Work item type
            area_path: Area path
            assigned_to: Assigned to user
            
        Returns:
            Filter dictionary
        """
        filters = {}
        
        if project_id:
            filters["projectId"] = project_id
        if work_item_type:
            filters["workItemType"] = work_item_type
        if area_path:
            filters["areaPath"] = area_path
        if assigned_to:
            filters["assignedTo"] = assigned_to
        
        return filters
    
    async def get_build_filters(
        self,
        project_id: Optional[str] = None,
        definition_id: Optional[str] = None,
        build_status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build build filters for subscriptions.
        
        Args:
            project_id: Project ID
            definition_id: Build definition ID
            build_status: Build status
            
        Returns:
            Filter dictionary
        """
        filters = {}
        
        if project_id:
            filters["projectId"] = project_id
        if definition_id:
            filters["definitionId"] = definition_id
        if build_status:
            filters["buildStatus"] = build_status
        
        return filters
    
    async def get_git_filters(
        self,
        project_id: Optional[str] = None,
        repository_id: Optional[str] = None,
        branch_name: Optional[str] = None,
        pusher: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build Git filters for subscriptions.
        
        Args:
            project_id: Project ID
            repository_id: Repository ID
            branch_name: Branch name
            pusher: Pusher identity
            
        Returns:
            Filter dictionary
        """
        filters = {}
        
        if project_id:
            filters["projectId"] = project_id
        if repository_id:
            filters["repository"] = repository_id
        if branch_name:
            filters["branch"] = branch_name
        if pusher:
            filters["pusher"] = pusher
        
        return filters
    
    async def bulk_create_subscriptions(
        self,
        subscriptions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Create multiple service hook subscriptions in bulk.
        
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
    
    async def get_failed_notifications(
        self,
        subscription_id: Optional[str] = None,
        days: int = 7
    ) -> List[ServiceHookNotification]:
        """
        Get failed notifications for troubleshooting.
        
        Args:
            subscription_id: Filter by subscription
            days: Number of days to look back
            
        Returns:
            List of failed notifications
        """
        end_date = datetime.utcnow()
        start_date = end_date.replace(day=end_date.day - days) if days < end_date.day else end_date.replace(month=end_date.month - 1)
        
        notifications = await self.list_notifications(
            subscription_id=subscription_id,
            start_date=start_date,
            end_date=end_date,
            result="failed"
        )
        
        return notifications
    
    async def get_service_hooks_summary(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get a comprehensive summary of service hooks activity.
        
        Args:
            days: Number of days to include in summary
            
        Returns:
            Service hooks summary
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
            "total_notifications": 0,
            "successful_notifications": 0,
            "failed_notifications": 0,
            "success_rate": 0.0,
            "consumers": {},
            "publishers": {},
            "event_types": {},
            "subscriptions": [],
            "recent_failures": []
        }
        
        try:
            # Get all subscriptions
            subscriptions = await self.list_subscriptions()
            summary["subscriptions"] = subscriptions
            summary["total_subscriptions"] = len(subscriptions)
            
            active_count = 0
            disabled_count = 0
            consumer_counts = {}
            publisher_counts = {}
            
            for subscription in subscriptions:
                if subscription.status == "enabled":
                    active_count += 1
                else:
                    disabled_count += 1
                
                # Count by consumer
                consumer = subscription.consumer_id
                consumer_counts[consumer] = consumer_counts.get(consumer, 0) + 1
                
                # Count by publisher
                publisher = subscription.publisher_id
                publisher_counts[publisher] = publisher_counts.get(publisher, 0) + 1
            
            summary["active_subscriptions"] = active_count
            summary["disabled_subscriptions"] = disabled_count
            summary["consumers"] = consumer_counts
            summary["publishers"] = publisher_counts
            
            # Get notifications
            notifications = await self.list_notifications(
                start_date=start_date,
                end_date=end_date
            )
            summary["total_notifications"] = len(notifications)
            
            successful_count = 0
            failed_count = 0
            event_type_counts = {}
            
            for notification in notifications:
                if notification.result == "succeeded":
                    successful_count += 1
                elif notification.result == "failed":
                    failed_count += 1
                
                # Count by event type
                event_type = getattr(notification, 'event_type', 'unknown')
                event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            summary["successful_notifications"] = successful_count
            summary["failed_notifications"] = failed_count
            summary["event_types"] = event_type_counts
            
            if summary["total_notifications"] > 0:
                summary["success_rate"] = successful_count / summary["total_notifications"]
            
            # Get recent failures
            recent_failures = await self.get_failed_notifications(days=7)
            summary["recent_failures"] = recent_failures[:10]  # Top 10 recent failures
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
