"""
Compliance engine - Regulatory framework validation and reporting
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)


class ComplianceEngine:
    """Compliance framework validation engine"""
    
    def __init__(self):
        self.frameworks = {
            "cmmi": CMMLIFramework(),
            "sox": SOXFramework(),
            "gdpr": GDPRFramework(),
            "iso27001": ISO27001Framework()
        }
    
    async def validate_compliance(
        self,
        framework: str,
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate compliance against specific framework"""
        
        if framework not in self.frameworks:
            raise ValueError(f"Unsupported compliance framework: {framework}")
        
        framework_validator = self.frameworks[framework]
        
        return await framework_validator.validate(project_data)
    
    async def generate_compliance_report(
        self,
        framework: str,
        project_id: str,
        validation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate compliance report"""
        
        return {
            "report_id": f"{framework}_{project_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "framework": framework,
            "project_id": project_id,
            "generated_date": datetime.utcnow().isoformat(),
            "validation_results": validation_results,
            "overall_status": validation_results.get("status", "unknown"),
            "compliance_score": validation_results.get("score", 0),
            "recommendations": validation_results.get("recommendations", [])
        }


class BaseComplianceFramework:
    """Base class for compliance frameworks"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.requirements = []
    
    async def validate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate project against framework requirements"""
        raise NotImplementedError


class CMMLIFramework(BaseComplianceFramework):
    """CMMI Level 3+ compliance framework"""
    
    def __init__(self):
        super().__init__("CMMI", "2.0")
        self.level = 3
    
    async def validate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate CMMI compliance"""
        
        violations = []
        score = 100
        
        # Process Area: Requirements Management (REQM)
        if not project_data.get("requirements_traceability", False):
            violations.append({
                "area": "REQM",
                "requirement": "Requirements Traceability",
                "message": "Requirements must be traceable throughout development",
                "severity": "high"
            })
            score -= 15
        
        # Process Area: Project Planning (PP)
        if not project_data.get("project_plan", False):
            violations.append({
                "area": "PP",
                "requirement": "Project Planning",
                "message": "Project must have documented planning",
                "severity": "high"
            })
            score -= 15
        
        # Process Area: Configuration Management (CM)
        if not project_data.get("version_control", False):
            violations.append({
                "area": "CM",
                "requirement": "Configuration Management",
                "message": "All artifacts must be under version control",
                "severity": "medium"
            })
            score -= 10
        
        # Process Area: Process and Product Quality Assurance (PPQA)
        if not project_data.get("quality_assurance", False):
            violations.append({
                "area": "PPQA",
                "requirement": "Quality Assurance",
                "message": "Quality assurance processes must be established",
                "severity": "medium"
            })
            score -= 10
        
        status = "compliant" if score >= 80 else "non_compliant"
        
        return {
            "framework": "CMMI",
            "level": self.level,
            "status": status,
            "score": max(0, score),
            "violations": violations,
            "validated_areas": [
                "Requirements Management",
                "Project Planning", 
                "Configuration Management",
                "Quality Assurance"
            ],
            "recommendations": self._generate_recommendations(violations)
        }
    
    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate recommendations based on violations"""
        recommendations = []
        
        for violation in violations:
            if violation["area"] == "REQM":
                recommendations.append("Implement requirements traceability matrix")
            elif violation["area"] == "PP":
                recommendations.append("Create comprehensive project planning documentation")
            elif violation["area"] == "CM":
                recommendations.append("Ensure all project artifacts are in version control")
            elif violation["area"] == "PPQA":
                recommendations.append("Establish quality assurance review processes")
        
        return recommendations


class SOXFramework(BaseComplianceFramework):
    """SOX compliance framework"""
    
    def __init__(self):
        super().__init__("SOX", "2002")
    
    async def validate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate SOX compliance"""
        
        violations = []
        score = 100
        
        # Section 302: Management Assessment
        if not project_data.get("management_certification", False):
            violations.append({
                "section": "302",
                "requirement": "Management Assessment",
                "message": "Management must certify financial reporting controls",
                "severity": "high"
            })
            score -= 25
        
        # Section 404: Internal Controls
        if not project_data.get("internal_controls", False):
            violations.append({
                "section": "404", 
                "requirement": "Internal Controls",
                "message": "Internal controls over financial reporting required",
                "severity": "high"
            })
            score -= 25
        
        # Audit Trail Requirements
        if not project_data.get("audit_trail", False):
            violations.append({
                "section": "General",
                "requirement": "Audit Trail",
                "message": "Complete audit trail of changes required",
                "severity": "medium"
            })
            score -= 15
        
        status = "compliant" if score >= 75 else "non_compliant"
        
        return {
            "framework": "SOX",
            "status": status,
            "score": max(0, score),
            "violations": violations,
            "validated_sections": ["302", "404", "General Controls"],
            "recommendations": ["Implement comprehensive audit logging", "Establish change control procedures"]
        }


class GDPRFramework(BaseComplianceFramework):
    """GDPR compliance framework"""
    
    def __init__(self):
        super().__init__("GDPR", "2018")
    
    async def validate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate GDPR compliance"""
        
        violations = []
        score = 100
        
        # Data Protection by Design
        if not project_data.get("privacy_by_design", False):
            violations.append({
                "article": "25",
                "requirement": "Data Protection by Design",
                "message": "Privacy by design principles must be implemented",
                "severity": "high"
            })
            score -= 20
        
        # Data Subject Rights
        if not project_data.get("data_subject_rights", False):
            violations.append({
                "article": "12-23",
                "requirement": "Data Subject Rights",
                "message": "Data subject rights mechanisms required",
                "severity": "high"
            })
            score -= 20
        
        # Data Breach Notification
        if not project_data.get("breach_notification", False):
            violations.append({
                "article": "33",
                "requirement": "Data Breach Notification",
                "message": "Data breach notification procedures required",
                "severity": "medium"
            })
            score -= 15
        
        status = "compliant" if score >= 80 else "non_compliant"
        
        return {
            "framework": "GDPR",
            "status": status,
            "score": max(0, score),
            "violations": violations,
            "validated_articles": ["25", "12-23", "33"],
            "recommendations": ["Implement privacy impact assessments", "Establish data subject request procedures"]
        }


class ISO27001Framework(BaseComplianceFramework):
    """ISO 27001 compliance framework"""
    
    def __init__(self):
        super().__init__("ISO 27001", "2013")
    
    async def validate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate ISO 27001 compliance"""
        
        violations = []
        score = 100
        
        # Information Security Policy
        if not project_data.get("security_policy", False):
            violations.append({
                "control": "A.5.1.1",
                "requirement": "Information Security Policy",
                "message": "Information security policy must be established",
                "severity": "high"
            })
            score -= 20
        
        # Access Control
        if not project_data.get("access_control", False):
            violations.append({
                "control": "A.9",
                "requirement": "Access Control",
                "message": "Access control measures must be implemented",
                "severity": "high"
            })
            score -= 20
        
        # Incident Management
        if not project_data.get("incident_management", False):
            violations.append({
                "control": "A.16",
                "requirement": "Incident Management",
                "message": "Security incident management procedures required",
                "severity": "medium"
            })
            score -= 15
        
        status = "compliant" if score >= 75 else "non_compliant"
        
        return {
            "framework": "ISO 27001",
            "status": status,
            "score": max(0, score),
            "violations": violations,
            "validated_controls": ["A.5.1.1", "A.9", "A.16"],
            "recommendations": ["Conduct security risk assessment", "Implement security awareness training"]
        }
