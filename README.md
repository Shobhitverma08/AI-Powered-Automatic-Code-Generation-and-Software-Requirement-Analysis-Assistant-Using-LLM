# CodeMind AI — AI-Powered Software Requirement & Code Assistant

> **College Mini-Project Prototype**  
> An intelligent software engineering assistant that converts natural-language requirements into structured specifications, automatically generates production-ready source code, performs static code reviews, provides step-by-step logic explanations, and generates complete Software Requirement Specifications (SRS).

---

## 🌟 Features Overview

1. **Dashboard Hub**: Displays analytics counters (Projects, Code Generations, Code Reviews, Analyses) and quick-action presets for sample projects (Student Management System, E-Commerce REST API, Library System).
2. **Software Requirement Analyzer & Ambiguity Detector**:
   - Converts raw software requirements into structured JSON specifications (Problem Statement, Functional/Non-Functional Reqs, Actors, Inputs, Outputs, Constraints, Assumptions).
   - Automatically detects vague or incomplete requirements and renders a prominent warning banner with clarification questions.
3. **Automated Source Code Generator**:
   - Supports Python, JavaScript, C++, and Java.
   - Configurable difficulty levels (Beginner, Intermediate, Advanced) and code architecture styles (Clean/Modular, OOP, Functional, Concise).
   - Generates code with syntax viewports, copy/download options, algorithm summaries, and Time/Space complexity metrics (\(O(N)\), \(O(1)\)).
4. **Code Reviewer & Security Auditor**:
   - Assigns an Overall Code Quality Score (0–100).
   - Categorizes bugs, logical flaws, security risks, and performance bottlenecks with severity badges (**Critical**, **High**, **Medium**, **Low**, **Good**).
   - Generates a refactored/improved version of the source code.
5. **Beginner-Friendly Code Explainer**:
   - Breaks down complex code into high-level summaries, step-by-step execution logic, key functions/classes, and important variables.
6. **Automatic Software Documentation Generator (SRS)**:
   - Renders a complete SRS document in Markdown with options to copy text, download `.md` files, or export as `.pdf`.
7. **SQLite Project History & Persistence**:
   - Automatically saves all project sessions, requirements, generated code, and reviews.
   - Allows users to **Open**, **Duplicate**, or **Delete** past projects.
8. **Built-in Demo Mode**:
   - If `GEMINI_API_KEY` is not present, CodeMind AI automatically runs in Demo Mode using realistic sample datasets so the prototype remains 100% functional for presentations and testing without an API key.

---

## 🎨 Theme & UI Design

- **Light & Eyecatchy Theme**: Designed with a clean light slate (`#f8fafc`) background, pure white (`#ffffff`) cards, soft indigo (`#4f46e5`) accents, light cyan highlights, and crisp typography.
- **Dark Code Viewport**: Code containers use a high-contrast dark navy (`#0f172a`) theme to maximize syntax highlighting readability while keeping the rest of the application light and visually pleasant.

---

## 🏗️ System Architecture

```
                               ┌───────────────────────────────────┐
                               │       User Web Browser / SPA      │
                               └─────────────────┬─────────────────┘
                                                 │ HTTP / JSON API
                               ┌─────────────────▼─────────────────┐
                               │      Flask Backend (app.py)       │
                               └────────┬─────────────────┬────────┘
                                        │                 │
               ┌────────────────────────▼─┐             ┌─▼────────────────────────┐
               │ SQLite Database          │             │ LLM Service              │
               │ (database.py)            │             │ (llm_service.py)         │
               └──────────────────────────┘             └─────────┬──────┬─────────┘
                                                                  │      │
                                             ┌────────────────────▼┐    ┌▼───────────────────┐
                                             │ Gemini REST API     │    │ Demo Mode Fallback │
                                             │ (GEMINI_API_KEY)    │    │ (sample_data.py)   │
                                             └─────────────────────┘    └────────────────────┘
```

---

## 📁 Directory Structure

```
c:\Users\verma\OneDrive\Desktop\mini project (3rd year)\
├── .env.example              # Environment variables template
├── .gitignore                 # Version control exclusions
├── README.md                  # Comprehensive project documentation
├── requirements.txt           # Python library dependencies
├── app.py                     # Flask server & API routes controller
├── database.py                # SQLite database management module
├── llm_service.py             # LLM Service abstraction & Gemini API integration
├── prompt_templates.py        # Structured JSON prompt engineering templates
├── sample_data.py             # Realistic mock responses for Demo Mode
├── static/
│   ├── css/
│   │   └── style.css          # Light, eyecatchy theme & layout stylesheet
│   └── js/
│       └── main.js            # Frontend single-page app client logic
└── templates/
    └── index.html             # Main single-page web app template
```

---

## ⚙️ Installation & Setup Instructions

### Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- `pip` package manager

### 1. Clone or Extract Project Files
Navigate to the project root directory:
```bash
cd "c:\Users\verma\OneDrive\Desktop\mini project (3rd year)"
```

### 2. Install Dependencies
Install all required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=5000
HOST=127.0.0.1
DEBUG=True
```
> **Note**: If `GEMINI_API_KEY` is omitted or left as default, CodeMind AI automatically runs in **Demo Mode** with full functionality!

---

## 🚀 Running the Application

Run the Flask application:
```bash
python app.py
```

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔮 Future Scope & System Enhancements

- **RAG-based Software Documentation Analysis**: Enable context retrieval across college policy documents and enterprise software specs using Retrieval-Augmented Generation.
- **GitHub Integration**: Direct repository committing and pull request generation.
- **Automatic Unit Test Generation**: Auto-generating `pytest`, `Jest`, or `JUnit` test suites.
- **UML Diagram Auto-Rendering**: Generating PlantUML/Mermaid Sequence and Class diagrams from requirements.
- **Multi-Agent Software Workflow**: Orchestrating sub-agents for database schema design, backend API generation, and frontend code creation.
- **CI/CD Pipeline Generation**: Auto-building GitHub Actions or GitLab CI configuration files.
