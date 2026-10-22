"""
CodeMind AI Flask Backend Server
Provides API endpoints for Requirement Analysis, Code Generation, Code Review, Explanation, Documentation, and Project Management.
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file, Response
from dotenv import load_dotenv
import io

import database
from llm_service import LLMService

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "codemind-ai-secret-key-2026")

# Initialize SQLite Database on startup
database.init_db()

# Initialize LLM Service Instance
llm_service = LLMService()

@app.route("/")
def index():
    """Renders main single-page web app."""
    return render_template("index.html")

@app.after_request
def add_cache_headers(response):
    """Enables browser caching for static assets to eliminate redundant disk reads."""
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns application status, demo mode flag, dashboard counts, and runtime cache stats."""
    stats = database.get_dashboard_stats()
    recent = database.get_recent_projects(limit=5)
    return jsonify({
        "status": "online",
        "app_name": "CodeMind AI",
        "subtitle": "AI-Powered Software Requirement & Code Assistant",
        "is_demo_mode": llm_service.is_demo_mode(),
        "stats": stats,
        "recent_projects": recent,
        "model_name": llm_service.model_name,
        "cache_stats": llm_service.get_cache_stats()
    })

@app.route("/api/test-connection", methods=["GET"])
def test_connection():
    """Performs live connectivity verification with Gemini API."""
    result = llm_service.test_connection()
    return jsonify(result)

@app.route("/api/analyze", methods=["POST"])
def analyze_requirement():
    """Analyzes natural language requirements."""
    data = request.json or {}
    requirement = data.get("requirement", "").strip()
    project_type = data.get("project_type", "Web App")
    language = data.get("language", "Python")
    complexity = data.get("complexity", "Intermediate")
    project_name = data.get("project_name", "").strip() or f"{language} {project_type} System"

    if not requirement:
        return jsonify({"error": "Please enter a valid software requirement."}), 400

    # Execute LLM analysis
    analysis_result = llm_service.analyze_requirement(requirement, project_type, language, complexity)

    # Save to SQLite Database
    project_id = database.save_project(project_name, project_type, language, complexity, requirement, status="Analyzed")
    database.save_analysis(project_id, requirement, analysis_result)

    return jsonify({
        "success": True,
        "project_id": project_id,
        "analysis": analysis_result
    })

@app.route("/api/generate-code", methods=["POST"])
def generate_code():
    """Generates source code based on requirement."""
    data = request.json or {}
    requirement = data.get("requirement", "").strip()
    language = data.get("language", "Python")
    complexity = data.get("complexity", "Intermediate")
    code_style = data.get("code_style", "Clean/Modular")
    project_id = data.get("project_id")

    if not requirement:
        return jsonify({"error": "Requirement text cannot be empty."}), 400

    code_res = llm_service.generate_code(requirement, language, complexity, code_style)

    if project_id:
        database.save_code_generation(
            project_id=project_id,
            language=language,
            code=code_res.get("code", ""),
            algorithm=code_res.get("algorithm", ""),
            explanation=code_res.get("short_explanation", ""),
            time_complexity=code_res.get("time_complexity", ""),
            space_complexity=code_res.get("space_complexity", "")
        )

    return jsonify({
        "success": True,
        "data": code_res
    })

@app.route("/api/review-code", methods=["POST"])
def review_code():
    """Reviews provided source code."""
    data = request.json or {}
    code = data.get("code", "").strip()
    language = data.get("language", "Python")
    project_id = data.get("project_id")

    if not code:
        return jsonify({"error": "Please provide source code for review."}), 400

    review_res = llm_service.review_code(code, language)

    if project_id:
        database.save_code_review(
            project_id=project_id,
            language=language,
            score=review_res.get("score", 85),
            review_data=review_res,
            improved_code=review_res.get("improved_code", "")
        )

    return jsonify({
        "success": True,
        "data": review_res
    })

