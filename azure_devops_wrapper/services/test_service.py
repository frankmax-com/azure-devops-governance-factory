"""
Test service for Azure DevOps - Test Plans, Test Cases, Test Runs, Test Results, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    TestPlan, TestSuite, TestCase, TestRun, TestResult, TestPoint, TestIteration,
    TestConfiguration, TestVariable, TestAttachment, TestCaseResult, TestRunStatistic,
    TestPlansResponse, TestSuitesResponse, TestCasesResponse, TestRunsResponse,
    TestResultsResponse, TestPointsResponse, TestConfigurationsResponse
)


class TestService:
    """Service for Test Management operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Test Plans
    async def list_test_plans(
        self,
        project: str,
        owner: Optional[str] = None,
        skip: Optional[int] = None,
        top: Optional[int] = None,
        include_plan_details: Optional[bool] = None,
        filter_active_plans: Optional[bool] = None
    ) -> List[TestPlan]:
        """
        List test plans in a project.
        
        Args:
            project: Project ID or name
            owner: Owner filter
            skip: Number of plans to skip
            top: Maximum number of plans
            include_plan_details: Include plan details
            filter_active_plans: Filter only active plans
            
        Returns:
            List of test plans
        """
        params = {}
        if owner:
            params['owner'] = owner
        if skip:
            params['$skip'] = skip
        if top:
            params['$top'] = top
        if include_plan_details:
            params['includePlanDetails'] = include_plan_details
        if filter_active_plans:
            params['filterActivePlans'] = filter_active_plans
        
        endpoint = f"projects/{project}/test/plans"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestPlansResponse(**response_data)
        return response.value
    
    async def get_test_plan(
        self,
        project: str,
        plan_id: int
    ) -> TestPlan:
        """
        Get a specific test plan.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            
        Returns:
            Test plan details
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}"
        response_data = await self.client.get_json(endpoint)
        return TestPlan(**response_data)
    
    async def create_test_plan(
        self,
        project: str,
        plan_data: Dict[str, Any]
    ) -> TestPlan:
        """
        Create a new test plan.
        
        Args:
            project: Project ID or name
            plan_data: Test plan creation data
            
        Returns:
            Created test plan
        """
        endpoint = f"projects/{project}/test/plans"
        response_data = await self.client.post_json(endpoint, data=plan_data)
        return TestPlan(**response_data)
    
    async def update_test_plan(
        self,
        project: str,
        plan_id: int,
        plan_data: Dict[str, Any]
    ) -> TestPlan:
        """
        Update a test plan.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            plan_data: Test plan update data
            
        Returns:
            Updated test plan
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}"
        response_data = await self.client.patch_json(endpoint, data=plan_data)
        return TestPlan(**response_data)
    
    async def delete_test_plan(
        self,
        project: str,
        plan_id: int
    ) -> None:
        """
        Delete a test plan.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}"
        await self.client.delete(endpoint)
    
    # Test Suites
    async def list_test_suites(
        self,
        project: str,
        plan_id: int,
        expand: Optional[str] = None,
        continuation_token: Optional[str] = None,
        as_tree_view: Optional[bool] = None
    ) -> List[TestSuite]:
        """
        List test suites in a test plan.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            expand: Expand options
            continuation_token: Continuation token
            as_tree_view: Return as tree view
            
        Returns:
            List of test suites
        """
        params = {}
        if expand:
            params['$expand'] = expand
        if continuation_token:
            params['continuationToken'] = continuation_token
        if as_tree_view:
            params['$asTreeView'] = as_tree_view
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestSuitesResponse(**response_data)
        return response.value
    
    async def get_test_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        expand: Optional[str] = None
    ) -> TestSuite:
        """
        Get a specific test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            expand: Expand options
            
        Returns:
            Test suite details
        """
        params = {}
        if expand:
            params['$expand'] = expand
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return TestSuite(**response_data)
    
    async def create_test_suite(
        self,
        project: str,
        plan_id: int,
        suite_data: Dict[str, Any]
    ) -> TestSuite:
        """
        Create a new test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_data: Test suite creation data
            
        Returns:
            Created test suite
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites"
        response_data = await self.client.post_json(endpoint, data=suite_data)
        return TestSuite(**response_data)
    
    async def update_test_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        suite_data: Dict[str, Any]
    ) -> TestSuite:
        """
        Update a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            suite_data: Test suite update data
            
        Returns:
            Updated test suite
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}"
        response_data = await self.client.patch_json(endpoint, data=suite_data)
        return TestSuite(**response_data)
    
    async def delete_test_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int
    ) -> None:
        """
        Delete a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}"
        await self.client.delete(endpoint)
    
    # Test Cases
    async def list_test_cases(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        test_case_ids: Optional[str] = None,
        configuration_ids: Optional[str] = None,
        wit_fields: Optional[str] = None,
        continuation_token: Optional[str] = None,
        return_identity_ref: Optional[bool] = None,
        expand: Optional[str] = None,
        exclude_flags: Optional[str] = None,
        is_recursive: Optional[bool] = None
    ) -> List[TestCase]:
        """
        List test cases in a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            test_case_ids: Specific test case IDs
            configuration_ids: Configuration IDs filter
            wit_fields: Work item fields to include
            continuation_token: Continuation token
            return_identity_ref: Return identity references
            expand: Expand options
            exclude_flags: Exclude flags
            is_recursive: Include child suites
            
        Returns:
            List of test cases
        """
        params = {}
        if test_case_ids:
            params['testCaseIds'] = test_case_ids
        if configuration_ids:
            params['configurationIds'] = configuration_ids
        if wit_fields:
            params['witFields'] = wit_fields
        if continuation_token:
            params['continuationToken'] = continuation_token
        if return_identity_ref:
            params['returnIdentityRef'] = return_identity_ref
        if expand:
            params['$expand'] = expand
        if exclude_flags:
            params['excludeFlags'] = exclude_flags
        if is_recursive:
            params['isRecursive'] = is_recursive
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/testcases"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestCasesResponse(**response_data)
        return response.value
    
    async def get_test_case(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        test_case_ids: str,
        wit_fields: Optional[str] = None,
        return_identity_ref: Optional[bool] = None
    ) -> TestCase:
        """
        Get a specific test case.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            test_case_ids: Test case ID
            wit_fields: Work item fields to include
            return_identity_ref: Return identity references
            
        Returns:
            Test case details
        """
        params = {'testCaseIds': test_case_ids}
        if wit_fields:
            params['witFields'] = wit_fields
        if return_identity_ref:
            params['returnIdentityRef'] = return_identity_ref
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/testcases/{test_case_ids}"
        response_data = await self.client.get_json(endpoint, params=params)
        return TestCase(**response_data)
    
    async def add_test_cases_to_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        test_case_ids: List[int]
    ) -> List[TestCase]:
        """
        Add test cases to a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            test_case_ids: List of test case IDs to add
            
        Returns:
            List of added test cases
        """
        test_cases_data = [{"workItem": {"id": tc_id}} for tc_id in test_case_ids]
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/testcases"
        response_data = await self.client.post_json(endpoint, data=test_cases_data)
        return [TestCase(**tc) for tc in response_data.get('value', [])]
    
    async def remove_test_case_from_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        test_case_ids: str
    ) -> None:
        """
        Remove test cases from a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            test_case_ids: Test case IDs to remove
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/testcases/{test_case_ids}"
        await self.client.delete(endpoint)
    
    # Test Points
    async def get_test_points(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        point_ids: Optional[str] = None,
        wit_fields: Optional[str] = None,
        configuration_id: Optional[str] = None,
        test_case_id: Optional[str] = None,
        test_point_ids: Optional[str] = None,
        include_point_details: Optional[bool] = None,
        is_recursive: Optional[bool] = None
    ) -> List[TestPoint]:
        """
        Get test points in a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            point_ids: Specific point IDs
            wit_fields: Work item fields
            configuration_id: Configuration ID
            test_case_id: Test case ID
            test_point_ids: Test point IDs
            include_point_details: Include point details
            is_recursive: Include child suites
            
        Returns:
            List of test points
        """
        params = {}
        if point_ids:
            params['pointIds'] = point_ids
        if wit_fields:
            params['witFields'] = wit_fields
        if configuration_id:
            params['configurationId'] = configuration_id
        if test_case_id:
            params['testCaseId'] = test_case_id
        if test_point_ids:
            params['testPointIds'] = test_point_ids
        if include_point_details:
            params['includePointDetails'] = include_point_details
        if is_recursive:
            params['isRecursive'] = is_recursive
        
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/points"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestPointsResponse(**response_data)
        return response.value
    
    async def update_test_points(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        point_update_model: Dict[str, Any]
    ) -> List[TestPoint]:
        """
        Update test points.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            point_update_model: Point update data
            
        Returns:
            List of updated test points
        """
        endpoint = f"projects/{project}/test/plans/{plan_id}/suites/{suite_id}/points"
        response_data = await self.client.patch_json(endpoint, data=point_update_model)
        return [TestPoint(**point) for point in response_data.get('value', [])]
    
    # Test Runs
    async def list_test_runs(
        self,
        project: str,
        build_uri: Optional[str] = None,
        owner: Optional[str] = None,
        tmi_run_id: Optional[str] = None,
        plan_id: Optional[int] = None,
        include_run_details: Optional[bool] = None,
        automated: Optional[bool] = None,
        skip: Optional[int] = None,
        top: Optional[int] = None
    ) -> List[TestRun]:
        """
        List test runs in a project.
        
        Args:
            project: Project ID or name
            build_uri: Build URI filter
            owner: Owner filter
            tmi_run_id: TMI run ID filter
            plan_id: Test plan ID filter
            include_run_details: Include run details
            automated: Automated runs filter
            skip: Number of runs to skip
            top: Maximum number of runs
            
        Returns:
            List of test runs
        """
        params = {}
        if build_uri:
            params['buildUri'] = build_uri
        if owner:
            params['owner'] = owner
        if tmi_run_id:
            params['tmiRunId'] = tmi_run_id
        if plan_id:
            params['planId'] = plan_id
        if include_run_details:
            params['includeRunDetails'] = include_run_details
        if automated is not None:
            params['automated'] = automated
        if skip:
            params['$skip'] = skip
        if top:
            params['$top'] = top
        
        endpoint = f"projects/{project}/test/runs"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestRunsResponse(**response_data)
        return response.value
    
    async def get_test_run(
        self,
        project: str,
        run_id: int,
        include_details: Optional[bool] = None
    ) -> TestRun:
        """
        Get a specific test run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            include_details: Include run details
            
        Returns:
            Test run details
        """
        params = {}
        if include_details:
            params['includeDetails'] = include_details
        
        endpoint = f"projects/{project}/test/runs/{run_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return TestRun(**response_data)
    
    async def create_test_run(
        self,
        project: str,
        run_data: Dict[str, Any]
    ) -> TestRun:
        """
        Create a new test run.
        
        Args:
            project: Project ID or name
            run_data: Test run creation data
            
        Returns:
            Created test run
        """
        endpoint = f"projects/{project}/test/runs"
        response_data = await self.client.post_json(endpoint, data=run_data)
        return TestRun(**response_data)
    
    async def update_test_run(
        self,
        project: str,
        run_id: int,
        run_data: Dict[str, Any]
    ) -> TestRun:
        """
        Update a test run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            run_data: Test run update data
            
        Returns:
            Updated test run
        """
        endpoint = f"projects/{project}/test/runs/{run_id}"
        response_data = await self.client.patch_json(endpoint, data=run_data)
        return TestRun(**response_data)
    
    async def delete_test_run(
        self,
        project: str,
        run_id: int
    ) -> None:
        """
        Delete a test run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
        """
        endpoint = f"projects/{project}/test/runs/{run_id}"
        await self.client.delete(endpoint)
    
    # Test Results
    async def get_test_results(
        self,
        project: str,
        run_id: int,
        details_to_include: Optional[str] = None,
        skip: Optional[int] = None,
        top: Optional[int] = None,
        outcomes: Optional[List[str]] = None
    ) -> List[TestResult]:
        """
        Get test results for a test run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            details_to_include: Details to include
            skip: Number of results to skip
            top: Maximum number of results
            outcomes: Outcome filters
            
        Returns:
            List of test results
        """
        params = {}
        if details_to_include:
            params['detailsToInclude'] = details_to_include
        if skip:
            params['$skip'] = skip
        if top:
            params['$top'] = top
        if outcomes:
            params['outcomes'] = ','.join(outcomes)
        
        endpoint = f"projects/{project}/test/runs/{run_id}/results"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestResultsResponse(**response_data)
        return response.value
    
    async def get_test_result(
        self,
        project: str,
        run_id: int,
        test_case_result_id: int,
        details_to_include: Optional[str] = None
    ) -> TestResult:
        """
        Get a specific test result.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            test_case_result_id: Test case result ID
            details_to_include: Details to include
            
        Returns:
            Test result details
        """
        params = {}
        if details_to_include:
            params['detailsToInclude'] = details_to_include
        
        endpoint = f"projects/{project}/test/runs/{run_id}/results/{test_case_result_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return TestResult(**response_data)
    
    async def update_test_results(
        self,
        project: str,
        run_id: int,
        results_data: List[Dict[str, Any]]
    ) -> List[TestResult]:
        """
        Update test results.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            results_data: List of test result updates
            
        Returns:
            List of updated test results
        """
        endpoint = f"projects/{project}/test/runs/{run_id}/results"
        response_data = await self.client.patch_json(endpoint, data=results_data)
        return [TestResult(**result) for result in response_data.get('value', [])]
    
    # Test Configurations
    async def get_test_configurations(
        self,
        project: str,
        continuation_token: Optional[str] = None
    ) -> List[TestConfiguration]:
        """
        Get test configurations.
        
        Args:
            project: Project ID or name
            continuation_token: Continuation token
            
        Returns:
            List of test configurations
        """
        params = {}
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = f"projects/{project}/test/configurations"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TestConfigurationsResponse(**response_data)
        return response.value
    
    async def create_test_configuration(
        self,
        project: str,
        configuration_data: Dict[str, Any]
    ) -> TestConfiguration:
        """
        Create a test configuration.
        
        Args:
            project: Project ID or name
            configuration_data: Configuration creation data
            
        Returns:
            Created test configuration
        """
        endpoint = f"projects/{project}/test/configurations"
        response_data = await self.client.post_json(endpoint, data=configuration_data)
        return TestConfiguration(**response_data)
    
    # Test Attachments
    async def create_test_result_attachment(
        self,
        project: str,
        run_id: int,
        test_case_result_id: int,
        attachment_request_model: Dict[str, Any]
    ) -> TestAttachment:
        """
        Create a test result attachment.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            test_case_result_id: Test case result ID
            attachment_request_model: Attachment data
            
        Returns:
            Created test attachment
        """
        endpoint = f"projects/{project}/test/runs/{run_id}/results/{test_case_result_id}/attachments"
        response_data = await self.client.post_json(endpoint, data=attachment_request_model)
        return TestAttachment(**response_data)
    
    async def get_test_result_attachments(
        self,
        project: str,
        run_id: int,
        test_case_result_id: int
    ) -> List[TestAttachment]:
        """
        Get test result attachments.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            test_case_result_id: Test case result ID
            
        Returns:
            List of test attachments
        """
        endpoint = f"projects/{project}/test/runs/{run_id}/results/{test_case_result_id}/attachments"
        response_data = await self.client.get_json(endpoint)
        attachments = response_data.get('value', [])
        return [TestAttachment(**attachment) for attachment in attachments]
    
    # Test Run Statistics
    async def get_test_run_statistics(
        self,
        project: str,
        run_id: int
    ) -> TestRunStatistic:
        """
        Get test run statistics.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            
        Returns:
            Test run statistics
        """
        endpoint = f"projects/{project}/test/runs/{run_id}/statistics"
        response_data = await self.client.get_json(endpoint)
        return TestRunStatistic(**response_data)
    
    # Utility methods
    async def run_tests_from_suite(
        self,
        project: str,
        plan_id: int,
        suite_id: int,
        configuration_ids: Optional[List[int]] = None,
        run_name: Optional[str] = None,
        build_id: Optional[int] = None
    ) -> TestRun:
        """
        Create and start a test run from a test suite.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            suite_id: Test suite ID
            configuration_ids: Configuration IDs
            run_name: Test run name
            build_id: Build ID
            
        Returns:
            Created test run
        """
        # Get test points from the suite
        test_points = await self.get_test_points(
            project=project,
            plan_id=plan_id,
            suite_id=suite_id,
            configuration_id=','.join(map(str, configuration_ids)) if configuration_ids else None
        )
        
        # Create run data
        run_data = {
            "name": run_name or f"Test Run from Suite {suite_id}",
            "plan": {"id": plan_id},
            "pointIds": [point.id for point in test_points if point.id],
            "state": "inProgress"
        }
        
        if build_id:
            run_data["build"] = {"id": build_id}
        
        return await self.create_test_run(project=project, run_data=run_data)
    
    async def complete_test_run(
        self,
        project: str,
        run_id: int,
        comment: Optional[str] = None
    ) -> TestRun:
        """
        Complete a test run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            comment: Completion comment
            
        Returns:
            Completed test run
        """
        update_data = {"state": "completed"}
        if comment:
            update_data["comment"] = comment
        
        return await self.update_test_run(
            project=project,
            run_id=run_id,
            run_data=update_data
        )
    
    async def pass_test_result(
        self,
        project: str,
        run_id: int,
        test_case_result_id: int,
        comment: Optional[str] = None
    ) -> TestResult:
        """
        Mark a test result as passed.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            test_case_result_id: Test case result ID
            comment: Pass comment
            
        Returns:
            Updated test result
        """
        result_data = {
            "id": test_case_result_id,
            "outcome": "Passed",
            "state": "Completed"
        }
        if comment:
            result_data["comment"] = comment
        
        results = await self.update_test_results(
            project=project,
            run_id=run_id,
            results_data=[result_data]
        )
        return results[0] if results else None
    
    async def fail_test_result(
        self,
        project: str,
        run_id: int,
        test_case_result_id: int,
        comment: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> TestResult:
        """
        Mark a test result as failed.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            test_case_result_id: Test case result ID
            comment: Fail comment
            error_message: Error message
            
        Returns:
            Updated test result
        """
        result_data = {
            "id": test_case_result_id,
            "outcome": "Failed",
            "state": "Completed"
        }
        if comment:
            result_data["comment"] = comment
        if error_message:
            result_data["errorMessage"] = error_message
        
        results = await self.update_test_results(
            project=project,
            run_id=run_id,
            results_data=[result_data]
        )
        return results[0] if results else None
    
    async def get_test_plan_summary(
        self,
        project: str,
        plan_id: int
    ) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a test plan.
        
        Args:
            project: Project ID or name
            plan_id: Test plan ID
            
        Returns:
            Test plan summary with suites, cases, and recent runs
        """
        # Get the test plan
        plan = await self.get_test_plan(project=project, plan_id=plan_id)
        
        # Get test suites
        try:
            suites = await self.list_test_suites(project=project, plan_id=plan_id)
        except Exception:
            suites = []
        
        # Get recent test runs
        try:
            runs = await self.list_test_runs(
                project=project,
                plan_id=plan_id,
                top=10
            )
        except Exception:
            runs = []
        
        # Count test cases across all suites
        total_test_cases = 0
        for suite in suites:
            try:
                cases = await self.list_test_cases(
                    project=project,
                    plan_id=plan_id,
                    suite_id=suite.id
                )
                total_test_cases += len(cases)
            except Exception:
                continue
        
        return {
            "plan": plan,
            "suites": suites,
            "recent_runs": runs,
            "summary": {
                "plan_id": plan_id,
                "plan_name": plan.name,
                "suite_count": len(suites),
                "total_test_cases": total_test_cases,
                "recent_run_count": len(runs),
                "state": plan.state
            }
        }
    
    async def iterate_test_results(
        self,
        project: str,
        run_id: int,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[TestResult, None]:
        """
        Iterate through all test results in a run.
        
        Args:
            project: Project ID or name
            run_id: Test run ID
            page_size: Number of results per page
            
        Yields:
            Test results one by one
        """
        async def request_func(**params):
            results = await self.get_test_results(
                project=project,
                run_id=run_id,
                top=page_size,
                **params,
                **kwargs
            )
            return {"value": results, "count": len(results)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for result in paginator.iterate_items():
            yield result
