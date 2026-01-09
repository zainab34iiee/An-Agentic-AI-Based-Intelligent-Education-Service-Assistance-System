"""
Intent Agent
Detects and classifies the intent of student queries
"""

from typing import Tuple, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.intent_classifier import IntentClassifier


class IntentAgent:
    """
    Agent that uses intent_classifier to detect student query intent.
    Classifies queries into: admission, exam, scholarship, academic_policy
    """
    
    def __init__(self):
        """Initialize the intent agent with intent classifier."""
        self.classifier = IntentClassifier()
        self.agent_name = "Intent Detection Agent"
    
    def process(self, query: str) -> Dict:
        """
        Process a query and detect its intent.
        
        Args:
            query (str): The student query
            
        Returns:
            Dict: Intent detection result with intent, confidence, and description
        """
        try:
            intent, confidence = self.classifier.predict(query)
            description = self.classifier.get_intent_description(intent)
            
            result = {
                "agent": self.agent_name,
                "query": query,
                "intent": intent,
                "confidence": confidence,
                "description": description,
                "status": "success"
            }
            
            return result
        
        except Exception as e:
            # Fallback to keyword-based classification on error
            intent, confidence = self.classifier.predict_with_keywords(query)
            description = self.classifier.get_intent_description(intent)
            
            result = {
                "agent": self.agent_name,
                "query": query,
                "intent": intent,
                "confidence": confidence,
                "description": description,
                "status": "success_fallback",
                "error": str(e)
            }
            
            return result
    
    def validate_intent(self, intent: str) -> bool:
        """
        Validate if an intent is recognized.
        
        Args:
            intent (str): The intent to validate
            
        Returns:
            bool: Whether the intent is valid
        """
        return intent in self.classifier.intent_labels
    
    def get_supported_intents(self) -> list:
        """
        Get list of supported intent categories.
        
        Returns:
            list: List of supported intents
        """
        return self.classifier.intent_labels
    
    def batch_process(self, queries: list) -> list:
        """
        Process multiple queries.
        
        Args:
            queries (list): List of queries
            
        Returns:
            list: List of intent detection results
        """
        results = []
        for query in queries:
            result = self.process(query)
            results.append(result)
        
        return results


if __name__ == "__main__":
    # Test intent agent
    print("Initializing Intent Agent...")
    agent = IntentAgent()
    
    print(f"Supported intents: {agent.get_supported_intents()}\n")
    
    # Test queries
    test_queries = [
        "What is the eligibility for BS Electrical Engineering?",
        "When is the next exam scheduled?",
        "Am I eligible for scholarships?",
        "What is the minimum GPA requirement?"
    ]
    
    print("="*70)
    print("INTENT AGENT TEST RESULTS")
    print("="*70)
    
    for query in test_queries:
        result = agent.process(query)
        print(f"\nQuery: {query}")
        print(f"Intent: {result['intent']} (Confidence: {result['confidence']:.2%})")
        print(f"Status: {result['status']}")
    
    print("\n" + "="*70)
