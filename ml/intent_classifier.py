"""
Intent Classification Module
Uses keyword-based classification for student queries into categories:
- admission
- exam
- scholarship
- academic_policy
"""

import numpy as np
from typing import Tuple, List, Dict

class IntentClassifier:
    """
    Classifies student queries into intent categories using keyword matching.
    Categories: admission, exam, scholarship, academic_policy
    Works offline without downloading large models.
    """
    
    def __init__(self):
        """Initialize the intent classifier with keyword-based approach."""
        # Intent categories
        self.intent_labels = ["admission", "exam", "scholarship", "academic_policy"]
        self.intent_to_id = {label: idx for idx, label in enumerate(self.intent_labels)}
        self.id_to_intent = {idx: label for label, idx in self.intent_to_id.items()}
        
        # Training keywords for each category
        self.intent_keywords = {
            "admission": [
                "admission", "eligible", "eligibility", "application", "requirements",
                "enroll", "enrollment", "accepted", "acceptance", "degree program",
                "apply", "entrance exam", "gpa requirement", "sat", "act", "apply for",
                "program", "bs ", "ba ", "major", "undergraduate", "graduate"
            ],
            "exam": [
                "exam", "test", "quiz", "assessment", "midterm", "final", "grade",
                "score", "result", "schedule", "retake", "exam policy", "grading",
                "when is", "exam date", "test score", "marks", "gpa calculation"
            ],
            "scholarship": [
                "scholarship", "financial aid", "grant", "funding", "tuition waiver",
                "financial assistance", "sponsor", "sponsorship", "award",
                "merit scholarship", "need-based", "stipend", "loan", "fafsa",
                "eligible for", "qualify", "financial"
            ],
            "academic_policy": [
                "policy", "academic policy", "requirement", "gpa", "standing",
                "regulation", "rule", "course registration", "credit hour",
                "academic standing", "probation", "dismissal", "prerequisite",
                "minimum gpa", "maintain", "register", "credit", "hours", "policy"
            ]
        }
    
    def predict(self, query: str) -> Tuple[str, float]:
        """
        Predict the intent of a query using keyword matching.
        
        Args:
            query (str): The input query from student
            
        Returns:
            Tuple[str, float]: (predicted_intent, confidence_score)
        """
        return self.predict_with_keywords(query)
    
    def predict_with_keywords(self, query: str) -> Tuple[str, float]:
        """
        Fallback method using keyword matching to classify intent.
        
        Args:
            query (str): The input query from student
            
        Returns:
            Tuple[str, float]: (predicted_intent, confidence_score)
        """
        query_lower = query.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            intent_scores[intent] = score
        
        if max(intent_scores.values()) == 0:
            # Default to most general category
            return "academic_policy", 0.5
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent] / (len(query_lower.split()) / 2)
        confidence = min(confidence, 1.0)
        
        return best_intent, confidence
    
    def predict_batch(self, queries: List[str]) -> List[Tuple[str, float]]:
        """
        Predict intents for multiple queries.
        
        Args:
            queries (List[str]): List of queries
            
        Returns:
            List[Tuple[str, float]]: List of (intent, confidence) tuples
        """
        results = []
        for query in queries:
            intent, confidence = self.predict(query)
            results.append((intent, confidence))
        return results
    
    def get_intent_description(self, intent: str) -> str:
        """
        Get a description of the intent category.
        
        Args:
            intent (str): The intent category
            
        Returns:
            str: Description of the intent
        """
        descriptions = {
            "admission": "Questions about university admission eligibility and requirements",
            "exam": "Questions about exams, grades, and assessment-related topics",
            "scholarship": "Questions about scholarships and financial aid",
            "academic_policy": "Questions about academic policies, regulations, and requirements"
        }
        return descriptions.get(intent, "Unknown intent")


# Example usage and training simulation
def create_training_data():
    """Create synthetic training data for demonstration."""
    training_data = {
        "admission": [
            "What is the eligibility for BS Computer Science?",
            "What are the requirements to apply?",
            "When is the application deadline?",
            "What is the minimum GPA needed for admission?",
            "How do I enroll in the engineering program?"
        ],
        "exam": [
            "When is the next exam?",
            "What is my final grade?",
            "Can I retake the midterm?",
            "What is the grading policy?",
            "When are exam results released?"
        ],
        "scholarship": [
            "Am I eligible for scholarships?",
            "What financial aid options are available?",
            "How do I apply for grants?",
            "What is the scholarship amount?",
            "Is there merit-based funding?"
        ],
        "academic_policy": [
            "What is the minimum GPA requirement?",
            "What are the academic standing rules?",
            "Can I register late?",
            "What is the maximum course load?",
            "What are the prerequisites for this course?"
        ]
    }
    return training_data


if __name__ == "__main__":
    # Initialize classifier
    print("Initializing Intent Classifier...")
    classifier = IntentClassifier()
    
    # Test queries
    test_queries = [
        "What is the eligibility for BS Electrical Engineering?",
        "When is the final exam scheduled?",
        "Am I eligible for scholarships?",
        "What is the minimum GPA to maintain good academic standing?"
    ]
    
    print("\n" + "="*60)
    print("INTENT CLASSIFICATION RESULTS")
    print("="*60)
    
    for query in test_queries:
        intent, confidence = classifier.predict(query)
        description = classifier.get_intent_description(intent)
        print(f"\nQuery: {query}")
        print(f"Intent: {intent} (Confidence: {confidence:.2%})")
        print(f"Description: {description}")
    
    print("\n" + "="*60)