@app.route("/api/explain-code", methods=["POST"])
def explain_code():
    """Generates beginner-friendly step-by-step code explanation."""
    data = request.json or {}
    code = data.get("code", "").strip()
    language = data.get("language", "Python")

    if not code:
        return jsonify({"error": "Code cannot be empty."}), 400

    explanation_res = llm_service.explain_code(code, language)

    return jsonify({
        "success": True,
        "data": explanation_res
    })

@app.route("/api/generate-docs", methods=["POST"])
def generate_docs():
    """Generates Markdown SRS documentation."""
    data = request.json or {}
    requirement = data.get("requirement", "").strip()
    project_type = data.get("project_type", "Web App")
    language = data.get("language", "Python")
    project_id = data.get("project_id")

    if not requirement:
        return jsonify({"error": "Requirement is required to generate documentation."}), 400

    doc_markdown = llm_service.generate_documentation(requirement, project_type, language)

    if project_id:
        database.save_documentation(project_id, doc_markdown)

    return jsonify({
        "success": True,
        "markdown": doc_markdown
    })

@app.route("/api/export-pdf", methods=["POST"])
def export_pdf():
    """Converts markdown documentation to downloadable PDF file."""
    data = request.json or {}
    doc_markdown = data.get("markdown", "")
    title = data.get("title", "CodeMind_Documentation")

    try:
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 14)
                self.set_text_color(79, 70, 229) # Indigo
                self.cell(0, 10, 'CodeMind AI - System Documentation', border=False, align='L')
                self.ln(12)
                self.set_draw_color(226, 232, 240)
                self.line(10, 22, 200, 22)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 9)
                self.set_text_color(148, 163, 184)
                self.cell(0, 10, f'Page {self.page_no()}', border=False, align='C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(30, 41, 59)

        # Parse markdown lines into PDF elements cleanly
        lines = doc_markdown.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(4)
                continue
            if line.startswith('# '):
                pdf.set_font('Helvetica', 'B', 16)
                pdf.set_text_color(15, 23, 42)
                pdf.cell(0, 10, line[2:].encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font('Helvetica', '', 11)
                pdf.set_text_color(30, 41, 59)
            elif line.startswith('## '):
                pdf.set_font('Helvetica', 'B', 13)
                pdf.set_text_color(79, 70, 229)
                pdf.cell(0, 8, line[3:].encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font('Helvetica', '', 11)
                pdf.set_text_color(30, 41, 59)
            elif line.startswith('### '):
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_text_color(14, 165, 233)
                pdf.cell(0, 7, line[4:].encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font('Helvetica', '', 11)
                pdf.set_text_color(30, 41, 59)
            elif line.startswith('- '):
                pdf.multi_cell(0, 6, f"  * {line[2:]}".encode('latin-1', 'replace').decode('latin-1'))
            else:
                pdf.multi_cell(0, 6, line.encode('latin-1', 'replace').decode('latin-1'))

        pdf_bytes = pdf.output()
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment;filename={title}.pdf"}
        )
    except Exception as e:
        print(f"[PDF Export Warning] {e}")
        # Plain text fallback response
        return Response(
            doc_markdown.encode('utf-8'),
            mimetype="text/plain",
            headers={"Content-Disposition": f"attachment;filename={title}.txt"}
        )

@app.route("/api/projects", methods=["GET"])
def list_projects():
    """Retrieves all project history from SQLite."""
    projects = database.get_recent_projects(limit=50)
    return jsonify({"projects": projects})

@app.route("/api/projects/<int:project_id>/delete", methods=["DELETE"])
def delete_project_route(project_id):
    """Deletes project from database."""
    success = database.delete_project(project_id)
    return jsonify({"success": success})

@app.route("/api/projects/<int:project_id>/duplicate", methods=["POST"])
def duplicate_project_route(project_id):
    """Duplicates an existing project."""
    new_id = database.duplicate_project(project_id)
    if new_id:
        return jsonify({"success": True, "new_project_id": new_id})
    return jsonify({"error": "Project not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"\n=======================================================")
    print(f"CodeMind AI Assistant starting on http://{host}:{port}")
    print(f"=======================================================\n")
    app.run(host=host, port=port, debug=True)

