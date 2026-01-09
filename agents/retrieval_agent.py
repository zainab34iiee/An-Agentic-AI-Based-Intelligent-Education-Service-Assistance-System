"""
Retrieval Agent
Retrieves relevant academic documents using RAG pipeline
"""

from typing import List, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_pipeline import RAGPipeline


class RetrievalAgent:
    """
    Agent that retrieves relevant academic documents using RAG.
    Searches document database for query-relevant information.
    """
    
    def __init__(self):
        """Initialize the retrieval agent with RAG pipeline."""
        self.rag = RAGPipeline()
        self.agent_name = "Document Retrieval Agent"
    
    def process(self, query: str, intent: str = None, top_k: int = 3) -> Dict:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query (str): The student query
            intent (str): Optional query intent for targeted retrieval
            top_k (int): Number of top results to return
            
        Returns:
            Dict: Retrieval results with documents and metadata
        """
        try:
            if intent:
                # Retrieve documents filtered by intent category
                documents = self.rag.retrieve_by_category(query, intent, top_k)
            else:
                # Retrieve top documents without filtering
                documents = self.rag.retrieve(query, top_k)
            
            # Format results
            formatted_docs = []
            for doc in documents:
                formatted_doc = {
                    "rank": doc["rank"],
                    "text": doc["text"],
                    "category": doc["metadata"].get("category", "General"),
                    "similarity_score": doc["similarity_score"],
                    "metadata": doc["metadata"]
                }
                formatted_docs.append(formatted_doc)
            
            result = {
                "agent": self.agent_name,
                "query": query,
                "intent": intent,
                "documents_retrieved": len(formatted_docs),
                "documents": formatted_docs,
                "status": "success"
            }
            
            return result
        
        except Exception as e:
            result = {
                "agent": self.agent_name,
                "query": query,
                "intent": intent,
                "documents_retrieved": 0,
                "documents": [],
                "status": "failed",
                "error": str(e)
            }
            
            return result
    
    def add_document(self, text: str, metadata: Dict = None):
        """
        Add a new document to the retrieval database.
        
        Args:
            text (str): Document text
            metadata (Dict): Document metadata
        """
        self.rag.add_document(text, metadata)
    
    def batch_retrieve(self, queries: List[str], intent: str = None, top_k: int = 3) -> List[Dict]:
        """
        Retrieve documents for multiple queries.
        
        Args:
            queries (List[str]): List of queries
            intent (str): Optional intent for filtering
            top_k (int): Number of results per query
            
        Returns:
            List[Dict]: List of retrieval results
        """
        results = []
        for query in queries:
            result = self.process(query, intent, top_k)
            results.append(result)
        
        return results
    
    def get_document_summary(self, document: Dict) -> str:
        """
        Get a summary of a document's content.
        
        Args:
            document (Dict): Document from retrieval results
            
        Returns:
            str: Formatted summary
        """
        return document.get("text", "")[:150] + "..."
    
    def filter_documents_by_category(self, documents: List[Dict], category: str) -> List[Dict]:
        """
        Filter documents by category.
        
        Args:
            documents (List[Dict]): List of documents
            category (str): Category to filter by
            
        Returns:
            List[Dict]: Filtered documents
        """
        return [d for d in documents if d["category"] == category]


if __name__ == "__main__":
    # Test retrieval agent
    print("Initializing Retrieval Agent...")
    agent = RetrievalAgent()
    
    # Test queries
    test_queries = [
        ("What is the eligibility for BS Electrical Engineering?", "admission"),
        ("When is the final exam?", "exam"),
        ("Am I eligible for scholarships?", "scholarship")
    ]
    
    print("="*80)
    print("RETRIEVAL AGENT TEST RESULTS")
    print("="*80)
    
    for query, intent in test_queries:
        result = agent.process(query, intent, top_k=2)
        
        print(f"\nQuery: {query}")
        print(f"Intent: {intent}")
        print(f"Documents Retrieved: {result['documents_retrieved']}")
        
        for doc in result["documents"]:
            print(f"\n  [{doc['rank']}] {doc['category']} (Score: {doc['similarity_score']:.2%})")
            print(f"      {doc['text'][:80]}...")
    
    print("\n" + "="*80)
