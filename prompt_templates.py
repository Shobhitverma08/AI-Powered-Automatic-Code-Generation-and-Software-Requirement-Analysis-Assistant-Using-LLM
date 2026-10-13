"""
Prompt Templates for CodeMind AI
Provides structured system & user prompts for LLM operations.
"""

REQUIREMENT_ANALYSIS_PROMPT = """
You are an expert Software Architect and Business Analyst.
Analyze the following natural language software requirement and output a structured JSON object.

Target Project Parameters:
- Project Type: {project_type}
- Target Language: {language}
- Target Complexity: {complexity}

User Requirement:
"{requirement}"

Respond strictly with valid JSON conforming to this schema (do NOT include markdown code block backticks inside JSON strings):
{{
  "problem_statement": "Clear, professional synthesis of the problem being solved.",
  "functional_requirements": ["Array of functional requirement strings..."],
  "non_functional_requirements": ["Array of non-functional requirement strings (performance, security, usability)..."],
  "actors": ["Array of system user roles/actors..."],
  "inputs": ["Array of expected system inputs..."],
  "outputs": ["Array of expected system outputs..."],
  "constraints": ["Array of technical or operational constraints..."],
  "assumptions": ["Array of system assumptions..."],
  "ambiguities": ["Array of ambiguous phrases or unclear requirements found in text..."],
  "missing_information": ["Array of missing specifications recommended for clarification..."],
  "suggestions": ["Array of architectural improvements..."],
  "is_ambiguous": true_or_false
}}
"""

CODE_GENERATION_PROMPT = """
You are an expert Software Engineer.
Generate production-ready source code based on the software requirement provided below.

Target Specifications:
- Language: {language}
- Difficulty Level: {complexity}
- Code Style: {code_style}

Software Requirement:
"{requirement}"

Structure your response strictly as a valid JSON object matching this schema:
{{
  "code": "Complete, production-ready, well-commented source code string.",
  "algorithm": "Summary of the core algorithm or pattern used.",
  "short_explanation": "Concise summary of how the code satisfies the requirement.",
  "time_complexity": "Time complexity estimation e.g., O(N log N).",
  "space_complexity": "Space complexity estimation e.g., O(N)."
}}
"""

CODE_REVIEW_PROMPT = """
You are a Principal Code Reviewer and Lead Security Auditor.
Review the following source code for bugs, logical flaws, security risks, performance bottlenecks, and code quality.

Language: {language}

Source Code:
```
{code}
```

Structure your response strictly as a valid JSON object:
{{
  "score": 85,
  "issues": [
    {{
      "category": "Bugs / Potential Issues | Logical Issues | Security Issues | Performance Issues",
      "severity": "Critical | High | Medium | Low | Good",
      "title": "Short title of issue",
      "description": "Detailed explanation of the issue."
    }}
  ],
  "suggestions": ["List of overall code improvement suggestions..."],
  "improved_code": "Refactored/improved version of the code resolving identified issues."
}}
"""

CODE_EXPLANATION_PROMPT = """
You are a friendly Software Engineering Tutor.
Explain the following source code in a beginner-friendly, structured manner.

Language: {language}

Source Code:
```
{code}
```

Structure your response strictly as a valid JSON object:
{{
  "summary": "Beginner-friendly high-level overview of what this code does.",
  "step_by_step": ["Step 1 explanation...", "Step 2 explanation...", "Step 3 explanation..."],
  "key_components": [
    {{"name": "Component Name", "description": "What it does"}}
  ],
  "important_variables": [
    {{"name": "variable_name", "description": "Purpose and data type"}}
  ],
  "algorithm": "Core algorithm/design pattern used.",
  "time_complexity": "Time complexity e.g., O(N)",
  "space_complexity": "Space complexity e.g., O(1)"
}}
"""

DOCUMENTATION_PROMPT = """
You are a Technical Writer and Software Architect.
Generate a comprehensive Software Requirement Specification (SRS) and Technical Documentation in Markdown format.

Project Requirement:
"{requirement}"

Language/Stack: {language}
Project Type: {project_type}

Ensure the documentation includes the following sections formatted in GitHub-Flavored Markdown:
1. Project Overview & Objectives
2. Problem Statement
3. Functional Requirements
4. Non-Functional Requirements
5. System Requirements & Tech Stack
6. System Architecture & Modules
7. Algorithm & Data Flow
8. Future Scope (Include items such as RAG-based documentation analysis, GitHub integration, automatic unit-test generation, UML diagram generation, multi-agent workflows, CI/CD integration)
"""
