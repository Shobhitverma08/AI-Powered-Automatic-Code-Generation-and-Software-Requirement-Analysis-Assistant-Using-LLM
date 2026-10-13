"""
LLM Service Abstraction Layer for CodeMind AI
Encapsulates Gemini API calls with automatic JSON parsing and graceful Demo Mode fallback.
"""

import os
import json
import requests
from dotenv import load_dotenv

import prompt_templates
import sample_data

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        # Default model for Gemini REST API
        self.model_name = "gemini-1.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def is_demo_mode(self):
        """Returns True if no valid GEMINI_API_KEY is configured."""
        return not bool(self.api_key) or self.api_key == "your_api_key_here"

    def _call_gemini_api(self, prompt_text):
        """Dispatches prompt to Gemini REST API."""
        if self.is_demo_mode():
            raise ValueError("Demo Mode Active: No API Key")

        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "maxOutputTokens": 4096
            }
        }

        response = requests.post(self.api_url, headers=headers, params=params, json=payload, timeout=25)
        if response.status_code != 200:
            raise RuntimeError(f"Gemini API Error {response.status_code}: {response.text}")

        data = response.json()
        try:
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return raw_text
        except (KeyError, IndexError):
            raise RuntimeError("Invalid response structure from Gemini API")

    def _parse_json_response(self, raw_text):
        """Extracts JSON content safely even if wrapped in markdown block backticks."""
        clean_text = raw_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        
        clean_text = clean_text.strip()
        return json.loads(clean_text)

    def analyze_requirement(self, requirement, project_type="Web App", language="Python", complexity="Intermediate"):
        """Analyzes software requirements, detecting ambiguities and structure."""
        if self.is_demo_mode():
            # Check if this matches default demo requirement
            if "student" in requirement.lower():
                return sample_data.STUDENT_MANAGEMENT_ANALYSIS
            
            # Dynamic demo fallback for custom inputs
            return {
                "problem_statement": f"Software solution required for: {requirement}",
                "functional_requirements": [
                    f"System shall execute main workflow for {project_type}.",
                    "System shall provide input validation and status tracking.",
                    "System shall maintain secure records in target datastore."
                ],
                "non_functional_requirements": [
                    "Response time latency under 1.5 seconds.",
                    "Scalable architecture adhering to clean code principles.",
                    "Comprehensive error reporting."
                ],
                "actors": ["Primary User", "System Administrator"],
                "inputs": ["User Parameters", "Configuration Options"],
                "outputs": ["Execution Results", "Formatted Status Reports"],
                "constraints": [f"Implementation language: {language}", f"Complexity scope: {complexity}"],
                "assumptions": ["Stable network and datastore access."],
                "ambiguities": ["Specific database schema and auth roles not fully defined."],
                "missing_information": ["Target deployment environment details."],
                "suggestions": ["Add unit test suite", "Incorporate API rate limiting"],
                "is_ambiguous": True
            }

        prompt = prompt_templates.REQUIREMENT_ANALYSIS_PROMPT.format(
            requirement=requirement,
            project_type=project_type,
            language=language,
            complexity=complexity
        )
        try:
            raw_res = self._call_gemini_api(prompt)
            return self._parse_json_response(raw_res)
        except Exception as err:
            print(f"[LLMService Error] analyze_requirement fallback: {err}")
            return sample_data.STUDENT_MANAGEMENT_ANALYSIS

    def generate_code(self, requirement, language="Python", complexity="Intermediate", code_style="Clean/Modular"):
        """Generates source code with complexity metrics and explanations."""
        if self.is_demo_mode():
            if "student" in requirement.lower() and language.lower() == "python":
                return {
                    "code": sample_data.STUDENT_MANAGEMENT_CODE,
                    "algorithm": "Object-Oriented Data Access Layer with SQLite B-Tree Indexing",
                    "short_explanation": "Provides a robust Python Student Management System featuring persistent database CRUD operations and input regex validation.",
                    "time_complexity": "O(1) search by primary key ID, O(N) list search",
                    "space_complexity": "O(N) database record storage"
                }
            
            # Generic demo code snippet for other languages
            lang_lower = language.lower()
            if "c++" in lang_lower:
                code_snippet = '''#include <iostream>\n#include <vector>\n#include <string>\n\nclass SystemManager {\npublic:\n    void execute() {\n        std::cout << "System initialized successfully.\\n";\n    }\n};\n\nint main() {\n    SystemManager app;\n    app.execute();\n    return 0;\n}'''
            elif "javascript" in lang_lower or "node" in lang_lower:
                code_snippet = '''class SystemService {\n    constructor(name) {\n        this.name = name;\n    }\n    async process() {\n        console.log(`[${this.name}] Processing requirement...`);\n        return { success: true };\n    }\n}\nmodule.exports = SystemService;'''
            else:
                code_snippet = f'''# {language} Solution for: {requirement}\n\ndef main():\n    print("CodeMind AI generated module for {requirement}")\n\nif __name__ == "__main__":\n    main()\n'''
                
            return {
                "code": code_snippet,
                "algorithm": "Standard Modular Solution Pattern",
                "short_explanation": f"Generated functional code boilerplate in {language} for specified requirement.",
                "time_complexity": "O(N)",
                "space_complexity": "O(1)"
            }

        prompt = prompt_templates.CODE_GENERATION_PROMPT.format(
            requirement=requirement,
            language=language,
            complexity=complexity,
            code_style=code_style
        )
        try:
            raw_res = self._call_gemini_api(prompt)
            return self._parse_json_response(raw_res)
        except Exception as err:
            print(f"[LLMService Error] generate_code fallback: {err}")
            return {
                "code": sample_data.STUDENT_MANAGEMENT_CODE,
                "algorithm": "Object-Oriented Data Access Layer with SQLite B-Tree Indexing",
                "short_explanation": "Provides a robust Python Student Management System featuring persistent database CRUD operations.",
                "time_complexity": "O(1) search by ID",
                "space_complexity": "O(N)"
            }

    def review_code(self, code, language="Python"):
        """Performs static code review, scoring, and severity issue tagging."""
        if self.is_demo_mode():
            if "StudentDatabase" in code or "student" in code.lower():
                return sample_data.STUDENT_MANAGEMENT_REVIEW
            return {
                "score": 88,
                "issues": [
                    {
                        "category": "Bugs / Potential Issues",
                        "severity": "Medium",
                        "title": "Missing Explicit Return Type / Bounds Check",
                        "description": "Ensure input parameters undergo strict validation before processing."
                    },
                    {
                        "category": "Security Issues",
                        "severity": "Good",
                        "title": "No Hardcoded Credentials Detected",
                        "description": "Code follows safe parameter handling practices."
                    }
                ],
                "suggestions": [
                    "Add comprehensive docstrings for exported functions.",
                    "Implement automated unit tests with pytest."
                ],
                "improved_code": f"// Enhanced version in {language}\n" + code
            }

        prompt = prompt_templates.CODE_REVIEW_PROMPT.format(code=code, language=language)
        try:
            raw_res = self._call_gemini_api(prompt)
            return self._parse_json_response(raw_res)
        except Exception as err:
            print(f"[LLMService Error] review_code fallback: {err}")
            return sample_data.STUDENT_MANAGEMENT_REVIEW

    def explain_code(self, code, language="Python"):
        """Provides beginner-friendly step-by-step code explanation."""
        if self.is_demo_mode():
            if "StudentDatabase" in code or "student" in code.lower():
                return sample_data.STUDENT_MANAGEMENT_CODE_EXPLANATION
            return {
                "summary": f"This program written in {language} establishes core workflow operations with error handling.",
                "step_by_step": [
                    "1. Setup & Imports: Loads essential standard library modules.",
                    "2. Execution Logic: Initializes primary data structures and control flow.",
                    "3. Output Handling: Formats results for clean user interaction."
                ],
                "key_components": [
                    {"name": "Main Workflow", "description": "Coordinates application lifecycle."}
                ],
                "important_variables": [
                    {"name": "config", "description": "Holds runtime setup variables."}
                ],
                "algorithm": "Modular Function Dispatch",
                "time_complexity": "O(N)",
                "space_complexity": "O(1)"
            }

        prompt = prompt_templates.CODE_EXPLANATION_PROMPT.format(code=code, language=language)
        try:
            raw_res = self._call_gemini_api(prompt)
            return self._parse_json_response(raw_res)
        except Exception as err:
            print(f"[LLMService Error] explain_code fallback: {err}")
            return sample_data.STUDENT_MANAGEMENT_CODE_EXPLANATION

    def generate_documentation(self, requirement, project_type="Web App", language="Python"):
        """Generates complete Software Requirement Specification in Markdown."""
        if self.is_demo_mode():
            if "student" in requirement.lower():
                return sample_data.STUDENT_MANAGEMENT_DOCS
            
            return f"""# Software Requirement Specification (SRS)
## Project: System Assistant ({language})
**Generated by CodeMind AI**

---

### 1. Project Overview
System specification designed to fulfill natural language requirement: "{requirement}".

### 2. Functional Requirements
- **FR-1**: User authentication and session management.
- **FR-2**: Execution of core business logic in {language}.
- **FR-3**: Formatted output reporting.

### 3. System Architecture & Stack
- **Language**: {language}
- **Type**: {project_type}
- **Persistence**: SQLite Datastore

### 4. Future Scope
- RAG-based documentation search
- GitHub automated workflow integration
- Automatic unit-test generation
- UML diagram auto-rendering
"""

        prompt = prompt_templates.DOCUMENTATION_PROMPT.format(
            requirement=requirement,
            project_type=project_type,
            language=language
        )
        try:
            return self._call_gemini_api(prompt)
        except Exception as err:
            print(f"[LLMService Error] generate_documentation fallback: {err}")
            return sample_data.STUDENT_MANAGEMENT_DOCS
