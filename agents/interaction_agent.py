"""
Interaction Agent
Handles user interaction and response formatting
"""

from typing import Dict, List
import textwrap


class InteractionAgent:
    """
    Agent that handles user interaction and response formatting.
    Converts technical information into clear, student-friendly responses.
    """
    
    def __init__(self):
        """Initialize the interaction agent."""
        self.agent_name = "User Interaction Agent"
        self.response_templates = {
            "admission": "To apply for {program}, you need to meet these requirements:\n{requirements}\nApplication Deadline: {deadline}",
            "exam": "Exam Information:\n{details}",
            "scholarship": "Scholarship Eligibility:\n{requirements}\n{amount_info}",
            "academic_policy": "Academic Policy Information:\n{requirements}"
        }
    
    def process(self, policy_data: Dict, intent: str = None) -> Dict:
        """
        Process and format information for student presentation.
        
        Args:
            policy_data (Dict): Data from policy agent
            intent (str): Query intent
            
        Returns:
            Dict: Formatted response ready for display
        """
        try:
            formatted_response = self._format_response(policy_data, intent)
            
            result = {
                "agent": self.agent_name,
                "formatted_response": formatted_response,
                "intent": intent,
                "status": "success"
            }
            
            return result
        
        except Exception as e:
            result = {
                "agent": self.agent_name,
                "formatted_response": "Unable to process your query at this time.",
                "intent": intent,
                "status": "failed",
                "error": str(e)
            }
            
            return result
    
    def _format_response(self, data: Dict, intent: str) -> str:
        """
        Format the response based on intent and data.
        
        Args:
            data (Dict): Policy data
            intent (str): Query intent
            
        Returns:
            str: Formatted response
        """
        if not data:
            return "No information available for your query."
        
        # Convert dict to string for processing
        data_str = str(data)
        
        # Format based on intent
        if intent == "admission":
            return self._format_admission_response(data)
        elif intent == "exam":
            return self._format_exam_response(data)
        elif intent == "scholarship":
            return self._format_scholarship_response(data)
        elif intent == "academic_policy":
            return self._format_policy_response(data)
        else:
            return self._format_generic_response(data)
    
    def _format_admission_response(self, data: Dict) -> str:
        """Format admission-related response."""
        response = "📋 ADMISSION REQUIREMENTS\n"
        response += "-" * 40 + "\n"
        
        requirements = []
        
        # Extract requirements from data
        if "requirements" in str(data):
            requirements.append("• Meet the eligibility criteria for your desired program")
        
        # Add extracted information
        for policy in data.get("policies", []):
            info = policy.get("extracted_info", {})
            
            if "gpa_requirement" in info:
                requirements.append(f"• Minimum GPA: {info['gpa_requirement']}")
            
            if "sat_score" in info:
                requirements.append(f"• SAT Score: {info['sat_score']} or higher")
            
            if "act_score" in info:
                requirements.append(f"• ACT Score: {info['act_score']} or higher")
            
            if "deadline" in info:
                requirements.append(f"• Application Deadline: {info['deadline']}")
        
        if not requirements:
            requirements.append("• Submit your application and supporting documents")
        
        for req in requirements:
            response += f"{req}\n"
        
        response += "\n✅ Next Steps:\n"
        response += "1. Verify your eligibility\n"
        response += "2. Prepare your documents\n"
        response += "3. Submit your application before the deadline\n"
        response += "4. Monitor application status\n"
        
        return response
    
    def _format_exam_response(self, data: Dict) -> str:
        """Format exam-related response."""
        response = "📝 EXAM INFORMATION\n"
        response += "-" * 40 + "\n"
        
        # Extract exam details from data
        if "schedule" in str(data).lower():
            response += "• Check the academic calendar for exam dates\n"
        
        if "grading" in str(data).lower():
            response += "• Final grades are calculated based on course policies\n"
        
        if "retake" in str(data).lower():
            response += "• You may retake courses for grade improvement\n"
        
        response += "\n📌 Important:\n"
        response += "• Visit your course page for specific exam times\n"
        response += "• Contact your instructor for exam details\n"
        response += "• Review exam policies on the registrar website\n"
        
        return response
    
    def _format_scholarship_response(self, data: Dict) -> str:
        """Format scholarship-related response."""
        response = "💰 SCHOLARSHIP INFORMATION\n"
        response += "-" * 40 + "\n"
        
        response += "Eligibility:\n"
        
        for policy in data.get("policies", []):
            info = policy.get("extracted_info", {})
            
            if "gpa_requirement" in info:
                response += f"• Minimum GPA: {info['gpa_requirement']}\n"
        
        response += "• U.S. Citizenship or permanent residency\n"
        response += "• Full-time enrollment status\n"
        response += "• Good academic standing\n"
        
        response += "\n💡 Available Scholarships:\n"
        response += "• Merit-based scholarships\n"
        response += "• Need-based financial aid\n"
        response += "• Department-specific scholarships\n"
        response += "• Student worker positions\n"
        
        response += "\n📝 Application Process:\n"
        response += "1. Complete FAFSA form\n"
        response += "2. Explore available scholarships\n"
        response += "3. Submit scholarship applications\n"
        response += "4. Await award notification\n"
        
        return response
    
    def _format_policy_response(self, data: Dict) -> str:
        """Format academic policy response."""
        response = "📚 ACADEMIC POLICY INFORMATION\n"
        response += "-" * 40 + "\n"
        
        response += "Key Requirements:\n"
        
        for policy in data.get("policies", []):
            info = policy.get("extracted_info", {})
            
            if "gpa_requirement" in info:
                response += f"• Minimum GPA to maintain good standing: {info['gpa_requirement']}\n"
            
            if "credit_hours" in info:
                response += f"• Total credit hours required: {info['credit_hours']}\n"
        
        response += "• Maximum 18 credit hours per semester\n"
        response += "• Minimum 2.0 GPA requirement\n"
        response += "• Prerequisites must be completed before course enrollment\n"
        
        response += "\n⚠️ Academic Standing:\n"
        response += "• Probation: Below 2.0 GPA\n"
        response += "• Dismissal: 2 consecutive semesters on probation\n"
        
        response += "\n📞 Contact:\n"
        response += "• Registrar Office for policy details\n"
        response += "• Academic Advisor for course planning\n"
        response += "• Dean of Students for appeals\n"
        
        return response
    
    def _format_generic_response(self, data: Dict) -> str:
        """Format generic response."""
        response = "ℹ️ INFORMATION\n"
        response += "-" * 40 + "\n"
        
        response += "Based on your query, here's what we found:\n\n"
        
        for policy in data.get("policies", []):
            response += f"Category: {policy.get('category', 'General')}\n"
            info = policy.get("extracted_info", {})
            
            for key, value in info.items():
                response += f"• {key.replace('_', ' ').title()}: {value}\n"
            
            response += "\n"
        
        response += "For more information, please contact the appropriate office.\n"
        
        return response
    
    def format_conversation_turn(self, query: str, response: str, agent_info: str = None) -> str:
        """
        Format a conversation turn with query and response.
        
        Args:
            query (str): User query
            response (str): Formatted response
            agent_info (str): Information about which agents processed
            
        Returns:
            str: Formatted conversation turn
        """
        output = f"\nYour Question:\n{query}\n\n"
        
        if agent_info:
            output += f"Processing: {agent_info}\n\n"
        
        output += f"Response:\n{response}\n"
        
        return output
    
    def get_followup_suggestions(self, intent: str) -> List[str]:
        """
        Get suggested follow-up questions based on intent.
        
        Args:
            intent (str): Query intent
            
        Returns:
            List[str]: Suggested follow-up questions
        """
        suggestions = {
            "admission": [
                "What documents do I need to submit?",
                "When should I take the entrance exam?",
                "What is the application fee?"
            ],
            "exam": [
                "How is my final grade calculated?",
                "Can I retake the exam?",
                "When will results be posted?"
            ],
            "scholarship": [
                "How much funding can I receive?",
                "When is the scholarship application deadline?",
                "What is the renewal criteria?"
            ],
            "academic_policy": [
                "What happens if my GPA drops?",
                "How many credits can I take?",
                "What is the withdrawal deadline?"
            ]
        }
        
        return suggestions.get(intent, ["Is there anything else I can help with?"])
    
    def add_styling(self, text: str, style: str = "basic") -> str:
        """
        Add styling to formatted text.
        
        Args:
            text (str): Text to style
            style (str): Style type (basic, detailed, simple)
            
        Returns:
            str: Styled text
        """
        if style == "detailed":
            return f"\n{'='*50}\n{text}\n{'='*50}\n"
        elif style == "simple":
            return f"\n{text}\n"
        else:
            return text


if __name__ == "__main__":
    # Test interaction agent
    print("Initializing Interaction Agent...")
    agent = InteractionAgent()
    
    # Test data
    test_policy_data = {
        "policies": [
            {
                "category": "admission",
                "extracted_info": {
                    "gpa_requirement": 3.2,
                    "sat_score": 1400,
                    "deadline": "March 31"
                }
            }
        ]
    }
    
    print("="*70)
    print("INTERACTION AGENT TEST RESULTS")
    print("="*70)
    
    result = agent.process(test_policy_data, intent="admission")
    
    print("\nFormatted Response:")
    print(result["formatted_response"])
    
    print("\nFollow-up Suggestions:")
    suggestions = agent.get_followup_suggestions("admission")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n" + "="*70)
