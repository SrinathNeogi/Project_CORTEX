<div align="center">

# 🧠 Project CORTEX

### **C**entralized **O**perational **R**esponsive **T**echnical **EX**ecution System

> *Your intelligent, offline-first desktop assistant — built for those who demand speed, privacy, and power.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational?style=for-the-badge)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)]()

</div>

---

## 📖 What is CORTEX?

**CORTEX** is a Python-based intelligent desktop voice assistant that puts you in control. It automates everyday system tasks, responds to your voice in real time, and adapts to your workflow — with deep system access, an offline-friendly design, and full developer customizability.

---

## ✨ Features

| &nbsp;&nbsp;&nbsp;Feature&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
|:---|:---|
| 🎙️ &nbsp;**Voice Command Recognition** | Speak naturally — CORTEX listens and understands |
| 📡 &nbsp;**Semi-Offline Capable** | Most features run locally; voice listener needs internet |
| 🖥️ &nbsp;**System Control** | Shutdown, restart, open apps, and manage your OS |
| 📂 &nbsp;**Smart File & PDF Finder** | Locate files instantly using fuzzy matching |
| 🔐 &nbsp;**Voice Authentication** | Secure access using your unique voiceprint |
| ⚡ &nbsp;**Fast Speech-to-Text** | Powered by OpenAI's Whisper for high accuracy |
| 🧩 &nbsp;**Modular Architecture** | Plug-and-play modules — easy to extend |
| ⚙️ &nbsp;**Custom Command Handling** | Define your own commands and automations |

---

---

## 💡 Why CORTEX?

Modern desktops and laptops lack a powerful, customizable, and privacy-conscious voice assistant. CORTEX was built to fill that gap.

- 🖥️ **Desktop-First** — Designed specifically for PC workflows, not mobile
- 🔒 **Privacy-Focused** — Most processing stays on your machine
- 🛠️ **Developer-Friendly** — Fully open, modular, and hackable
- ⚡ **Fast & Lightweight** — No bloated cloud dependencies slowing you down
- 🎯 **System-Level Control** — Goes deeper than any consumer assistant can

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| 🐍 **Core Language** | Python 3.10+ |
| 🎤 **Speech-to-Text** | Faster-Whisper / SpeechRecognition |
| 🤖 **Voice Auth** | Machine Learning (Custom Model) |
| 🖼️ **GUI** | PyQt / Tkinter |
| ⚙️ **System Automation** | OS Automation Libraries |
| 🔍 **Fuzzy Matching** | RapidFuzz |

</div>

---

## 📁 Project Structure

```
CORTEX/
│
├── 📄 main.py                  # Entry point — boot CORTEX here
├── ⚙️  .vscode/                 # Editor configuration
│
├── 🎯 Actions/                 # Command execution modules
├── 💾 Data/                    # Runtime and persistent data
├── 📚 Documents/               # Project documentation
├── 🧠 Learning_ML/             # ML training scripts & experiments
├── 🤖 Models/                  # Trained model files
├── 🖼️  UI/                      # Interface components
├── 🎙️  Voice/                   # Speech processing pipeline
├── 🔐 Voice_Authentication/    # Voiceprint auth system
│
└── 📦 requirements.txt         # Python dependencies
```

---

## 🚀 How It Works

```
  🎙️  You speak          ──►  🔊 Audio captured
  🔊 Audio captured      ──►  📝 Whisper converts to text
  📝 Text processed      ──►  🧠 NLP understands intent
  🧠 Intent classified   ──►  ⚡ Module triggered
  ⚡ Module executes     ──►  💬 CORTEX responds
```

Most of the pipeline runs **locally on your machine**. Note: the default voice listener (Google Speech Recognition) requires an internet connection. Full offline support via Whisper is on the roadmap.

---

## 🗣️ Example Commands

```bash
"Open Chrome"               # 🌐 Launches your browser instantly
"Shutdown the system"       # 💤 Safe system shutdown
"Find my PDF file"          # 📂 Smart file search with fuzzy matching
"What is the time?"         # 🕐 Real-time system clock response
"Locate India"              # 🗺️  Geographical information lookup
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10 or higher
- A working microphone
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/CORTEX.git
cd CORTEX

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch CORTEX
python main.py
```

---

## 🔮 Roadmap

The following features are planned for future releases:

- [ ] 🧩 **Fully Offline Speech Recognition** — No internet needed, ever
- [ ] 🤖 **Local LLM Integration** — Conversational AI without the cloud
- [ ] 📅 **Smart Task Scheduling** — Automate recurring tasks by voice
- [ ] 🌍 **Cross-Platform Compatibility** — Full Linux & macOS support
- [ ] 💬 **Advanced Conversational AI** — Context-aware, multi-turn dialogue

---



<div align="center">

## 👨‍💻 Author

**Srinath Neogi**

*Designed, Derived, and Developed with 💙*

---

*CORTEX — Bringing intelligence to your desktop, one command at a time.*

</div># Project_CORTEX
