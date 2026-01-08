"""
Main Application - Agentic AI Education Assistant
Entry point for the education service assistance system
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator_agent import CoordinatorAgent


def print_banner():
    """Print application banner."""
    banner = """
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║     🎓 AGENTIC AI EDUCATION SERVICE ASSISTANCE SYSTEM 🎓          ║
    ║                                                                    ║
    ║              Multi-Agent Intelligent Query Resolution              ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_instructions():
    """Print user instructions."""
    instructions = """
    Welcome! Ask me about:
    ✓ Admissions - Eligibility, requirements, deadlines
    ✓ Exams - Schedules, grading policies, retakes
    ✓ Scholarships - Financial aid, eligibility
    ✓ Academic Policies - GPA requirements, course registration
    
    Type 'exit' to quit the system
    Type 'help' for more information
    
    """
    print(instructions)


def print_help():
    """Print help information."""
    help_text = """
    HELP - QUERY EXAMPLES
    ═════════════════════════════════════════════════════════════════
    
    📋 ADMISSIONS:
    • "What is the eligibility for BS Electrical Engineering?"
    • "What are the requirements to apply?"
    • "When is the application deadline?"
    
    📝 EXAMS:
    • "When is the next exam?"
    • "What is my final grade?"
    • "Can I retake the midterm?"
    
    💰 SCHOLARSHIPS:
    • "Am I eligible for scholarships?"
    • "What financial aid options are available?"
    • "How do I apply for grants?"
    
    📚 ACADEMIC POLICIES:
    • "What is the minimum GPA requirement?"
    • "What are the academic standing rules?"
    • "Can I register late?"
    
    ═════════════════════════════════════════════════════════════════
    """
    print(help_text)


def process_user_query(coordinator, query: str, verbose: bool = False):
    """
    Process a user query through the agent pipeline.
    
    Args:
        coordinator: CoordinatorAgent instance
        query (str): User query
        verbose (bool): Whether to show detailed processing info
    """
    print("\n" + "="*70)
    print("PROCESSING YOUR QUERY")
    print("="*70 + "\n")
    
    # Process query through agent pipeline
    result = coordinator.process_query(query, verbose=True)
    
    # Display results
    if result["status"] == "success":
        print("\n" + "="*70)
        print("📋 RESPONSE")
        print("="*70)
        
        print(result["final_response"])
        
        # Show follow-up suggestions
        if result.get("followup_suggestions"):
            print("\n💡 SUGGESTED FOLLOW-UP QUESTIONS:")
            print("-"*70)
            for i, suggestion in enumerate(result["followup_suggestions"], 1):
                print(f"{i}. {suggestion}")
    
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error occurred')}")
    
    print("\n" + "="*70 + "\n")


def run_interactive_mode(coordinator):
    """
    Run the application in interactive mode.
    
    Args:
        coordinator: CoordinatorAgent instance
    """
    print_banner()
    print_instructions()
    
    while True:
        try:
            # Get user input
            query = input("📝 Enter your query (or 'exit' to quit): ").strip()
            
            if not query:
                print("Please enter a valid query.\n")
                continue
            
            if query.lower() == "exit":
                print("\n👋 Thank you for using the Education Assistant!")
                print("Goodbye!\n")
                break
            
            if query.lower() == "help":
                print_help()
                continue
            
            # Process query
            process_user_query(coordinator, query)
        
        except KeyboardInterrupt:
            print("\n\n👋 Application terminated by user.")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again.\n")


def run_demo_mode(coordinator):
    """
    Run demo with predefined queries.
    
    Args:
        coordinator: CoordinatorAgent instance
    """
    print_banner()
    
    print("🚀 Running Demo Mode\n")
    
    demo_queries = [
        "What is the eligibility for BS Electrical Engineering?",
        "When is the final exam scheduled?",
        "Am I eligible for scholarships?",
        "What is the minimum GPA to maintain good academic standing?"
    ]
    
    print(f"Processing {len(demo_queries)} sample queries...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'='*70}")
        print(f"DEMO QUERY {i} of {len(demo_queries)}")
        print(f"{'='*70}\n")
        
        process_user_query(coordinator, query, verbose=False)
        
        print("\n⏳ Press Enter to continue to next query...")
        input()


def run_batch_mode(coordinator, queries: list):
    """
    Run the application in batch mode with multiple queries.
    
    Args:
        coordinator: CoordinatorAgent instance
        queries (list): List of queries to process
    """
    print_banner()
    print(f"Processing {len(queries)} queries in batch mode...\n")
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Processing: {query}")
        result = coordinator.process_query(query)
        results.append({
            "query": query,
            "intent": result["workflow"].get("intent", {}).get("intent"),
            "success": result["status"] == "success"
        })
    
    # Print summary
    print("\n" + "="*70)
    print("BATCH PROCESSING SUMMARY")
    print("="*70)
    
    successful = sum(1 for r in results if r["success"])
    
    print(f"Total Queries: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print("\nResults:")
    
    for i, result in enumerate(results, 1):
        status = "✅" if result["success"] else "❌"
        print(f"{i}. {status} {result['query']}")
        if result.get("intent"):
            print(f"   Intent: {result['intent']}")


def main():
    """Main entry point of the application."""
    print("Initializing Agentic AI Education Assistant...\n")
    
    try:
        # Initialize coordinator agent
        coordinator = CoordinatorAgent()
        print("✅ All agents loaded successfully!\n")
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "--demo":
                # Run demo mode
                run_demo_mode(coordinator)
            
            elif sys.argv[1] == "--query":
                # Process single query from command line
                if len(sys.argv) > 2:
                    query = " ".join(sys.argv[2:])
                    print_banner()
                    process_user_query(coordinator, query)
                else:
                    print("Please provide a query with --query argument")
            
            elif sys.argv[1] == "--help":
                print_help()
            
            else:
                print(f"Unknown argument: {sys.argv[1]}")
                print("Usage: python app.py [--demo|--query \"query text\"|--help]")
        
        else:
            # Run interactive mode by default
            run_interactive_mode(coordinator)
    
    except ImportError as e:
        print(f"\n❌ Import Error: {str(e)}")
        print("Make sure all required dependencies are installed:")
        print("pip install transformers sentence-transformers faiss-cpu torch numpy pandas")
    
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
