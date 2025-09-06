"""
Governance engine - Core governance policy evaluation and enforcement
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)


class GovernanceEngine:
    """Core governance policy engine"""
    
    def __init__(self):
        self.policies = {}
        self.rules = {}
        
    async def evaluate_policies(
        self,
        context: Dict[str, Any],
        policy_set: str = "default"
    ) -> Dict[str, Any]:
        """Evaluate governance policies against context"""
        
        results = {
            "policy_set": policy_set,
            "evaluation_date": datetime.utcnow().isoformat(),
            "context": context,
            "results": [],
            "violations": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Example policy evaluations
        if context.get("type") == "pull_request":
            pr_result = await self._evaluate_pull_request(context)
            results["results"].append(pr_result)
            
        elif context.get("type") == "pipeline":
            pipeline_result = await self._evaluate_pipeline(context)
            results["results"].append(pipeline_result)
            
        elif context.get("type") == "work_item":
            work_item_result = await self._evaluate_work_item(context)
            results["results"].append(work_item_result)
        
        return results
    
    async def _evaluate_pull_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate pull request governance"""
        
        violations = []
        warnings = []
        recommendations = []
        
        # Check for required reviewers
        reviewers = context.get("reviewers", [])
        if len(reviewers) < 2:
            violations.append({
                "rule": "PR_MIN_REVIEWERS",
                "message": "Pull request requires at least 2 reviewers",
                "severity": "high"
            })
        
        # Check for linked work items
        work_items = context.get("work_items", [])
        if not work_items:
            warnings.append({
                "rule": "PR_LINKED_WORK_ITEM",
                "message": "Pull request should be linked to work item",
                "severity": "medium"
            })
        
        # Check for automated tests
        has_tests = context.get("has_tests", False)
        if not has_tests:
            recommendations.append({
                "rule": "PR_AUTOMATED_TESTS",
                "message": "Consider adding automated tests",
                "severity": "low"
            })
        
        return {
            "type": "pull_request",
            "status": "evaluated",
            "violations": violations,
            "warnings": warnings,
            "recommendations": recommendations
        }
    
    async def _evaluate_pipeline(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate pipeline governance"""
        
        violations = []
        warnings = []
        recommendations = []
        
        # Check for security scanning
        has_security_scan = context.get("has_security_scan", False)
        if not has_security_scan:
            violations.append({
                "rule": "PIPELINE_SECURITY_SCAN",
                "message": "Pipeline must include security scanning",
                "severity": "high"
            })
        
        # Check for automated testing
        has_tests = context.get("has_tests", False)
        if not has_tests:
            warnings.append({
                "rule": "PIPELINE_AUTOMATED_TESTS",
                "message": "Pipeline should include automated tests",
                "severity": "medium"
            })
        
        # Check for deployment approvals
        has_approvals = context.get("has_approvals", False)
        if not has_approvals:
            recommendations.append({
                "rule": "PIPELINE_DEPLOYMENT_APPROVALS",
                "message": "Consider adding deployment approvals for production",
                "severity": "low"
            })
        
        return {
            "type": "pipeline",
            "status": "evaluated",
            "violations": violations,
            "warnings": warnings,
            "recommendations": recommendations
        }
    
    async def _evaluate_work_item(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work item governance"""
        
        violations = []
        warnings = []
        recommendations = []
        
        # Check for proper categorization
        area_path = context.get("area_path")
        if not area_path:
            violations.append({
                "rule": "WORK_ITEM_AREA_PATH",
                "message": "Work item must have area path assigned",
                "severity": "medium"
            })
        
        # Check for effort estimation
        effort = context.get("effort")
        if not effort:
            warnings.append({
                "rule": "WORK_ITEM_EFFORT",
                "message": "Work item should have effort estimation",
                "severity": "low"
            })
        
        # Check for acceptance criteria
        acceptance_criteria = context.get("acceptance_criteria")
        if not acceptance_criteria:
            recommendations.append({
                "rule": "WORK_ITEM_ACCEPTANCE_CRITERIA",
                "message": "Consider adding acceptance criteria",
                "severity": "low"
            })
        
        return {
            "type": "work_item",
            "status": "evaluated",
            "violations": violations,
            "warnings": warnings,
            "recommendations": recommendations
        }
    
    async def enforce_policy(
        self,
        policy_id: str,
        context: Dict[str, Any],
        action: str = "block"
    ) -> Dict[str, Any]:
        """Enforce specific governance policy"""
        
        logger.info(
            "Enforcing governance policy",
            policy_id=policy_id,
            action=action,
            context_type=context.get("type")
        )
        
        enforcement_result = {
            "policy_id": policy_id,
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "result": "success",
            "message": f"Policy {policy_id} enforced with action: {action}"
        }
        
        # Placeholder enforcement logic
        if action == "block":
            enforcement_result["blocked"] = True
        elif action == "warn":
            enforcement_result["warning_sent"] = True
        elif action == "notify":
            enforcement_result["notification_sent"] = True
        
        return enforcement_result
    
    async def get_policy_metrics(self) -> Dict[str, Any]:
        """Get governance policy metrics"""
        
        return {
            "total_policies": len(self.policies),
            "active_policies": len([p for p in self.policies.values() if p.get("enabled", True)]),
            "total_rules": len(self.rules),
            "recent_violations": 0,  # Placeholder
            "compliance_score": 85.5,  # Placeholder
            "last_updated": datetime.utcnow().isoformat()
        }
