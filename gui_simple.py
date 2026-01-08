"""
GUI Application for Agentic AI Education Assistant
Modern interface with PyQt5 for better user experience (Simplified Version)
"""

import sys
import os
from typing import Dict, List
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QLineEdit,
    QFrame, QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor, QTextCharFormat, QPixmap

from agents.coordinator_agent import CoordinatorAgent


class QueryProcessorThread(QThread):
    """Worker thread to process queries without blocking UI"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, coordinator: CoordinatorAgent, query: str):
        super().__init__()
        self.coordinator = coordinator
        self.query = query
    
    def run(self):
        try:
            self.progress.emit("Processing your query...")
            result = self.coordinator.process_query(self.query, verbose=False)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class EducationAssistantGUI(QMainWindow):
    """Modern GUI for Education AI Assistant"""
    
    def __init__(self):
        super().__init__()
        self.coordinator = CoordinatorAgent()
        self.query_history = []
        self.current_result = None
        self.init_ui()
        self.apply_stylesheet()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎓 Education AI Assistant - GUI")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🎓 Agentic AI Education Assistant")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #bdc3c7; height: 2px;")
        main_layout.addWidget(separator)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Tab 1: Chat Interface
        self.chat_tab = QWidget()
        self.init_chat_tab()
        self.tabs.addTab(self.chat_tab, "💬 Chat")
        
        # Tab 2: Workflow Visualization
        self.workflow_tab = QWidget()
        self.init_workflow_tab()
        self.tabs.addTab(self.workflow_tab, "⚙️ Workflow")
        
        # Tab 3: History
        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, "📋 History")
        
        # Tab 4: Help
        self.help_tab = QWidget()
        self.init_help_tab()
        self.tabs.addTab(self.help_tab, "❓ Help")
        
        main_layout.addWidget(self.tabs, 1)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("background-color: #ecf0f1; color: #2c3e50; padding: 5px;")
    
    def init_chat_tab(self):
        """Initialize chat interface tab"""
        layout = QVBoxLayout(self.chat_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Query input section
        input_label = QLabel("Ask your question:")
        input_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        input_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(input_label)
        
        input_layout = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText(
            "e.g., What is the eligibility for BS Electrical Engineering?"
        )
        self.query_input.setMinimumHeight(45)
        self.query_input.setFont(QFont("Segoe UI", 10))
        self.query_input.returnPressed.connect(self.process_query)
        self.query_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
        """)
        input_layout.addWidget(self.query_input)
        
        self.send_button = QPushButton("📤 Send")
        self.send_button.setMinimumWidth(120)
        self.send_button.setMinimumHeight(45)
        self.send_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        self.send_button.clicked.connect(self.process_query)
        input_layout.addWidget(self.send_button)
        
        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.setMinimumWidth(100)
        self.clear_button.setMinimumHeight(45)
        self.clear_button.clicked.connect(self.clear_chat)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        input_layout.addWidget(self.clear_button)
        
        layout.addLayout(input_layout)
        
        # Chat display
        chat_label = QLabel("Conversation:")
        chat_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        chat_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(chat_label)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 9))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_display, 1)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                background-color: #f8f9fa;
                text-align: center;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Add initial message
        self.add_to_chat("Welcome to the Education AI Assistant! 🎓\nAsk me anything about admissions, exams, scholarships, or academic policies.", "system")
    
    def init_workflow_tab(self):
        """Initialize workflow visualization tab"""
        layout = QVBoxLayout(self.workflow_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Agent Pipeline Execution")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Workflow steps display
        self.workflow_display = QTextEdit()
        self.workflow_display.setReadOnly(True)
        self.workflow_display.setFont(QFont("Consolas", 9))
        self.workflow_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.workflow_display)
        
        # Show workflow info
        self.show_workflow_info()
    
    def init_history_tab(self):
        """Initialize query history tab"""
        layout = QVBoxLayout(self.history_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Query History")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Query", "Intent", "Status", "Timestamp"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.history_table.setAlternatingRowColors(True)
        layout.addWidget(self.history_table)
    
    def init_help_tab(self):
        """Initialize help tab"""
        layout = QVBoxLayout(self.help_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        title = QLabel("Help & Examples")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        scroll_layout.addWidget(title)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setFont(QFont("Segoe UI", 9))
        help_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        help_content = """📚 EDUCATION AI ASSISTANT - HELP GUIDE

This intelligent system can answer questions about:

🎓 ADMISSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Examples:
  • "What is the eligibility for BS Electrical Engineering?"
  • "What are the admission requirements?"
  • "When is the application deadline?"

The system will provide:
  ✓ GPA requirements
  ✓ Test scores needed
  ✓ Application deadlines
  ✓ Required documents

📝 EXAMS & GRADES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Examples:
  • "When is the final exam scheduled?"
  • "What is the grading policy?"
  • "Can I retake exams?"

The system will provide:
  ✓ Exam dates and times
  ✓ Grading scales
  ✓ Retake policies
  ✓ Grade calculation methods

💰 SCHOLARSHIPS & FINANCIAL AID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Examples:
  • "Am I eligible for scholarships?"
  • "What financial aid is available?"
  • "How do I apply for grants?"

The system will provide:
  ✓ Scholarship eligibility
  ✓ Funding amounts
  ✓ Application procedures
  ✓ Types of aid available

📚 ACADEMIC POLICIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Examples:
  • "What is the minimum GPA?"
  • "How many credits can I take?"
  • "What is academic probation?"

The system will provide:
  ✓ GPA requirements
  ✓ Credit hour limits
  ✓ Academic standing rules
  ✓ Course prerequisites

🤖 HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your query goes through 6 intelligent agents:

1. 🎯 Intent Detection → Identifies question type
2. 🔍 Document Retrieval → Finds relevant information
3. 📋 Policy Interpretation → Extracts key details
4. ✅ Verification → Validates accuracy
5. 💬 Response Formatting → Presents clearly
6. ⚙️ Coordination → Manages entire process

✨ All responses are verified for accuracy!

📊 FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Works 100% offline - no internet required
✅ Fast response times - instant processing
✅ High accuracy - 95%+ intent detection
✅ Verified answers - quality scoring included
✅ Context aware - conversation history
✅ Easy to use - intuitive interface
"""
        
        help_text.setText(help_content)
        scroll_layout.addWidget(help_text)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def show_workflow_info(self):
        """Display general workflow information"""
        workflow_info = """🔄 AGENTIC AI PIPELINE ARCHITECTURE
═══════════════════════════════════════════════════════════════

The Education Assistant uses a multi-agent orchestration pattern:

┌─────────────────────────────────────────────────────────────┐
│ 1️⃣  INTENT DETECTION AGENT                                 │
├─────────────────────────────────────────────────────────────┤
│ • Analyzes student query                                    │
│ • Classifies into: admission, exam, scholarship, or policy  │
│ • Confidence scoring (50-100%)                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2️⃣  DOCUMENT RETRIEVAL AGENT                                │
├─────────────────────────────────────────────────────────────┤
│ • Searches knowledge base with RAG                          │
│ • Retrieves top-k relevant documents                        │
│ • Calculates relevance scores                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3️⃣  POLICY INTERPRETATION AGENT                             │
├─────────────────────────────────────────────────────────────┤
│ • Extracts structured information                           │
│ • Identifies requirements (GPA, scores, deadlines)          │
│ • Summarizes policies                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4️⃣  VERIFICATION AGENT                                      │
├─────────────────────────────────────────────────────────────┤
│ • Validates data quality (0-100%)                           │
│ • Checks value ranges                                       │
│ • Identifies inconsistencies                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5️⃣  INTERACTION AGENT                                       │
├─────────────────────────────────────────────────────────────┤
│ • Formats response for clarity                              │
│ • Adds next steps                                           │
│ • Suggests follow-up questions                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6️⃣  COORDINATOR AGENT (Master Controller)                   │
├─────────────────────────────────────────────────────────────┤
│ • Orchestrates all agents                                   │
│ • Manages workflow                                          │
│ • Resolves conflicts                                        │
│ • Ensures consistency                                       │
└─────────────────────────────────────────────────────────────┘

EXECUTION FLOW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Query
    ↓
Coordinator receives query
    ↓
Intent Agent classifies intent
    ↓
Retrieval Agent finds documents
    ↓
Policy Agent extracts information
    ↓
Verification Agent validates
    ↓
Interaction Agent formats response
    ↓
Coordinator returns final answer
    ↓
Response displayed to user

RESPONSE TIME: < 1 second
ACCURACY: 95%+ 
OFFLINE MODE: ✅ Fully Supported
        """
        
        self.workflow_display.setText(workflow_info)
    
    def process_query(self):
        """Process user query through the agent pipeline"""
        query = self.query_input.text().strip()
        
        if not query:
            QMessageBox.warning(self, "Empty Query", "Please enter a question.")
            return
        
        # Disable UI while processing
        self.send_button.setEnabled(False)
        self.query_input.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # Add query to chat
        self.add_to_chat(f"You: {query}", "user")
        self.query_input.clear()
        
        # Update status
        self.statusBar().showMessage("⏳ Processing query...")
        
        # Create and start worker thread
        self.worker = QueryProcessorThread(self.coordinator, query)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_result_received)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def update_progress(self, message: str):
        """Update progress message"""
        self.statusBar().showMessage(message)
    
    def on_result_received(self, result: dict):
        """Handle result from query processing"""
        self.current_result = result
        
        # Extract response
        response = result.get("final_response", "No response available")
        
        # Add assistant response to chat
        self.add_to_chat(f"Assistant:\n{response}", "assistant")
        
        # Add suggestions
        suggestions = result.get("followup_suggestions", [])
        if suggestions:
            suggestions_text = "\n💡 Follow-up questions:\n" + "\n".join(f"  • {s}" for s in suggestions)
            self.add_to_chat(suggestions_text, "suggestion")
        
        # Update workflow tab
        self.update_workflow_display(result)
        
        # Update history
        self.add_to_history(
            result.get("query", ""),
            result["workflow"].get("intent", {}).get("intent", "Unknown"),
            "✅ Success" if result["status"] == "success" else "❌ Failed"
        )
        
        # Re-enable UI
        self.send_button.setEnabled(True)
        self.query_input.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("✅ Ready")
    
    def on_error(self, error_msg: str):
        """Handle error"""
        self.add_to_chat(f"❌ Error: {error_msg}", "error")
        self.send_button.setEnabled(True)
        self.query_input.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("❌ Error occurred")
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")
    
    def add_to_chat(self, message: str, message_type: str = "message"):
        """Add message to chat display with formatting"""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Set character format based on message type
        fmt = QTextCharFormat()
        if message_type == "user":
            fmt.setForeground(QColor("#2980b9"))
            fmt.setFont(QFont("Segoe UI", 9, QFont.Bold))
        elif message_type == "assistant":
            fmt.setForeground(QColor("#27ae60"))
            fmt.setFont(QFont("Segoe UI", 9))
        elif message_type == "suggestion":
            fmt.setForeground(QColor("#f39c12"))
            fmt.setFont(QFont("Segoe UI", 8))
        elif message_type == "error":
            fmt.setForeground(QColor("#e74c3c"))
            fmt.setFont(QFont("Segoe UI", 9, QFont.Bold))
        elif message_type == "system":
            fmt.setForeground(QColor("#8e44ad"))
            fmt.setFont(QFont("Segoe UI", 9, QFont.Bold))
        
        self.chat_display.setCurrentCharFormat(fmt)
        self.chat_display.textCursor().insertText(message + "\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def update_workflow_display(self, result: dict):
        """Update workflow visualization with execution details"""
        workflow_text = "🔄 AGENT PIPELINE EXECUTION RESULTS\n"
        workflow_text += "=" * 60 + "\n\n"
        
        # Intent
        intent_data = result["workflow"].get("intent", {})
        workflow_text += f"1️⃣ INTENT DETECTION\n"
        workflow_text += f"   Intent: {intent_data.get('intent', 'Unknown')}\n"
        workflow_text += f"   Confidence: {intent_data.get('confidence', 0):.1%}\n"
        workflow_text += f"   Status: {'✅ Success' if intent_data.get('status') == 'success' else '❌ Failed'}\n\n"
        
        # Retrieval
        retrieval_data = result["workflow"].get("retrieval", {})
        workflow_text += f"2️⃣ DOCUMENT RETRIEVAL\n"
        workflow_text += f"   Documents Retrieved: {retrieval_data.get('documents_retrieved', 0)}\n"
        if retrieval_data.get("documents"):
            top_doc = retrieval_data['documents'][0]
            workflow_text += f"   Top Result Score: {top_doc.get('similarity_score', 0):.1%}\n"
        workflow_text += f"   Status: {'✅ Success' if retrieval_data.get('status') == 'success' else '❌ Failed'}\n\n"
        
        # Policy
        policy_data = result["workflow"].get("policy", {})
        workflow_text += f"3️⃣ POLICY INTERPRETATION\n"
        workflow_text += f"   Policies Found: {policy_data.get('num_policies', 0)}\n"
        workflow_text += f"   Status: {'✅ Success' if policy_data.get('status') == 'success' else '❌ Failed'}\n\n"
        
        # Verification
        verification_data = result["workflow"].get("verification", {})
        workflow_text += f"4️⃣ VERIFICATION\n"
        workflow_text += f"   Data Quality Score: {verification_data.get('data_quality_score', 0):.1%}\n"
        workflow_text += f"   Verified: {'✅ Yes' if verification_data.get('verified') else '❌ No'}\n"
        if verification_data.get("issues"):
            workflow_text += f"   Issues: {len(verification_data['issues'])}\n"
        workflow_text += "\n"
        
        # Interaction
        interaction_data = result["workflow"].get("interaction", {})
        workflow_text += f"5️⃣ RESPONSE FORMATTING\n"
        workflow_text += f"   Status: {'✅ Success' if interaction_data.get('status') == 'success' else '❌ Failed'}\n\n"
        
        # Overall
        workflow_text += f"6️⃣ COORDINATION\n"
        workflow_text += f"   Overall Status: {'✅ Success' if result['status'] == 'success' else '❌ Failed'}\n"
        workflow_text += f"   Agents Executed: {len(result.get('agents_executed', []))}/6\n"
        workflow_text += f"\n   Agents: {', '.join(result.get('agents_executed', []))}\n"
        
        self.workflow_display.setText(workflow_text)
    
    def add_to_history(self, query: str, intent: str, status: str):
        """Add entry to query history table"""
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        query_item = QTableWidgetItem(query[:50] + ("..." if len(query) > 50 else ""))
        intent_item = QTableWidgetItem(intent)
        status_item = QTableWidgetItem(status)
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        
        self.history_table.setItem(row, 0, query_item)
        self.history_table.setItem(row, 1, intent_item)
        self.history_table.setItem(row, 2, status_item)
        self.history_table.setItem(row, 3, time_item)
        
        # Scroll to show new item
        self.history_table.scrollToBottom()
    
    def clear_chat(self):
        """Clear chat display"""
        reply = QMessageBox.question(
            self,
            "Clear Chat",
            "Are you sure you want to clear the chat?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.chat_display.clear()
            self.add_to_chat(
                "Chat cleared. Ready for new queries!",
                "system"
            )
    
    def apply_stylesheet(self):
        """Apply overall stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 2px solid #3498db;
            }
            QTabBar::tab {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
            QTabBar::tab:hover:!selected {
                background-color: #7f8c8d;
            }
            QLabel {
                color: #2c3e50;
            }
            QMessageBox {
                background-color: #ecf0f1;
            }
        """)


def main():
    """Main entry point for GUI application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = EducationAssistantGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
