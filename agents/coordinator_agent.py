"""
Coordinator Agent
Orchestrates all other agents and controls workflow
"""

from typing import Dict, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.intent_agent import IntentAgent
from agents.retrieval_agent import RetrievalAgent
from agents.policy_agent import PolicyAgent
from agents.verification_agent import VerificationAgent
from agents.interaction_agent import InteractionAgent


class CoordinatorAgent:
    """
    Coordinator agent that orchestrates all other agents.
    Controls workflow and resolves conflicts between agents.
    """
    
    def __init__(self):
        """Initialize the coordinator and all sub-agents."""
        self.agent_name = "Coordinator Agent"
        
        # Initialize all agents
        self.intent_agent = IntentAgent()
        self.retrieval_agent = RetrievalAgent()
        self.policy_agent = PolicyAgent()
        self.verification_agent = VerificationAgent()
        self.interaction_agent = InteractionAgent()
        
        # Track conversation history
        self.conversation_history = []
        self.execution_log = []
    
    def process_query(self, query: str, verbose: bool = False) -> Dict:
        """
        Process a student query through the entire agent pipeline.
        
        Args:
            query (str): Student query
            verbose (bool): Whether to print detailed execution info
            
        Returns:
            Dict: Final response with all agent results
        """
        # Initialize result structure
        result = {
            "query": query,
            "workflow": {},
            "final_response": "",
            "status": "success",
            "agents_executed": []
        }
        
        try:
            if verbose:
                print(f"\n🔄 Processing Query: {query}\n")
                print("="*80)
            
            # Step 1: Intent Detection
            if verbose:
                print("\n[Step 1] 🎯 Intent Detection Agent")
                print("-"*80)
            
            intent_result = self.intent_agent.process(query)
            result["workflow"]["intent"] = intent_result
            result["agents_executed"].append("Intent Agent")
            intent = intent_result["intent"]
            confidence = intent_result["confidence"]
            
            if verbose:
                print(f"Intent: {intent} (Confidence: {confidence:.1%})")
            
            # Step 2: Document Retrieval
            if verbose:
                print("\n[Step 2] 🔍 Document Retrieval Agent")
                print("-"*80)
            
            retrieval_result = self.retrieval_agent.process(query, intent, top_k=3)
            result["workflow"]["retrieval"] = retrieval_result
            result["agents_executed"].append("Retrieval Agent")
            documents = retrieval_result.get("documents", [])
            
            if verbose:
                print(f"Documents Retrieved: {retrieval_result['documents_retrieved']}")
                for doc in documents[:2]:
                    print(f"  - {doc['text'][:60]}...")
            
            # Step 3: Policy Interpretation
            if verbose:
                print("\n[Step 3] 📋 Policy Interpretation Agent")
                print("-"*80)
            
            policy_result = self.policy_agent.process(documents)
            result["workflow"]["policy"] = policy_result
            result["agents_executed"].append("Policy Agent")
            
            if verbose:
                print(f"Policies Extracted: {policy_result['num_policies']}")
            
            # Step 4: Verification
            if verbose:
                print("\n[Step 4] ✅ Verification Agent")
                print("-"*80)
            
            verification_result = self.verification_agent.process(policy_result)
            result["workflow"]["verification"] = verification_result
            result["agents_executed"].append("Verification Agent")
            
            if verbose:
                quality_score = verification_result.get("data_quality_score", 0)
                print(f"Data Quality Score: {quality_score:.1%}")
                
                if verification_result.get("issues"):
                    for issue in verification_result["issues"]:
                        print(f"  ⚠️ {issue}")
            
            # Step 5: Response Formatting
            if verbose:
                print("\n[Step 5] 💬 User Interaction Agent")
                print("-"*80)
            
            interaction_result = self.interaction_agent.process(policy_result, intent)
            result["workflow"]["interaction"] = interaction_result
            result["agents_executed"].append("Interaction Agent")
            
            final_response = interaction_result.get("formatted_response", "")
            result["final_response"] = final_response
            
            if verbose:
                print("Response formatted for user presentation")
            
            # Add suggestions
            suggestions = self.interaction_agent.get_followup_suggestions(intent)
            result["followup_suggestions"] = suggestions
            
            if verbose:
                print("\n" + "="*80)
                print("\n✅ FINAL RESPONSE:\n")
                print(final_response)
                
                if suggestions:
                    print("\n💡 You might also want to ask:")
                    for suggestion in suggestions:
                        print(f"  - {suggestion}")
            
            # Store in conversation history
            self.conversation_history.append({
                "query": query,
                "intent": intent,
                "response": final_response
            })
            
            return result
        
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            result["final_response"] = f"Error processing query: {str(e)}"
            
            if verbose:
                print(f"\n❌ Error: {str(e)}")
            
            return result
    
    def get_execution_summary(self, result: Dict) -> str:
        """
        Get a summary of the execution for a query.
        
        Args:
            result (Dict): Result from process_query
            
        Returns:
            str: Execution summary
        """
        summary = f"\n📊 EXECUTION SUMMARY\n"
        summary += "="*50 + "\n"
        summary += f"Query: {result['query']}\n"
        summary += f"Status: {result['status']}\n"
        summary += f"Agents Executed: {len(result['agents_executed'])}\n"
        
        for i, agent in enumerate(result['agents_executed'], 1):
            summary += f"  {i}. {agent}\n"
        
        if result['workflow'].get('intent'):
            intent_data = result['workflow']['intent']
            summary += f"\nIntent: {intent_data.get('intent')} (Confidence: {intent_data.get('confidence', 0):.1%})\n"
        
        if result['workflow'].get('retrieval'):
            retrieval_data = result['workflow']['retrieval']
            summary += f"Documents Retrieved: {retrieval_data.get('documents_retrieved', 0)}\n"
        
        if result['workflow'].get('verification'):
            verification_data = result['workflow']['verification']
            summary += f"Data Quality: {verification_data.get('data_quality_score', 0):.1%}\n"
        
        summary += "="*50 + "\n"
        
        return summary
    
    def handle_conversation(self, queries: List[str]) -> List[Dict]:
        """
        Handle multiple queries in a conversation.
        
        Args:
            queries (List[str]): List of queries
            
        Returns:
            List[Dict]: List of results
        """
        results = []
        
        for query in queries:
            result = self.process_query(query)
            results.append(result)
        
        return results
    
    def get_conversation_context(self) -> List[Dict]:
        """
        Get the current conversation context.
        
        Returns:
            List[Dict]: Conversation history
        """
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        self.execution_log = []
    
    def log_execution(self, log_entry: str):
        """
        Log an execution event.
        
        Args:
            log_entry (str): Log entry message
        """
        self.execution_log.append(log_entry)


if __name__ == "__main__":
    # Test coordinator agent
    print("Initializing Coordinator Agent...")
    print("Loading all sub-agents...\n")
    
    coordinator = CoordinatorAgent()
    
    # Test queries
    test_queries = [
        "What is the eligibility for BS Electrical Engineering?",
        "What is the minimum GPA requirement?"
    ]
    
    print("="*80)
    print("COORDINATOR AGENT FULL PIPELINE TEST")
    print("="*80)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'#'*80}")
        print(f"Query {i} of {len(test_queries)}")
        print(f"{'#'*80}")
        
        result = coordinator.process_query(query, verbose=True)
        
        # Print execution summary
        print("\n" + coordinator.get_execution_summary(result))
    
    # Show conversation history
    print("\n" + "="*80)
    print("CONVERSATION HISTORY")
    print("="*80)
    
    for i, turn in enumerate(coordinator.get_conversation_context(), 1):
        print(f"\nTurn {i}:")
        print(f"Query: {turn['query']}")
        print(f"Intent: {turn['intent']}")
