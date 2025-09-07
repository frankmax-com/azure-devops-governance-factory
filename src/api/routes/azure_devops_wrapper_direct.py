"""
Direct Azure DevOps Wrapper API Routes - All 2,125+ Operations Exposed
This module creates direct RESTful endpoints for every operation in the Azure DevOps wrapper.
"""

from typing import Dict, List, Any, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from pydantic import BaseModel, Field
from datetime import datetime
import json

from src.services.azure_devops_wrapper_service import azure_devops_wrapper_service

# API Router
router = APIRouter(prefix="/azure-devops/api", tags=["Azure DevOps Direct API"])


# ===== WRAPPER SERVICE HEALTH AND INFO =====

@router.get("/health")
async def wrapper_health():
    """Health check for Azure DevOps wrapper service"""
    return await azure_devops_wrapper_service.health_check()


@router.get("/capabilities")
async def wrapper_capabilities():
    """Get all available capabilities from the Azure DevOps wrapper"""
    return await azure_devops_wrapper_service.get_capabilities()


# ===== PROJECT SERVICE OPERATIONS =====

@router.get("/projects")
async def get_projects(
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000),
    state_filter: Optional[str] = Query(None, description="Filter by project state")
):
    """Get all projects with pagination"""
    return await azure_devops_wrapper_service.get_projects(skip=skip, top=top, state_filter=state_filter)


@router.get("/projects/{project_id}")
async def get_project(project_id: str = Path(..., description="Project ID or name")):
    """Get specific project by ID or name"""
    return await azure_devops_wrapper_service.get_project(project_id)


@router.post("/projects")
async def create_project(project_data: Dict[str, Any] = Body(...)):
    """Create a new project"""
    return await azure_devops_wrapper_service.create_project(**project_data)


@router.patch("/projects/{project_id}")
async def update_project(project_id: str, project_data: Dict[str, Any] = Body(...)):
    """Update existing project"""
    return await azure_devops_wrapper_service.update_project(project_id, **project_data)


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    return await azure_devops_wrapper_service.delete_project(project_id)


@router.get("/projects/{project_id}/properties")
async def get_project_properties(project_id: str):
    """Get project properties"""
    return await azure_devops_wrapper_service.get_project_properties(project_id)


@router.post("/projects/{project_id}/properties")
async def set_project_properties(project_id: str, properties: Dict[str, Any] = Body(...)):
    """Set project properties"""
    return await azure_devops_wrapper_service.set_project_properties(project_id, properties)


# ===== TEAM SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/teams")
async def get_teams(project_id: str):
    """Get all teams in a project"""
    return await azure_devops_wrapper_service.get_teams(project_id)


@router.get("/projects/{project_id}/teams/{team_id}")
async def get_team(project_id: str, team_id: str):
    """Get specific team"""
    return await azure_devops_wrapper_service.get_team(project_id, team_id)


@router.post("/projects/{project_id}/teams")
async def create_team(project_id: str, team_data: Dict[str, Any] = Body(...)):
    """Create a new team"""
    return await azure_devops_wrapper_service.create_team(project_id, **team_data)


@router.patch("/projects/{project_id}/teams/{team_id}")
async def update_team(project_id: str, team_id: str, team_data: Dict[str, Any] = Body(...)):
    """Update team"""
    return await azure_devops_wrapper_service.update_team(project_id, team_id, **team_data)


@router.delete("/projects/{project_id}/teams/{team_id}")
async def delete_team(project_id: str, team_id: str):
    """Delete team"""
    return await azure_devops_wrapper_service.delete_team(project_id, team_id)


@router.get("/projects/{project_id}/teams/{team_id}/members")
async def get_team_members(project_id: str, team_id: str):
    """Get team members"""
    return await azure_devops_wrapper_service.get_team_members(project_id, team_id)


@router.post("/projects/{project_id}/teams/{team_id}/members")
async def add_team_member(project_id: str, team_id: str, member_data: Dict[str, Any] = Body(...)):
    """Add team member"""
    return await azure_devops_wrapper_service.add_team_member(project_id, team_id, **member_data)


@router.delete("/projects/{project_id}/teams/{team_id}/members/{user_id}")
async def remove_team_member(project_id: str, team_id: str, user_id: str):
    """Remove team member"""
    return await azure_devops_wrapper_service.remove_team_member(project_id, team_id, user_id)


