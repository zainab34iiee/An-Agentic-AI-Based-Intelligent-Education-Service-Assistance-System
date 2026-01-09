"""
Policy Agent
Interprets academic policies from retrieved documents
"""

from typing import List, Dict
import re


class PolicyAgent:
    """
    Agent that interprets academic policies from retrieved documents.
    Extracts and structures policy information for clear presentation.
    """
    
    def __init__(self):
        """Initialize the policy agent."""
        self.agent_name = "Policy Interpretation Agent"
        
        # Policy extraction patterns
        self.policy_patterns = {
            "gpa": r"(?:minimum|min|GPA|gpa).*?(\d+\.\d+)",
            "score": r"(?:SAT|ACT|score|Score).*?(\d+)",
            "deadline": r"(?:deadline|due|by|before).*?([A-Za-z]+\s+\d+)",
            "requirement": r"(?:require|must|need|completion).*?([^,\.]+)",
            "grade": r"(?:grade|Grade).*?([A-F])",
            "credit": r"(?:credit|hours?).*?(\d+)"
        }
    
    def process(self, documents: List[Dict]) -> Dict:
        """
        Interpret policies from a list of retrieved documents.
        
        Args:
            documents (List[Dict]): Retrieved documents
            
        Returns:
            Dict: Extracted and interpreted policy information
        """
        if not documents:
            return {
                "agent": self.agent_name,
                "policies": [],
                "requirements": [],
                "status": "no_documents"
            }
        
        # Extract policy information
        policies = []
        requirements = []
        
        for doc in documents:
            text = doc.get("text", "")
            category = doc.get("category", "")
            
            # Extract structured information
            extracted = self._extract_policies(text)
            
            if extracted:
                policies.append({
                    "category": category,
                    "source": text[:80] + "...",
                    "extracted_info": extracted
                })
            
            # Extract requirements
            reqs = self._extract_requirements(text)
            if reqs:
                requirements.extend(reqs)
        
        result = {
            "agent": self.agent_name,
            "policies": policies,
            "requirements": requirements,
            "num_policies": len(policies),
            "status": "success"
        }
        
        return result
    
    def _extract_policies(self, text: str) -> Dict:
        """
        Extract policy information from document text.
        
        Args:
            text (str): Document text
            
        Returns:
            Dict: Extracted policy data
        """
        extracted = {}
        
        # Extract GPA requirements
        gpa_match = re.search(r"(?:minimum|min|GPA|gpa).*?(\d+\.\d+)", text, re.IGNORECASE)
        if gpa_match:
            extracted["gpa_requirement"] = float(gpa_match.group(1))
        
        # Extract test scores
        sat_match = re.search(r"SAT\s+(?:score)?.*?(\d{3,4})", text, re.IGNORECASE)
        if sat_match:
            extracted["sat_score"] = int(sat_match.group(1))
        
        act_match = re.search(r"ACT\s+(?:score)?.*?(\d{2,3})", text, re.IGNORECASE)
        if act_match:
            extracted["act_score"] = int(act_match.group(1))
        
        # Extract deadlines
        deadline_match = re.search(r"(?:deadline|due|by|before).*?([A-Za-z]+\s+\d+)", text)
        if deadline_match:
            extracted["deadline"] = deadline_match.group(1)
        
        # Extract credit hour requirements
        credit_match = re.search(r"(\d+)\s+(?:credit|hour)", text, re.IGNORECASE)
        if credit_match:
            extracted["credit_hours"] = int(credit_match.group(1))
        
        # Extract grade requirements
        grade_match = re.search(r"(?:grade|Grade)\s+([A-F])", text)
        if grade_match:
            extracted["minimum_grade"] = grade_match.group(1)
        
        return extracted
    
    def _extract_requirements(self, text: str) -> List[str]:
        """
        Extract specific requirements from text.
        
        Args:
            text (str): Document text
            
        Returns:
            List[str]: Extracted requirements
        """
        requirements = []
        
        # Extract requirements using keywords
        if "require" in text.lower() or "must" in text.lower():
            # Split by common delimiters and extract requirements
            sentences = text.split(",")
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in ["require", "must", "need"]):
                    req = sentence.strip()
                    if len(req) > 10:  # Filter out too short strings
                        requirements.append(req)
        
        return requirements
    
    def interpret_admission_policy(self, policies: Dict) -> List[str]:
        """
        Generate human-readable admission requirements from extracted policies.
        
        Args:
            policies (Dict): Extracted policy information
            
        Returns:
            List[str]: Readable requirements
        """
        interpretation = []
        
        for policy in policies.get("policies", []):
            info = policy.get("extracted_info", {})
            
            if info:
                if "gpa_requirement" in info:
                    interpretation.append(f"Minimum GPA: {info['gpa_requirement']}")
                
                if "sat_score" in info:
                    interpretation.append(f"SAT Score: {info['sat_score']}+")
                
                if "act_score" in info:
                    interpretation.append(f"ACT Score: {info['act_score']}+")
                
                if "deadline" in info:
                    interpretation.append(f"Application Deadline: {info['deadline']}")
                
                if "credit_hours" in info:
                    interpretation.append(f"Required Credit Hours: {info['credit_hours']}")
        
        return interpretation
    
    def compare_policies(self, policy1: Dict, policy2: Dict) -> Dict:
        """
        Compare two policies and identify differences.
        
        Args:
            policy1 (Dict): First policy
            policy2 (Dict): Second policy
            
        Returns:
            Dict: Comparison results
        """
        differences = {
            "policy1_unique": [],
            "policy2_unique": [],
            "common": []
        }
        
        keys1 = set(policy1.get("extracted_info", {}).keys())
        keys2 = set(policy2.get("extracted_info", {}).keys())
        
        differences["policy1_unique"] = list(keys1 - keys2)
        differences["policy2_unique"] = list(keys2 - keys1)
        differences["common"] = list(keys1 & keys2)
        
        return differences


if __name__ == "__main__":
    # Test policy agent
    print("Initializing Policy Agent...")
    agent = PolicyAgent()
    
    # Test documents (simulating retrieval results)
    test_documents = [
        {
            "text": "BS Electrical Engineering admission: Minimum GPA 3.2, SAT 1400+, ACT 32+, deadline March 31",
            "category": "admission"
        },
        {
            "text": "Grading policy: A (90-100), B (80-89), minimum grade C required, credits needed 120",
            "category": "academic_policy"
        }
    ]
    
    print("="*70)
    print("POLICY AGENT TEST RESULTS")
    print("="*70)
    
    result = agent.process(test_documents)
    
    print(f"\nPolicies Found: {result['num_policies']}")
    print("\nExtracted Information:")
    
    for i, policy in enumerate(result["policies"], 1):
        print(f"\n[Policy {i}] Category: {policy['category']}")
        print(f"Information: {policy['extracted_info']}")
    
    print("\nRequirements:")
    for req in result["requirements"]:
        print(f"  - {req}")
    
    print("\nReadable Interpretation:")
    interpretation = agent.interpret_admission_policy(result)
    for item in interpretation:
        print(f"  - {item}")
    
    print("\n" + "="*70)
