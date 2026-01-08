## 🎨 GUI Version - User Guide

The GUI version provides a modern, user-friendly interface for the Education AI Assistant.

### 🚀 Launching the GUI

```bash
python gui_simple.py
```

### 📱 Interface Overview

The GUI has 4 main tabs:

#### 1. 💬 Chat Tab
- **Query Input**: Type your question in the text field
- **Send Button**: Submit your query
- **Clear Button**: Clear chat history
- **Chat Display**: Shows conversation history with color-coded messages
  - 🔵 **Blue**: Your questions
  - 🟢 **Green**: Assistant responses
  - 🟠 **Orange**: Follow-up suggestions
  - 🔴 **Red**: Error messages

#### 2. ⚙️ Workflow Tab
- Shows the agent pipeline architecture
- Displays execution results after each query
- Shows:
  - Intent detected
  - Documents retrieved
  - Quality score
  - Overall status

#### 3. 📋 History Tab
- Table of all queries processed
- Columns: Query, Intent, Status, Timestamp
- Shows up to 100 most recent queries

#### 4. ❓ Help Tab
- Examples for different query types
- How the system works
- Tips and tricks

### ✨ Features

- **Real-time Processing**: Uses threading to keep UI responsive
- **Beautiful Design**: Modern PyQt5 interface with custom styling
- **Color-Coded Messages**: Easy to read chat history
- **Execution Details**: See how each agent processed your query
- **Query History**: Track all your questions
- **Status Bar**: Real-time status updates

### 📋 Example Queries

**Admissions:**
- "What is the eligibility for BS Electrical Engineering?"
- "What are the admission requirements?"
- "When is the application deadline?"

**Exams:**
- "When is the final exam scheduled?"
- "What is the grading policy?"
- "Can I retake exams?"

**Scholarships:**
- "Am I eligible for scholarships?"
- "What financial aid is available?"
- "How do I apply for grants?"

**Academic Policies:**
- "What is the minimum GPA?"
- "How many credits can I take?"
- "What is academic probation?"

### 🔧 System Requirements

- Python 3.8+
- PyQt5
- All dependencies from main app.py

### 📊 Execution Pipeline View

In the **Workflow** tab, you can see:
- ✅ Intent Detection results
- ✅ Document Retrieval performance
- ✅ Policy Interpretation findings
- ✅ Verification scores
- ✅ Response formatting status
- ✅ Coordinator management info

Each step shows success/failure status and relevant metrics.

### 💾 Data Quality Indicators

The system shows data quality scores:
- 🟢 **90-100%**: Excellent quality
- 🟡 **70-90%**: Good quality
- 🟠 **50-70%**: Fair quality
- 🔴 **<50%**: Low quality

### 🎯 Tips for Best Results

1. **Be Specific**: The more details you provide, the better the response
2. **Use Keywords**: Include relevant terms like "GPA", "SAT", "deadline"
3. **One Question at a Time**: Ask one clear question per query
4. **Check History**: Review past queries in the History tab

### 🐛 Troubleshooting

**GUI doesn't open:**
- Ensure PyQt5 is installed: `pip install PyQt5`
- Check Python version (3.8+)

**Slow responses:**
- First query may take longer (model initialization)
- Subsequent queries should be fast

**Can't type in input box:**
- Click on the input field to focus
- Press Enter or click Send button

### 📝 Keyboard Shortcuts

- **Enter**: Submit query (when in input field)
- **Escape**: Clear input field (standard)
- **Tab**: Move between UI elements

### 🌟 GUI Improvements Over CLI

✅ Cleaner interface  
✅ Visual feedback  
✅ Easier to read responses  
✅ History tracking  
✅ Workflow visualization  
✅ No typing "exit"  
✅ Suggests follow-up questions  
✅ Real-time status updates  
✅ Professional appearance  
✅ Multi-tab interface  

Enjoy using the Education AI Assistant! 🎓