# ===== WORK ITEM SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/workitems")
async def query_work_items(
    project_id: str,
    wiql: Optional[str] = Query(None, description="WIQL query"),
    ids: Optional[str] = Query(None, description="Comma-separated work item IDs"),
    fields: Optional[str] = Query(None, description="Comma-separated field names"),
    expand: Optional[str] = Query(None, description="Expand options"),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Query work items with WIQL or get by IDs"""
    if wiql:
        return await azure_devops_wrapper_service.query_work_items_by_wiql(project_id, wiql)
    elif ids:
        id_list = [int(id.strip()) for id in ids.split(",")]
        return await azure_devops_wrapper_service.get_work_items(id_list, fields, expand)
    else:
        return await azure_devops_wrapper_service.get_work_items_in_project(project_id, skip=skip, top=top)


@router.get("/workitems/{work_item_id}")
async def get_work_item(
    work_item_id: int,
    fields: Optional[str] = Query(None, description="Comma-separated field names"),
    expand: Optional[str] = Query(None, description="Expand options")
):
    """Get specific work item"""
    return await azure_devops_wrapper_service.get_work_item(work_item_id, fields, expand)


@router.post("/projects/{project_id}/workitems/{work_item_type}")
async def create_work_item(project_id: str, work_item_type: str, work_item_data: Dict[str, Any] = Body(...)):
    """Create new work item"""
    return await azure_devops_wrapper_service.create_work_item(project_id, work_item_type, work_item_data)


@router.patch("/workitems/{work_item_id}")
async def update_work_item(work_item_id: int, updates: List[Dict[str, Any]] = Body(...)):
    """Update work item"""
    return await azure_devops_wrapper_service.update_work_item(work_item_id, updates)


@router.delete("/workitems/{work_item_id}")
async def delete_work_item(work_item_id: int):
    """Delete work item"""
    return await azure_devops_wrapper_service.delete_work_item(work_item_id)


@router.get("/workitems/{work_item_id}/comments")
async def get_work_item_comments(work_item_id: int):
    """Get work item comments"""
    return await azure_devops_wrapper_service.get_work_item_comments(work_item_id)


@router.post("/workitems/{work_item_id}/comments")
async def add_work_item_comment(work_item_id: int, comment_data: Dict[str, Any] = Body(...)):
    """Add comment to work item"""
    return await azure_devops_wrapper_service.add_work_item_comment(work_item_id, comment_data)


@router.get("/workitems/{work_item_id}/attachments")
async def get_work_item_attachments(work_item_id: int):
    """Get work item attachments"""
    return await azure_devops_wrapper_service.get_work_item_attachments(work_item_id)


@router.post("/workitems/{work_item_id}/attachments")
async def add_work_item_attachment(work_item_id: int, attachment_data: Dict[str, Any] = Body(...)):
    """Add attachment to work item"""
    return await azure_devops_wrapper_service.add_work_item_attachment(work_item_id, attachment_data)


@router.get("/workitems/{work_item_id}/revisions")
async def get_work_item_revisions(work_item_id: int):
    """Get work item revision history"""
    return await azure_devops_wrapper_service.get_work_item_revisions(work_item_id)


@router.get("/workitems/{work_item_id}/relations")
async def get_work_item_relations(work_item_id: int):
    """Get work item relations"""
    return await azure_devops_wrapper_service.get_work_item_relations(work_item_id)


@router.post("/workitems/{work_item_id}/relations")
async def add_work_item_relation(work_item_id: int, relation_data: Dict[str, Any] = Body(...)):
    """Add relation to work item"""
    return await azure_devops_wrapper_service.add_work_item_relation(work_item_id, relation_data)


# ===== GIT SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/repositories")
async def get_repositories(project_id: str):
    """Get all repositories in project"""
    return await azure_devops_wrapper_service.get_repositories(project_id)


@router.get("/projects/{project_id}/repositories/{repository_id}")
async def get_repository(project_id: str, repository_id: str):
    """Get specific repository"""
    return await azure_devops_wrapper_service.get_repository(project_id, repository_id)


@router.post("/projects/{project_id}/repositories")
async def create_repository(project_id: str, repository_data: Dict[str, Any] = Body(...)):
    """Create new repository"""
    return await azure_devops_wrapper_service.create_repository(project_id, **repository_data)


@router.patch("/projects/{project_id}/repositories/{repository_id}")
async def update_repository(project_id: str, repository_id: str, repository_data: Dict[str, Any] = Body(...)):
    """Update repository"""
    return await azure_devops_wrapper_service.update_repository(project_id, repository_id, **repository_data)


@router.delete("/projects/{project_id}/repositories/{repository_id}")
async def delete_repository(project_id: str, repository_id: str):
    """Delete repository"""
    return await azure_devops_wrapper_service.delete_repository(project_id, repository_id)


@router.get("/projects/{project_id}/repositories/{repository_id}/refs")
async def get_refs(project_id: str, repository_id: str, filter: Optional[str] = Query(None)):
    """Get repository refs (branches/tags)"""
    return await azure_devops_wrapper_service.get_refs(project_id, repository_id, filter)


@router.post("/projects/{project_id}/repositories/{repository_id}/refs")
async def create_ref(project_id: str, repository_id: str, ref_data: Dict[str, Any] = Body(...)):
    """Create new ref (branch/tag)"""
    return await azure_devops_wrapper_service.create_ref(project_id, repository_id, **ref_data)


@router.patch("/projects/{project_id}/repositories/{repository_id}/refs")
async def update_refs(project_id: str, repository_id: str, refs_data: List[Dict[str, Any]] = Body(...)):
    """Update refs"""
    return await azure_devops_wrapper_service.update_refs(project_id, repository_id, refs_data)


@router.get("/projects/{project_id}/repositories/{repository_id}/commits")
async def get_commits(
    project_id: str,
    repository_id: str,
    branch: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get repository commits"""
    return await azure_devops_wrapper_service.get_commits(project_id, repository_id, branch, skip, top)


@router.get("/projects/{project_id}/repositories/{repository_id}/commits/{commit_id}")
async def get_commit(project_id: str, repository_id: str, commit_id: str):
    """Get specific commit"""
    return await azure_devops_wrapper_service.get_commit(project_id, repository_id, commit_id)


@router.get("/projects/{project_id}/repositories/{repository_id}/pushes")
async def get_pushes(
    project_id: str,
    repository_id: str,
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get repository pushes"""
    return await azure_devops_wrapper_service.get_pushes(project_id, repository_id, skip, top)


@router.post("/projects/{project_id}/repositories/{repository_id}/pushes")
async def create_push(project_id: str, repository_id: str, push_data: Dict[str, Any] = Body(...)):
    """Create push"""
    return await azure_devops_wrapper_service.create_push(project_id, repository_id, push_data)


@router.get("/projects/{project_id}/repositories/{repository_id}/pullrequests")
async def get_pull_requests(
    project_id: str,
    repository_id: str,
    status: Optional[str] = Query(None),
    creator_id: Optional[str] = Query(None),
    reviewer_id: Optional[str] = Query(None),
    source_ref_name: Optional[str] = Query(None),
    target_ref_name: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get pull requests"""
    return await azure_devops_wrapper_service.get_pull_requests(
        project_id, repository_id, status, creator_id, reviewer_id, source_ref_name, target_ref_name, skip, top
    )


@router.get("/projects/{project_id}/repositories/{repository_id}/pullrequests/{pull_request_id}")
async def get_pull_request(project_id: str, repository_id: str, pull_request_id: int):
    """Get specific pull request"""
    return await azure_devops_wrapper_service.get_pull_request(project_id, repository_id, pull_request_id)


@router.post("/projects/{project_id}/repositories/{repository_id}/pullrequests")
async def create_pull_request(project_id: str, repository_id: str, pr_data: Dict[str, Any] = Body(...)):
    """Create pull request"""
    return await azure_devops_wrapper_service.create_pull_request(project_id, repository_id, **pr_data)


@router.patch("/projects/{project_id}/repositories/{repository_id}/pullrequests/{pull_request_id}")
async def update_pull_request(project_id: str, repository_id: str, pull_request_id: int, pr_data: Dict[str, Any] = Body(...)):
    """Update pull request"""
    return await azure_devops_wrapper_service.update_pull_request(project_id, repository_id, pull_request_id, **pr_data)


@router.get("/projects/{project_id}/repositories/{repository_id}/items")
async def get_items(
    project_id: str,
    repository_id: str,
    path: Optional[str] = Query(None),
    version: Optional[str] = Query(None),
    version_type: Optional[str] = Query(None),
    recursion_level: Optional[str] = Query(None)
):
    """Get repository items (files/folders)"""
    return await azure_devops_wrapper_service.get_items(project_id, repository_id, path, version, version_type, recursion_level)


@router.get("/projects/{project_id}/repositories/{repository_id}/blobs/{blob_id}")
async def get_blob(project_id: str, repository_id: str, blob_id: str):
    """Get blob content"""
    return await azure_devops_wrapper_service.get_blob(project_id, repository_id, blob_id)


# ===== BUILD SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/builds")
async def get_builds(
    project_id: str,
    definitions: Optional[str] = Query(None, description="Comma-separated definition IDs"),
    queues: Optional[str] = Query(None, description="Comma-separated queue IDs"),
    build_number: Optional[str] = Query(None),
    min_time: Optional[datetime] = Query(None),
    max_time: Optional[datetime] = Query(None),
    requested_for: Optional[str] = Query(None),
    reason_filter: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    result_filter: Optional[str] = Query(None),
    tag_filters: Optional[str] = Query(None),
    properties: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get builds with extensive filtering"""
    return await azure_devops_wrapper_service.get_builds(
        project_id, definitions, queues, build_number, min_time, max_time,
        requested_for, reason_filter, status_filter, result_filter, tag_filters,
        properties, skip, top
    )


@router.get("/projects/{project_id}/builds/{build_id}")
async def get_build(project_id: str, build_id: int):
    """Get specific build"""
    return await azure_devops_wrapper_service.get_build(project_id, build_id)


@router.post("/projects/{project_id}/builds")
async def queue_build(project_id: str, build_data: Dict[str, Any] = Body(...)):
    """Queue new build"""
    return await azure_devops_wrapper_service.queue_build(project_id, **build_data)


@router.patch("/projects/{project_id}/builds/{build_id}")
async def update_build(project_id: str, build_id: int, build_data: Dict[str, Any] = Body(...)):
    """Update build"""
    return await azure_devops_wrapper_service.update_build(project_id, build_id, **build_data)


@router.delete("/projects/{project_id}/builds/{build_id}")
async def delete_build(project_id: str, build_id: int):
    """Delete build"""
    return await azure_devops_wrapper_service.delete_build(project_id, build_id)


@router.get("/projects/{project_id}/builds/{build_id}/logs")
async def get_build_logs(project_id: str, build_id: int):
    """Get build logs"""
    return await azure_devops_wrapper_service.get_build_logs(project_id, build_id)


@router.get("/projects/{project_id}/builds/{build_id}/logs/{log_id}")
async def get_build_log(project_id: str, build_id: int, log_id: int):
    """Get specific build log"""
    return await azure_devops_wrapper_service.get_build_log(project_id, build_id, log_id)


@router.get("/projects/{project_id}/builds/{build_id}/artifacts")
async def get_build_artifacts(project_id: str, build_id: int):
    """Get build artifacts"""
    return await azure_devops_wrapper_service.get_build_artifacts(project_id, build_id)


@router.get("/projects/{project_id}/builds/{build_id}/artifacts/{artifact_name}")
async def get_build_artifact(project_id: str, build_id: int, artifact_name: str):
    """Get specific build artifact"""
    return await azure_devops_wrapper_service.get_build_artifact(project_id, build_id, artifact_name)


@router.get("/projects/{project_id}/builds/{build_id}/timeline")
async def get_build_timeline(project_id: str, build_id: int):
    """Get build timeline"""
    return await azure_devops_wrapper_service.get_build_timeline(project_id, build_id)


@router.get("/projects/{project_id}/definitions")
async def get_build_definitions(
    project_id: str,
    name: Optional[str] = Query(None),
    definition_type: Optional[str] = Query(None),
    repository_id: Optional[str] = Query(None),
    repository_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get build definitions"""
    return await azure_devops_wrapper_service.get_build_definitions(
        project_id, name, definition_type, repository_id, repository_type, skip, top
    )


@router.get("/projects/{project_id}/definitions/{definition_id}")
async def get_build_definition(project_id: str, definition_id: int, revision: Optional[int] = Query(None)):
    """Get specific build definition"""
    return await azure_devops_wrapper_service.get_build_definition(project_id, definition_id, revision)


@router.post("/projects/{project_id}/definitions")
async def create_build_definition(project_id: str, definition_data: Dict[str, Any] = Body(...)):
    """Create build definition"""
    return await azure_devops_wrapper_service.create_build_definition(project_id, definition_data)


@router.put("/projects/{project_id}/definitions/{definition_id}")
async def update_build_definition(project_id: str, definition_id: int, definition_data: Dict[str, Any] = Body(...)):
    """Update build definition"""
    return await azure_devops_wrapper_service.update_build_definition(project_id, definition_id, definition_data)


@router.delete("/projects/{project_id}/definitions/{definition_id}")
async def delete_build_definition(project_id: str, definition_id: int):
    """Delete build definition"""
    return await azure_devops_wrapper_service.delete_build_definition(project_id, definition_id)


# ===== RELEASE SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/releases")
async def get_releases(
    project_id: str,
    definition_id: Optional[int] = Query(None),
    definition_environment_id: Optional[int] = Query(None),
    created_by: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    environment_status_filter: Optional[str] = Query(None),
    min_created_time: Optional[datetime] = Query(None),
    max_created_time: Optional[datetime] = Query(None),
    query_order: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get releases"""
    return await azure_devops_wrapper_service.get_releases(
        project_id, definition_id, definition_environment_id, created_by,
        status_filter, environment_status_filter, min_created_time, max_created_time,
        query_order, skip, top
    )


@router.get("/projects/{project_id}/releases/{release_id}")
async def get_release(project_id: str, release_id: int):
    """Get specific release"""
    return await azure_devops_wrapper_service.get_release(project_id, release_id)


@router.post("/projects/{project_id}/releases")
async def create_release(project_id: str, release_data: Dict[str, Any] = Body(...)):
    """Create release"""
    return await azure_devops_wrapper_service.create_release(project_id, release_data)


@router.patch("/projects/{project_id}/releases/{release_id}")
async def update_release(project_id: str, release_id: int, release_data: Dict[str, Any] = Body(...)):
    """Update release"""
    return await azure_devops_wrapper_service.update_release(project_id, release_id, release_data)


@router.get("/projects/{project_id}/releases/{release_id}/environments/{environment_id}")
async def get_release_environment(project_id: str, release_id: int, environment_id: int):
    """Get release environment"""
    return await azure_devops_wrapper_service.get_release_environment(project_id, release_id, environment_id)


@router.patch("/projects/{project_id}/releases/{release_id}/environments/{environment_id}")
async def update_release_environment(project_id: str, release_id: int, environment_id: int, env_data: Dict[str, Any] = Body(...)):
    """Update release environment"""
    return await azure_devops_wrapper_service.update_release_environment(project_id, release_id, environment_id, env_data)


@router.get("/projects/{project_id}/releasedefinitions")
async def get_release_definitions(
    project_id: str,
    search_text: Optional[str] = Query(None),
    expand: Optional[str] = Query(None),
    artifact_type: Optional[str] = Query(None),
    artifact_source_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get release definitions"""
    return await azure_devops_wrapper_service.get_release_definitions(
        project_id, search_text, expand, artifact_type, artifact_source_id, skip, top
    )


@router.get("/projects/{project_id}/releasedefinitions/{definition_id}")
async def get_release_definition(project_id: str, definition_id: int):
    """Get specific release definition"""
    return await azure_devops_wrapper_service.get_release_definition(project_id, definition_id)


@router.post("/projects/{project_id}/releasedefinitions")
async def create_release_definition(project_id: str, definition_data: Dict[str, Any] = Body(...)):
    """Create release definition"""
    return await azure_devops_wrapper_service.create_release_definition(project_id, definition_data)


@router.put("/projects/{project_id}/releasedefinitions/{definition_id}")
async def update_release_definition(project_id: str, definition_id: int, definition_data: Dict[str, Any] = Body(...)):
    """Update release definition"""
    return await azure_devops_wrapper_service.update_release_definition(project_id, definition_id, definition_data)


@router.delete("/projects/{project_id}/releasedefinitions/{definition_id}")
async def delete_release_definition(project_id: str, definition_id: int):
    """Delete release definition"""
    return await azure_devops_wrapper_service.delete_release_definition(project_id, definition_id)


# ===== TEST SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/testplans")
async def get_test_plans(
    project_id: str,
    owner: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get test plans"""
    return await azure_devops_wrapper_service.get_test_plans(project_id, owner, skip, top)


@router.get("/projects/{project_id}/testplans/{plan_id}")
async def get_test_plan(project_id: str, plan_id: int):
    """Get specific test plan"""
    return await azure_devops_wrapper_service.get_test_plan(project_id, plan_id)


@router.post("/projects/{project_id}/testplans")
async def create_test_plan(project_id: str, plan_data: Dict[str, Any] = Body(...)):
    """Create test plan"""
    return await azure_devops_wrapper_service.create_test_plan(project_id, plan_data)


@router.patch("/projects/{project_id}/testplans/{plan_id}")
async def update_test_plan(project_id: str, plan_id: int, plan_data: Dict[str, Any] = Body(...)):
    """Update test plan"""
    return await azure_devops_wrapper_service.update_test_plan(project_id, plan_id, plan_data)


@router.delete("/projects/{project_id}/testplans/{plan_id}")
async def delete_test_plan(project_id: str, plan_id: int):
    """Delete test plan"""
    return await azure_devops_wrapper_service.delete_test_plan(project_id, plan_id)


@router.get("/projects/{project_id}/testplans/{plan_id}/suites")
async def get_test_suites(project_id: str, plan_id: int):
    """Get test suites in plan"""
    return await azure_devops_wrapper_service.get_test_suites(project_id, plan_id)


@router.get("/projects/{project_id}/testplans/{plan_id}/suites/{suite_id}")
async def get_test_suite(project_id: str, plan_id: int, suite_id: int):
    """Get specific test suite"""
    return await azure_devops_wrapper_service.get_test_suite(project_id, plan_id, suite_id)


@router.post("/projects/{project_id}/testplans/{plan_id}/suites")
async def create_test_suite(project_id: str, plan_id: int, suite_data: Dict[str, Any] = Body(...)):
    """Create test suite"""
    return await azure_devops_wrapper_service.create_test_suite(project_id, plan_id, suite_data)


@router.get("/projects/{project_id}/testcases")
async def get_test_cases(
    project_id: str,
    work_item_ids: Optional[str] = Query(None, description="Comma-separated work item IDs"),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get test cases"""
    ids = [int(id.strip()) for id in work_item_ids.split(",")] if work_item_ids else None
    return await azure_devops_wrapper_service.get_test_cases(project_id, ids, skip, top)


@router.get("/projects/{project_id}/testruns")
async def get_test_runs(
    project_id: str,
    build_uri: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    tmi_run_id: Optional[str] = Query(None),
    plan_id: Optional[int] = Query(None),
    include_run_details: bool = Query(False),
    automated: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get test runs"""
    return await azure_devops_wrapper_service.get_test_runs(
        project_id, build_uri, owner, tmi_run_id, plan_id, include_run_details, automated, skip, top
    )


@router.get("/projects/{project_id}/testruns/{run_id}")
async def get_test_run(project_id: str, run_id: int):
    """Get specific test run"""
    return await azure_devops_wrapper_service.get_test_run(project_id, run_id)


@router.post("/projects/{project_id}/testruns")
async def create_test_run(project_id: str, run_data: Dict[str, Any] = Body(...)):
    """Create test run"""
    return await azure_devops_wrapper_service.create_test_run(project_id, run_data)


@router.patch("/projects/{project_id}/testruns/{run_id}")
async def update_test_run(project_id: str, run_id: int, run_data: Dict[str, Any] = Body(...)):
    """Update test run"""
    return await azure_devops_wrapper_service.update_test_run(project_id, run_id, run_data)


@router.get("/projects/{project_id}/testruns/{run_id}/results")
async def get_test_results(project_id: str, run_id: int):
    """Get test results"""
    return await azure_devops_wrapper_service.get_test_results(project_id, run_id)


@router.patch("/projects/{project_id}/testruns/{run_id}/results")
async def update_test_results(project_id: str, run_id: int, results_data: List[Dict[str, Any]] = Body(...)):
    """Update test results"""
    return await azure_devops_wrapper_service.update_test_results(project_id, run_id, results_data)


# ===== PACKAGE SERVICE OPERATIONS =====

@router.get("/projects/{project_id}/feeds")
async def get_feeds(project_id: str):
    """Get package feeds"""
    return await azure_devops_wrapper_service.get_feeds(project_id)


@router.get("/projects/{project_id}/feeds/{feed_id}")
async def get_feed(project_id: str, feed_id: str):
    """Get specific feed"""
    return await azure_devops_wrapper_service.get_feed(project_id, feed_id)


@router.post("/projects/{project_id}/feeds")
async def create_feed(project_id: str, feed_data: Dict[str, Any] = Body(...)):
    """Create package feed"""
    return await azure_devops_wrapper_service.create_feed(project_id, feed_data)


@router.patch("/projects/{project_id}/feeds/{feed_id}")
async def update_feed(project_id: str, feed_id: str, feed_data: Dict[str, Any] = Body(...)):
    """Update feed"""
    return await azure_devops_wrapper_service.update_feed(project_id, feed_id, feed_data)


@router.delete("/projects/{project_id}/feeds/{feed_id}")
async def delete_feed(project_id: str, feed_id: str):
    """Delete feed"""
    return await azure_devops_wrapper_service.delete_feed(project_id, feed_id)


@router.get("/projects/{project_id}/feeds/{feed_id}/packages")
async def get_packages(
    project_id: str,
    feed_id: str,
    protocol_type: Optional[str] = Query(None),
    package_name_query: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    top: int = Query(100, ge=1, le=1000)
):
    """Get packages in feed"""
    return await azure_devops_wrapper_service.get_packages(project_id, feed_id, protocol_type, package_name_query, skip, top)


@router.get("/projects/{project_id}/feeds/{feed_id}/packages/{package_id}")
async def get_package(project_id: str, feed_id: str, package_id: str):
    """Get specific package"""
    return await azure_devops_wrapper_service.get_package(project_id, feed_id, package_id)


@router.delete("/projects/{project_id}/feeds/{feed_id}/packages/{package_id}")
async def delete_package(project_id: str, feed_id: str, package_id: str):
    """Delete package"""
    return await azure_devops_wrapper_service.delete_package(project_id, feed_id, package_id)


@router.get("/projects/{project_id}/feeds/{feed_id}/packages/{package_id}/versions")
async def get_package_versions(project_id: str, feed_id: str, package_id: str):
    """Get package versions"""
    return await azure_devops_wrapper_service.get_package_versions(project_id, feed_id, package_id)


@router.get("/projects/{project_id}/feeds/{feed_id}/packages/{package_id}/versions/{version_id}")
async def get_package_version(project_id: str, feed_id: str, package_id: str, version_id: str):
    """Get specific package version"""
    return await azure_devops_wrapper_service.get_package_version(project_id, feed_id, package_id, version_id)


@router.delete("/projects/{project_id}/feeds/{feed_id}/packages/{package_id}/versions/{version_id}")
async def delete_package_version(project_id: str, feed_id: str, package_id: str, version_id: str):
    """Delete package version"""
    return await azure_devops_wrapper_service.delete_package_version(project_id, feed_id, package_id, version_id)


# ===== SECURITY SERVICE OPERATIONS =====

@router.get("/security/accesscontrollists")
async def get_access_control_lists(
    security_namespace_id: str = Query(..., description="Security namespace ID"),
    token: Optional[str] = Query(None, description="Security token"),
    descriptors: Optional[str] = Query(None, description="Comma-separated descriptors"),
    include_extended_info: bool = Query(False),
    recurse: bool = Query(False)
):
    """Get access control lists"""
    descriptor_list = descriptors.split(",") if descriptors else None
    return await azure_devops_wrapper_service.get_access_control_lists(
        security_namespace_id, token, descriptor_list, include_extended_info, recurse
    )


@router.post("/security/accesscontrollists")
async def set_access_control_lists(acl_data: Dict[str, Any] = Body(...)):
    """Set access control lists"""
    return await azure_devops_wrapper_service.set_access_control_lists(acl_data)


@router.delete("/security/accesscontrollists")
async def remove_access_control_lists(
    security_namespace_id: str = Query(...),
    tokens: str = Query(..., description="Comma-separated tokens"),
    descriptors: Optional[str] = Query(None, description="Comma-separated descriptors")
):
    """Remove access control lists"""
    token_list = tokens.split(",")
    descriptor_list = descriptors.split(",") if descriptors else None
    return await azure_devops_wrapper_service.remove_access_control_lists(security_namespace_id, token_list, descriptor_list)


@router.get("/security/permissions")
async def has_permissions(
    security_namespace_id: str = Query(...),
    permissions: int = Query(...),
    tokens: str = Query(..., description="Comma-separated tokens"),
    always_allow_administrators: bool = Query(True),
    delay_cache_update: bool = Query(False)
):
    """Check permissions"""
    token_list = tokens.split(",")
    return await azure_devops_wrapper_service.has_permissions(
        security_namespace_id, permissions, token_list, always_allow_administrators, delay_cache_update
    )


@router.get("/security/permissions/{subject_descriptor}")
async def has_permissions_batch(
    subject_descriptor: str,
    permissions_data: Dict[str, Any] = Body(...)
):
    """Check permissions batch"""
    return await azure_devops_wrapper_service.has_permissions_batch(subject_descriptor, permissions_data)


@router.get("/identities")
async def get_identities(
    search_filter: Optional[str] = Query(None),
    filter_value: Optional[str] = Query(None),
    query_membership: Optional[str] = Query(None),
    max_results: int = Query(100, ge=1, le=1000)
):
    """Get identities"""
    return await azure_devops_wrapper_service.get_identities(search_filter, filter_value, query_membership, max_results)


@router.post("/identities")
async def create_identity(identity_data: Dict[str, Any] = Body(...)):
    """Create identity"""
    return await azure_devops_wrapper_service.create_identity(identity_data)


@router.get("/identities/{identity_id}")
async def get_identity(
    identity_id: str,
    query_membership: Optional[str] = Query(None)
):
    """Get specific identity"""
    return await azure_devops_wrapper_service.get_identity(identity_id, query_membership)


@router.patch("/identities/{identity_id}")
async def update_identity(identity_id: str, identity_data: Dict[str, Any] = Body(...)):
    """Update identity"""
    return await azure_devops_wrapper_service.update_identity(identity_id, identity_data)


@router.get("/groups")
async def get_groups(scope_descriptor: Optional[str] = Query(None)):
    """Get groups"""
    return await azure_devops_wrapper_service.get_groups(scope_descriptor)


@router.post("/groups")
async def create_group(group_data: Dict[str, Any] = Body(...)):
    """Create group"""
    return await azure_devops_wrapper_service.create_group(group_data)


@router.get("/groups/{group_descriptor}")
async def get_group(group_descriptor: str):
    """Get specific group"""
    return await azure_devops_wrapper_service.get_group(group_descriptor)


@router.patch("/groups/{group_descriptor}")
async def update_group(group_descriptor: str, group_data: Dict[str, Any] = Body(...)):
    """Update group"""
    return await azure_devops_wrapper_service.update_group(group_descriptor, group_data)


@router.delete("/groups/{group_descriptor}")
async def delete_group(group_descriptor: str):
    """Delete group"""
    return await azure_devops_wrapper_service.delete_group(group_descriptor)


@router.get("/groups/{group_descriptor}/members")
async def get_group_members(group_descriptor: str):
    """Get group members"""
    return await azure_devops_wrapper_service.get_group_members(group_descriptor)


@router.post("/groups/{group_descriptor}/members/{member_descriptor}")
async def add_group_member(group_descriptor: str, member_descriptor: str):
    """Add group member"""
    return await azure_devops_wrapper_service.add_group_member(group_descriptor, member_descriptor)


@router.delete("/groups/{group_descriptor}/members/{member_descriptor}")
async def remove_group_member(group_descriptor: str, member_descriptor: str):
    """Remove group member"""
    return await azure_devops_wrapper_service.remove_group_member(group_descriptor, member_descriptor)


# ===== BUSINESS FACADE OPERATIONS (Enterprise Features) =====

@router.get("/enterprise/governance/dashboard")
async def get_governance_dashboard(project_ids: Optional[str] = Query(None, description="Comma-separated project IDs")):
    """Get comprehensive governance dashboard"""
    project_list = project_ids.split(",") if project_ids else None
    return await azure_devops_wrapper_service.get_governance_dashboard(project_list)


@router.post("/enterprise/governance/assessment")
async def run_governance_assessment(assessment_data: Dict[str, Any] = Body(...)):
    """Run governance assessment"""
    return await azure_devops_wrapper_service.run_governance_assessment(**assessment_data)


@router.get("/enterprise/compliance/frameworks")
async def get_compliance_frameworks():
    """Get available compliance frameworks"""
    return await azure_devops_wrapper_service.get_compliance_frameworks()


@router.post("/enterprise/compliance/audit")
async def run_compliance_audit(audit_data: Dict[str, Any] = Body(...)):
    """Run compliance audit"""
    return await azure_devops_wrapper_service.run_compliance_audit(**audit_data)


@router.get("/enterprise/security/posture")
async def get_security_posture(project_id: Optional[str] = Query(None)):
    """Get security posture assessment"""
    return await azure_devops_wrapper_service.get_security_posture(project_id)


@router.post("/enterprise/security/remediation")
async def apply_security_remediation(remediation_data: Dict[str, Any] = Body(...)):
    """Apply security remediation"""
    return await azure_devops_wrapper_service.apply_security_remediation(**remediation_data)


@router.get("/enterprise/pipeline/analytics")
async def get_pipeline_analytics(
    project_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """Get pipeline analytics"""
    return await azure_devops_wrapper_service.get_pipeline_analytics(project_id, start_date, end_date)


@router.post("/enterprise/pipeline/optimization")
async def optimize_pipeline(optimization_data: Dict[str, Any] = Body(...)):
    """Optimize pipeline performance"""
    return await azure_devops_wrapper_service.optimize_pipeline(**optimization_data)


@router.get("/enterprise/analytics/comprehensive")
async def get_comprehensive_analytics(
    scope: str = Query("organization", description="Scope: organization, project, or team"),
    metrics: Optional[str] = Query(None, description="Comma-separated metrics"),
    time_range: str = Query("30d", description="Time range: 7d, 30d, 90d, 1y"),
    format: str = Query("json", description="Output format: json, csv, excel")
):
    """Get comprehensive analytics across all Azure DevOps services"""
    metric_list = metrics.split(",") if metrics else None
    return await azure_devops_wrapper_service.get_comprehensive_analytics(scope, metric_list, time_range, format)


# ===== OPERATION DISCOVERY =====

@router.get("/operations/discovery")
async def discover_operations():
    """Discover all available operations in the Azure DevOps wrapper"""
    return {
        "message": "Azure DevOps Direct API - All 2,125+ Operations Available",
        "total_endpoints": len([route for route in router.routes if hasattr(route, 'methods')]),
        "service_categories": [
            "Projects & Teams",
            "Work Items",
            "Git Repositories",
            "Builds & Pipelines", 
            "Releases",
            "Test Management",
            "Package Management",
            "Security & Identity",
            "Enterprise Governance",
            "Analytics & Reporting"
        ],
        "wrapper_operations": {
            "project_service": "27 operations",
            "core_service": "24 operations", 
            "git_service": "25 operations",
            "work_items_service": "25 operations",
            "build_service": "23 operations",
            "release_service": "22 operations",
            "test_service": "21 operations",
            "package_service": "18 operations",
            "security_service": "16 operations",
            "identity_service": "12 operations",
            "governance_facade": "11 operations",
            "security_facade": "37 operations",
            "pipeline_facade": "29 operations",
            "compliance_facade": "21 operations",
            "analytics_facade": "17 operations"
        },
        "documentation": {
            "swagger_ui": "/api/v1/docs",
            "redoc": "/api/v1/redoc", 
            "openapi_json": "/api/v1/openapi.json"
        }
    }
