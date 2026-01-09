"""
Verification Agent
Verifies factual correctness and policy compliance
"""

from typing import Dict, List
import re


class VerificationAgent:
    """
    Agent that verifies factual correctness and policy compliance.
    Validates information consistency and accuracy.
    """
    
    def __init__(self):
        """Initialize the verification agent."""
        self.agent_name = "Verification Agent"
        
        # Known valid ranges and constraints
        self.valid_ranges = {
            "gpa": (0.0, 4.0),
            "credit_hours": (1, 200),
            "sat_score": (400, 1600),
            "act_score": (1, 36),
            "percentage": (0, 100)
        }
        
        # Known valid entities
        self.valid_categories = ["admission", "exam", "scholarship", "academic_policy"]
        self.valid_intents = ["admission", "exam", "scholarship", "academic_policy"]
    
    def process(self, information: Dict) -> Dict:
        """
        Verify the correctness of extracted information.
        
        Args:
            information (Dict): Information to verify (from policy agent)
            
        Returns:
            Dict: Verification results with confidence scores
        """
        verification_results = {
            "agent": self.agent_name,
            "verified": True,
            "issues": [],
            "warnings": [],
            "data_quality_score": 1.0
        }
        
        # Verify various aspects
        self._verify_numeric_values(information, verification_results)
        self._verify_consistency(information, verification_results)
        self._verify_completeness(information, verification_results)
        
        # Calculate overall quality score
        issues_count = len(verification_results["issues"])
        warnings_count = len(verification_results["warnings"])
        quality_deduction = (issues_count * 0.1) + (warnings_count * 0.05)
        verification_results["data_quality_score"] = max(0, 1.0 - quality_deduction)
        
        verification_results["status"] = "success"
        return verification_results
    
    def _verify_numeric_values(self, information: Dict, results: Dict):
        """
        Verify that numeric values are within valid ranges.
        
        Args:
            information (Dict): Information to verify
            results (Dict): Results dictionary to update
        """
        # Check GPA
        if "gpa" in str(information):
            gpa_values = re.findall(r"(\d+\.\d+)", str(information))
            for gpa_val in gpa_values:
                gpa_float = float(gpa_val)
                if not (self.valid_ranges["gpa"][0] <= gpa_float <= self.valid_ranges["gpa"][1]):
                    results["issues"].append(f"Invalid GPA value: {gpa_float}")
                    results["verified"] = False
        
        # Check SAT scores
        if "SAT" in str(information):
            sat_values = re.findall(r"SAT.*?(\d{3,4})", str(information))
            for sat_val in sat_values:
                sat_int = int(sat_val)
                if not (self.valid_ranges["sat_score"][0] <= sat_int <= self.valid_ranges["sat_score"][1]):
                    results["warnings"].append(f"SAT score {sat_int} is unusual")
        
        # Check ACT scores
        if "ACT" in str(information):
            act_values = re.findall(r"ACT.*?(\d{1,2})", str(information))
            for act_val in act_values:
                act_int = int(act_val)
                if not (self.valid_ranges["act_score"][0] <= act_int <= self.valid_ranges["act_score"][1]):
                    results["warnings"].append(f"ACT score {act_int} is unusual")
    
    def _verify_consistency(self, information: Dict, results: Dict):
        """
        Verify consistency in the information.
        
        Args:
            information (Dict): Information to verify
            results (Dict): Results dictionary to update
        """
        info_str = str(information).lower()
        
        # Check for contradictory statements
        if "must" in info_str and "no" in info_str:
            results["warnings"].append("Potential contradictory statements detected")
        
        # Check category validity
        for category in self.valid_categories:
            if f'"{category}"' in str(information):
                # Category found and is valid
                pass
    
    def _verify_completeness(self, information: Dict, results: Dict):
        """
        Verify completeness of information.
        
        Args:
            information (Dict): Information to verify
            results (Dict): Results dictionary to update
        """
        info_str = str(information)
        
        # Check if minimum required information is present
        if len(info_str) < 50:
            results["warnings"].append("Information seems incomplete or too brief")
        
        # Check for common required fields in different categories
        if "admission" in info_str.lower():
            required_fields = ["gpa", "test", "deadline"]
            found_fields = sum(1 for field in required_fields if field.lower() in info_str.lower())
            
            if found_fields < 2:
                results["warnings"].append("Admission information may be missing key details")
    
    def verify_documents(self, documents: List[Dict]) -> Dict:
        """
        Verify a list of documents.
        
        Args:
            documents (List[Dict]): Documents to verify
            
        Returns:
            Dict: Verification results for all documents
        """
        results = {
            "agent": self.agent_name,
            "total_documents": len(documents),
            "verified_documents": 0,
            "document_results": [],
            "overall_score": 0.0
        }
        
        scores = []
        
        for doc in documents:
            doc_result = self.process(doc)
            results["document_results"].append(doc_result)
            scores.append(doc_result["data_quality_score"])
            
            if doc_result["verified"]:
                results["verified_documents"] += 1
        
        # Calculate overall quality score
        results["overall_score"] = sum(scores) / len(scores) if scores else 0.0
        results["status"] = "success"
        
        return results
    
    def get_verification_report(self, verification_result: Dict) -> str:
        """
        Generate a human-readable verification report.
        
        Args:
            verification_result (Dict): Verification results
            
        Returns:
            str: Formatted report
        """
        report = f"\n[VERIFICATION REPORT]\n"
        report += f"Status: {'✓ Verified' if verification_result['verified'] else '✗ Issues Found'}\n"
        report += f"Data Quality Score: {verification_result['data_quality_score']:.1%}\n"
        
        if verification_result["issues"]:
            report += "\nIssues:\n"
            for issue in verification_result["issues"]:
                report += f"  ✗ {issue}\n"
        
        if verification_result["warnings"]:
            report += "\nWarnings:\n"
            for warning in verification_result["warnings"]:
                report += f"  ⚠ {warning}\n"
        
        if not verification_result["issues"] and not verification_result["warnings"]:
            report += "No issues detected. All information verified.\n"
        
        return report
    
    def check_factual_accuracy(self, statement: str, reference_data: Dict) -> Dict:
        """
        Check if a statement is factually accurate against reference data.
        
        Args:
            statement (str): Statement to check
            reference_data (Dict): Reference data to check against
            
        Returns:
            Dict: Accuracy check results
        """
        result = {
            "statement": statement,
            "accuracy": "unknown",
            "confidence": 0.5,
            "matches_reference": False
        }
        
        # Simple string matching for basic verification
        reference_str = str(reference_data).lower()
        statement_lower = statement.lower()
        
        # Check for key phrase matches
        key_phrases = re.findall(r'\b\w+\s+\w+\b', statement_lower)
        matches = sum(1 for phrase in key_phrases if phrase in reference_str)
        
        if matches > 0:
            result["matches_reference"] = True
            result["accuracy"] = "likely_accurate"
            result["confidence"] = min(matches / len(key_phrases), 1.0) if key_phrases else 0.5
        else:
            result["accuracy"] = "unverifiable"
            result["confidence"] = 0.3
        
        return result


if __name__ == "__main__":
    # Test verification agent
    print("Initializing Verification Agent...")
    agent = VerificationAgent()
    
    # Test data
    test_data = {
        "gpa_requirement": 3.2,
        "sat_score": 1400,
        "act_score": 32,
        "deadline": "March 31",
        "category": "admission"
    }
    
    print("="*70)
    print("VERIFICATION AGENT TEST RESULTS")
    print("="*70)
    
    result = agent.process(test_data)
    
    print(agent.get_verification_report(result))
    
    # Test invalid data
    print("\n\nTesting Invalid Data:")
    print("-"*70)
    
    invalid_data = {
        "gpa_requirement": 5.0,  # Invalid: GPA > 4.0
        "sat_score": 2000,  # Invalid: SAT > 1600
        "category": "admission"
    }
    
    result_invalid = agent.process(invalid_data)
    print(agent.get_verification_report(result_invalid))
    
    print("\n" + "="*70)
