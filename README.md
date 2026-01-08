# Agentic AI–Based Intelligent Education Service Assistance System

This project implements an AI-based education service assistant for university students.

## Features
- **Intent Classification**: Uses DistilBERT to classify student queries into categories (admission, exam, scholarship, academic_policy)
- **Retrieval-Augmented Generation (RAG)**: Uses FAISS for semantic document retrieval
- **Multi-Agent Architecture**: Orchestrated AI agents for specialized tasks
- **Agent Types**:
  - **Intent Agent**: Detects query intent
  - **Retrieval Agent**: Fetches relevant academic documents
  - **Policy Agent**: Interprets academic policies
  - **Verification Agent**: Validates factual correctness
  - **Interaction Agent**: Formats responses for users
  - **Coordinator Agent**: Orchestrates all agents and controls workflow

## Query Categories
- **Admissions**: Eligibility, application deadlines, requirements
- **Exams**: Exam schedules, grading policies, retake rules
- **Scholarships**: Eligibility, application process, funding info
- **Academic Policies**: Course registration, GPA requirements, academic standing

## Tech Stack
- **Python 3.8+**
- **Transformers** (DistilBERT for intent classification)
- **Sentence Transformers** (for document embeddings)
- **FAISS** (for vector similarity search)
- **GPT-based LLM** (for response generation)
- **Custom Agent Framework**

## Project Structure
```
education-ai-assistant/
├── data/
│   ├── admissions/
│   ├── exams/
│   ├── scholarships/
│   └── academics/
├── agents/
│   ├── coordinator_agent.py
│   ├── intent_agent.py
│   ├── retrieval_agent.py
│   ├── policy_agent.py
│   ├── verification_agent.py
│   └── interaction_agent.py
├── ml/
│   └── intent_classifier.py
├── rag/
│   └── rag_pipeline.py
├── app.py
└── README.md
```

## Installation

```bash
pip install transformers sentence-transformers faiss-cpu torch numpy pandas
```

## Usage

```bash
python app.py
```

Enter your query when prompted. Example queries:
- "What is the eligibility for BS Electrical Engineering?"
- "When is the next exam for CS101?"
- "Am I eligible for scholarships?"
- "What is the minimum GPA required?"

## Sample Output

```
Query: What is the eligibility for BS Electrical Engineering?

[Intent Detected] admission

[Documents Retrieved] 3 relevant documents found

[Policy Interpretation] 
- Minimum GPA: 3.2
- Required Tests: SAT/ACT
- Application Deadline: March 31, 2024

[Verification] Information verified against official policies

[Response]
To be eligible for BS Electrical Engineering, you need:
1. Minimum GPA of 3.2 or above
2. Successful completion of SAT/ACT
3. Submit application before March 31, 2024
```

## Agent Workflow

1. **Coordinator Agent** receives user query
2. **Intent Agent** classifies the query
3. **Retrieval Agent** fetches relevant documents
4. **Policy Agent** extracts key information
5. **Verification Agent** validates accuracy
6. **Interaction Agent** formats final response
7. **Coordinator** returns response to user

## Future Enhancements
- Multi-turn conversation support
- Real-time document updates
- User authentication and session management
- Analytics and feedback loop
- Support for multiple languages
