# 🤖 AI Talk: Intelligent SQL Assistant

**AI Talk** is a modern desktop application that bridges the gap between natural language and complex databases. Using advanced AI and voice recognition, it allows users to query databases using plain English or voice commands, instantly generating SQL code, fetching data, and creating beautiful visualizations.

---

## 🌟 Key Features

- **Natural Language to SQL:** Transform English questions into precise SQL queries using Google's Gemini AI.
- **Voice-Activated Querying:** Speak your data questions directly into the app for a hands-free experience.
- **Live Data Visualization:** Automatically generate Bar, Line, and Pie charts from your query results.
- **Voice Feedback:** Get audible confirmation and results read aloud using Text-to-Speech (TTS).
- **Modern UI:** A sleek, professional Dark Mode interface built with CustomTkinter.
- **Schema Awareness:** The AI automatically understands your database tables and columns for accurate results.

---

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **AI Model:** Google Gemini API
- **GUI Framework:** CustomTkinter (Modern Tkinter)
- **Database:** MySQL / SQLite
- **Audio Engines:** - `SpeechRecognition` (Speech-to-Text)
  - `pyttsx3` (Text-to-Speech)
- **Data Analysis:** Pandas & Matplotlib

---

## 🚀 Getting Started

### Prerequisites
- Python installed on your machine.
- A Google Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/)).
- A running MySQL server (or an SQLite file).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/ai-talk-sql-assistant.git](https://github.com/your-username/ai-talk-sql-assistant.git)
   cd ai-talk-sql-assistant
