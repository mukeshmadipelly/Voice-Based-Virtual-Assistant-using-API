# Voice-Based Virtual Assistant

A Python-based virtual assistant with voice recognition, AI responses, and task automation.

---

## 📌 Project Overview

This is a voice-controlled virtual assistant that performs tasks using natural language commands. It integrates:

* **Speech Recognition (STT)**
* **AI-Powered Responses (NLP)**
* **Task Automation** (app control, web search)
* **Image Generation** (AI-based)
* **Interactive GUI** (PyQt5)

---

## 🚀 Features

* **Voice Commands** – Speak naturally to execute tasks.
* **Smart AI Responses** – Context-aware replies using NLP.
* **Automation** – Open/close apps, search Google/YouTube.
* **AI Image Generation** – Create images from text prompts.
* **Real-Time Web Search** – Fetch latest information.
* **Interactive GUI** – Visual feedback for commands.

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

* **Python 3.10+** ([Download](https://www.python.org/downloads/))
* **FFmpeg** (For audio processing)
* **ChromeDriver** (For web automation)

### 2️⃣ Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate # Linux/Mac
.\.venv\Scripts\activate # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```
Username=YourName
Assistantname=JARVIS
InputLanguage=en # Language for speech recognition
HuggingFaceAPIKey=your_api_key # For image generation
```

### 5️⃣ Run the Project

```bash
python Main.py
```

---

## 🔧 Project Structure

```
JarvisAI/
├── Backend/
│ ├── Automation.py           # Task automation
│ ├── Chatbot.py              # AI responses
│ ├── Model.py                # Decision-making logic
│ ├── RealTimeSearchEngine.py # Web searches
│ ├── SpeechToText.py         # Voice recognition
│ └── TextToSpeech.py         # Voice output
├── Frontend/
│ ├── GUI.py                  # PyQt5 interface
│ └── Graphics/               # UI assets
├── Data/                     # Chat logs & temp files
├── .env                      # Configuration
├── Main.py                   # Entry point
└── requirements.txt          # Dependencies
```

---

## 💡 Usage

1.  **Launch the GUI**:
    * Run `python Main.py`.
    * Click the mic button to start listening.

2.  **Give Voice Commands**:
    * "Open Chrome" → Launches browser.
    * "Search for AI news" → Performs a Google search.
    * "Generate an image of a cat" → Creates AI art.

3.  **Toggle Mic**:
    * Click the mic icon to enable/disable listening.

---

## 📌 Notes

* **For Developers**: Modify `Automation.py` to add custom commands.
* **For Better Accuracy**: Use a noise-canceling microphone.
* **Troubleshooting**: Check `Data/` logs for errors.

Enjoy your AI assistant!

---

## 🔗 Dependencies Used

* **PyQt5** (GUI)
* **SpeechRecognition** (STT)
* **cohere** (NLP)
* **transformers** (AI models)
* **selenium** (Web automation)
