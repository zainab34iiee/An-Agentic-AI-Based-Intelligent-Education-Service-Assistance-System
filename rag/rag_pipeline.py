"""
Retrieval-Augmented Generation (RAG) Pipeline
Implements document retrieval using simple similarity matching
Works offline without external model downloads
"""

import numpy as np
from typing import List, Tuple, Dict
import re


class RAGPipeline:
    """
    Simplified Retrieval-Augmented Generation Pipeline.
    Retrieves relevant academic documents for a given query using keyword matching.
    """
    
    def __init__(self, embedding_model: str = None):
        """
        Initialize the RAG pipeline.
        
        Args:
            embedding_model (str): Ignored for offline mode
        """
        self.documents = []
        self.metadata = []
        
        # Load sample education documents
        self._load_sample_documents()
    
    def _load_sample_documents(self):
        """Load sample education documents for retrieval."""
        sample_documents = [
            # Admission documents
            {
                "text": "BS Electrical Engineering admission requirements: Minimum GPA 3.2, SAT score 1400+, ACT score 32+, completion of physics and chemistry courses, application deadline March 31",
                "category": "admission",
                "program": "BS Electrical Engineering"
            },
            {
                "text": "BS Computer Science eligibility criteria: Minimum GPA 3.0, strong mathematical foundation, SAT 1350+, ACT 31+, admission test required, rolling admission until seats fill",
                "category": "admission",
                "program": "BS Computer Science"
            },
            {
                "text": "General admission process: Online application, transcripts, test scores, essay, 2 recommendation letters, application fee $50, decision within 6 weeks",
                "category": "admission",
                "program": "General"
            },
            
            # Exam documents
            {
                "text": "Final exam schedule: Fall semester finals held December 10-20, Spring semester finals held May 5-15, summer exams June 20-July 5, exam schedule posted 2 weeks before",
                "category": "exam",
                "topic": "Exam Schedule"
            },
            {
                "text": "Grading policy: A (90-100), B (80-89), C (70-79), D (60-69), F (below 60), GPA calculation uses 4.0 scale, plus/minus grading for A/B/C grades, grade appeals within 30 days",
                "category": "exam",
                "topic": "Grading Policy"
            },
            {
                "text": "Exam retake policy: Students can retake courses for grade improvement, only latest grade counts toward GPA, 2 retakes per course maximum, must wait 1 semester between retakes",
                "category": "exam",
                "topic": "Retake Policy"
            },
            
            # Scholarship documents
            {
                "text": "Merit scholarships: Full tuition coverage for students with 3.8+ GPA and 1500+ SAT score, half tuition for 3.5+ GPA and 1400+ SAT, automatically awarded to eligible applicants",
                "category": "scholarship",
                "scholarship_type": "Merit-Based"
            },
            {
                "text": "Need-based financial aid: Available for students with FAFSA EFC below 50000, grants up to $10000/year, low-interest loans 3.5% APR, work-study jobs $15/hour",
                "category": "scholarship",
                "scholarship_type": "Need-Based"
            },
            {
                "text": "Department scholarships: Engineering scholarship $5000/year for top students, business school scholarship $7500/year, science scholarship $6000/year, separate application required",
                "category": "scholarship",
                "scholarship_type": "Department-Specific"
            },
            
            # Academic policy documents
            {
                "text": "Academic standing: Maintain minimum 2.0 GPA to remain in good standing, below 2.0 GPA results in academic probation, dismissal after 2 consecutive semesters on probation",
                "category": "academic_policy",
                "policy": "Academic Standing"
            },
            {
                "text": "Course registration: Priority registration for seniors, then juniors, sophomores, freshmen. Registration opens 2 weeks before semester. Maximum 18 credit hours per semester.",
                "category": "academic_policy",
                "policy": "Registration"
            },
            {
                "text": "Prerequisite policy: Students must complete prerequisite courses with C grade or higher, prerequisite waivers available with department chair approval, verified through course history system",
                "category": "academic_policy",
                "policy": "Prerequisites"
            },
            {
                "text": "General education requirements: All students must complete 30 credit hours in general education including English, Mathematics, Science, Social Studies, Humanities. Specific courses listed in catalog.",
                "category": "academic_policy",
                "policy": "Gen Ed Requirements"
            },
            {
                "text": "Degree completion: Bachelor's degree requires 120 credit hours minimum, GPA 2.0 or above, completion of all program and general education requirements, maximum 7 years to complete",
                "category": "academic_policy",
                "policy": "Degree Requirements"
            }
        ]
        
        # Store documents and metadata
        self.documents = [doc["text"] for doc in sample_documents]
        self.metadata = sample_documents
        
        print(f"Loaded {len(self.documents)} documents into RAG pipeline")
    
    def _calculate_similarity(self, query: str, document: str) -> float:
        """
        Calculate similarity between query and document using keyword matching.
        
        Args:
            query (str): The search query
            document (str): The document text
            
        Returns:
            float: Similarity score (0-1)
        """
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())
        
        # Remove common words
        common_words = {"a", "an", "the", "and", "or", "is", "are", "for", "of", "to", "in"}
        query_words -= common_words
        doc_words -= common_words
        
        # Calculate Jaccard similarity
        if len(query_words | doc_words) == 0:
            return 0.0
        
        intersection = len(query_words & doc_words)
        union = len(query_words | doc_words)
        
        return intersection / union
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k relevant documents for a query.
        
        Args:
            query (str): The search query
            top_k (int): Number of top results to return
            
        Returns:
            List[Dict]: List of relevant documents with scores
        """
        # Calculate similarity for all documents
        scores = []
        for i, doc in enumerate(self.documents):
            score = self._calculate_similarity(query, doc)
            scores.append((i, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for rank, (idx, score) in enumerate(scores[:top_k], 1):
            result = {
                "rank": rank,
                "text": self.documents[idx],
                "metadata": self.metadata[idx],
                "similarity_score": score,
                "distance": 1 - score
            }
            results.append(result)
        
        return results
    
    def retrieve_by_category(self, query: str, category: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve documents filtered by category.
        
        Args:
            query (str): The search query
            category (str): Category to filter by
            top_k (int): Number of results to return
            
        Returns:
            List[Dict]: Filtered relevant documents
        """
        # Get all results
        all_results = self.retrieve(query, top_k * 3)
        
        # Filter by category
        filtered_results = [
            r for r in all_results 
            if r["metadata"].get("category") == category
        ]
        
        # Return top_k after filtering
        return filtered_results[:top_k]
    
    def get_document_summary(self, doc: Dict) -> str:
        """
        Get a summary of a document's key information.
        
        Args:
            doc (Dict): Document from retrieval results
            
        Returns:
            str: Formatted summary
        """
        text = doc["text"]
        metadata = doc["metadata"]
        
        # Extract key information
        sentences = text.split(", ")
        
        summary = f"[{metadata.get('category', 'General').upper()}] "
        if "program" in metadata:
            summary += f"{metadata['program']}: "
        
        summary += "; ".join(sentences[:2])  # First 2 sentences
        
        return summary
    
    def add_document(self, text: str, metadata: Dict = None):
        """
        Add a new document to the index.
        
        Args:
            text (str): Document text
            metadata (Dict): Document metadata
        """
        # Store document and metadata
        self.documents.append(text)
        self.metadata.append(metadata or {})
        
    def batch_retrieve(self, queries: List[str], top_k: int = 3) -> Dict[str, List[Dict]]:
        """
        Retrieve documents for multiple queries.
        
        Args:
            queries (List[str]): List of queries
            top_k (int): Number of results per query
            
        Returns:
            Dict[str, List[Dict]]: Results indexed by query
        """
        results = {}
        for query in queries:
            results[query] = self.retrieve(query, top_k)
        return results
    
    def evaluate_relevance(self, query: str, document: str, threshold: float = 0.2) -> bool:
        """
        Evaluate if a document is relevant to a query.
        
        Args:
            query (str): The query
            document (str): The document text
            threshold (float): Relevance threshold
            
        Returns:
            bool: Whether document is relevant
        """
        similarity = self._calculate_similarity(query, document)
        return similarity >= threshold


if __name__ == "__main__":
    # Initialize RAG pipeline
    print("Initializing RAG Pipeline...")
    rag = RAGPipeline()
    
    # Test queries
    test_queries = [
        "What is the eligibility for BS Electrical Engineering?",
        "When is the final exam?",
        "Am I eligible for scholarships?",
        "What is the minimum GPA?"
    ]
    
    print("\n" + "="*80)
    print("RAG PIPELINE RETRIEVAL RESULTS")
    print("="*80)
    
    for query in test_queries:
        print(f"\n\nQuery: {query}")
        print("-" * 80)
        
        results = rag.retrieve(query, top_k=3)
        
        for result in results:
            print(f"\n[Result {result['rank']}] Similarity: {result['similarity_score']:.2%}")
            print(f"Category: {result['metadata'].get('category', 'General')}")
            print(f"Text: {result['text'][:100]}...")
    
    print("\n" + "="*80)
