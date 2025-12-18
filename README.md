🤖 AI Talk: Intelligent SQL Assistant
AI Talk is a sophisticated desktop application designed to bridge the gap between natural language and complex relational databases. By leveraging Google's Gemini AI, the application allows users to interact with their data using plain English or voice commands, instantly generating SQL, fetching results, and providing audible feedback.
🌟 Key Features
Natural Language to SQL: Converts human questions into optimized SQL queries using the Gemini API.

Voice-Activated Querying: Hands-free interaction via high-accuracy Speech-to-Text (STT).

Audible AI Feedback: Real-time verbal responses using pyttsx3 for an interactive assistant experience.

Data Visualization: Automatically generates Bar, Line, and Pie charts from query results.

Clean Architecture: A modular code structure separating UI, Core Logic, and Database Management.

Schema-Aware Prompting: The AI understands your database structure (tables/columns) for precise accuracy.
📂 Project Organization
The project follows a Modular Design to ensure scalability and ease of debugging.

app.py: The main entry point that launches the GUI.

main.py: Orchestrates the flow between the AI, the database, and the UI.

core/: The "Engine" of the application.

db_manager.py: Manages all MySQL/SQLite connections and executions.

speech_handler.py: Handles pyttsx3 (Text-to-Speech) and voice input processing.

history_manager.py: Stores previous queries for quick user reference.

exporter.py: Allows users to export query results to CSV or Excel.

ui/: Contains the CustomTkinter interface definitions and styling.

assets/: Stores static resources like branding logos and application icons.
🛠️ Tech Stack
Category,Technology Used
Language,Python 3.12+
AI Engine,Google Gemini API
GUI Framework,CustomTkinter (Modern Tkinter)
Voice (TTS),pyttsx3 (Offline Support)
Voice (STT),SpeechRecognition
Data Analysis,Pandas & Matplotlib
Database,MySQL / MySQL-Connector

🚀 Getting Started
1. Prerequisites
Python 3.12+ installed.
A Google Gemini API Key (available via Google AI Studio).
A running MySQL Database (or local SQLite file).

2. Installation
Clone the Repo:
git clone https://github.com/your-username/ai-talk-sql-assistant.git
cd ai-talk-sql-assistant
Install Dependencies:
pip install -r requirements.txt
Running the App
python app.py
🛡️ Security & Safety
For production environments, it is strongly recommended to use a Read-Only Database User. This prevents the AI from executing destructive commands like DROP TABLE or DELETE, ensuring your data remains safe.

🛣️ Roadmap
[ ] Support for NoSQL (MongoDB) integration.
[ ] Multi-turn conversational memory (follow-up questions).
[ ] Cloud-based Web Version (Flask/React).
[ ] Advanced Excel reporting integration.
Developed by Jaiswal Sahil Uday Kumar Bina Project Presentation Date: December 18, 2025
