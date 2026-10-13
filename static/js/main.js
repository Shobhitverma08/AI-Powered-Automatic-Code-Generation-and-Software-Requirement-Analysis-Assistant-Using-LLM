/**
 * CodeMind AI - Frontend Single Page Application Client Logic
 * Handles tab navigation, API calls, dynamic rendering, and file exports.
 */

document.addEventListener("DOMContentLoaded", () => {
    // App State Store
    const state = {
        activeTab: "dashboard",
        isDemoMode: true,
        currentProjectId: null,
        currentRequirement: "",
        generatedCode: "",
        docMarkdown: ""
    };

    // Quick Preset Requirements
    const PRESETS = {
        student: {
            title: "Student Management System",
            req: "Create a Python student management system where an administrator can add, update, delete and search student records.",
            lang: "Python",
            type: "CLI / Console",
            complexity: "Intermediate"
        },
        ecommerce: {
            title: "E-Commerce REST API",
            req: "Design a RESTful API in JavaScript/Node.js for an e-commerce platform allowing users to view products, add items to cart, checkout, and process payments securely.",
            lang: "JavaScript",
            type: "REST API",
            complexity: "Advanced"
        },
        library: {
            title: "Library Management System",
            req: "Build a C++ library management application for tracking book inventory, issuing books to members, calculating late fines, and generating inventory reports.",
            lang: "C++",
            type: "CLI / Console",
            complexity: "Intermediate"
        }
    };

    // Initialize System Status
    fetchAppStatus();

    // Setup Event Listeners
    setupNavigation();
    setupDashboardActions();
    setupAnalyzerActions();
    setupGeneratorActions();
    setupReviewerActions();
    setupExplainerActions();
    setupDocsActions();
    setupHistoryActions();

    // =========================================================================
    // 1. Navigation & App Status
    // =========================================================================

    function fetchAppStatus() {
        fetch("/api/status")
            .then(res => res.json())
            .then(data => {
                state.isDemoMode = data.is_demo_mode;
                
                // Show Demo Banner if active
                const demoBanner = document.getElementById("demo-mode-banner");
                if (state.isDemoMode) {
                    demoBanner.style.display = "flex";
                } else {
                    demoBanner.style.display = "none";
                }

                // Update Stats Counter
                if (data.stats) {
                    document.getElementById("stat-projects").innerText = data.stats.projects || 0;
                    document.getElementById("stat-generations").innerText = data.stats.code_generations || 0;
                    document.getElementById("stat-reviews").innerText = data.stats.reviews || 0;
                    document.getElementById("stat-analyses").innerText = data.stats.analyses || 0;
                }

                // Render Recent Projects in Dashboard
                renderRecentProjects(data.recent_projects || []);
            })
            .catch(err => console.error("Error fetching app status:", err));
    }

    function setupNavigation() {
        const navItems = document.querySelectorAll(".nav-item");
        navItems.forEach(item => {
            item.addEventListener("click", () => {
                const targetTab = item.getAttribute("data-tab");
                switchTab(targetTab);
            });
        });

        // Delegate triggers with data-tab
        document.addEventListener("click", (e) => {
            const trigger = e.target.closest(".nav-trigger");
            if (trigger) {
                const targetTab = trigger.getAttribute("data-tab");
                switchTab(targetTab);
            }
        });
    }

    function switchTab(tabId) {
        state.activeTab = tabId;

        // Update nav item active states
        document.querySelectorAll(".nav-item").forEach(el => {
            if (el.getAttribute("data-tab") === tabId) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });

        // Hide all views, show selected
        document.querySelectorAll(".tab-view").forEach(view => {
            view.classList.remove("active");
        });

        const activeView = document.getElementById(`view-${tabId}`);
        if (activeView) activeView.classList.add("active");

        // Update titles
        const titleMap = {
            dashboard: { title: "Dashboard", desc: "Overview of software requirement analysis and code generations" },
            analyzer: { title: "Requirement Analyzer", desc: "Convert natural language specs into structured requirements & detect ambiguity" },
            generator: { title: "Code Generator", desc: "Automatically generate production-ready code with algorithmic breakdown" },
            reviewer: { title: "Code Reviewer", desc: "Automated static analysis, security checks, and quality scoring" },
            explainer: { title: "Code Explainer", desc: "Beginner-friendly step-by-step execution logic & variable analysis" },
            docs: { title: "Documentation Generator", desc: "Generate professional Software Requirement Specifications (SRS)" },
            history: { title: "Project History", desc: "Manage and revisit past project analyses, code gens, and reviews" }
        };

        if (titleMap[tabId]) {
            document.getElementById("view-title").innerText = titleMap[tabId].title;
            document.getElementById("view-desc").innerText = titleMap[tabId].desc;
        }

        if (tabId === "history") {
            loadHistoryTable();
        }
    }

    // =========================================================================
    // 2. Dashboard Actions
    // =========================================================================

    function setupDashboardActions() {
        document.querySelectorAll(".load-preset").forEach(btn => {
            btn.addEventListener("click", () => {
                const key = btn.getAttribute("data-preset");
                const preset = PRESETS[key];
                if (preset) {
                    // Populate Analyzer and switch view
                    document.getElementById("analyzer-req-input").value = preset.req;
                    document.getElementById("analyzer-language").value = preset.lang;
                    document.getElementById("analyzer-project-type").value = preset.type;
                    document.getElementById("analyzer-complexity").value = preset.complexity;

                    switchTab("analyzer");
                }
            });
        });
    }

    function renderRecentProjects(projects) {
        const container = document.getElementById("recent-projects-list");
        if (!projects || projects.length === 0) {
            container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.88rem;">No recent projects found. Create your first analysis!</p>`;
            return;
        }

        let html = `
            <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                <thead>
                    <tr style="text-align: left; border-bottom: 1px solid var(--border-color); color: var(--text-muted);">
                        <th style="padding: 0.6rem;">Project Name</th>
                        <th style="padding: 0.6rem;">Type</th>
                        <th style="padding: 0.6rem;">Language</th>
                        <th style="padding: 0.6rem;">Status</th>
                        <th style="padding: 0.6rem;">Action</th>
                    </tr>
                </thead>
                <tbody>
        `;

        projects.forEach(p => {
            html += `
                <tr style="border-bottom: 1px solid var(--border-color);">
                    <td style="padding: 0.75rem 0.6rem; font-weight: 600;">${p.name}</td>
                    <td style="padding: 0.75rem 0.6rem; color: var(--text-muted);">${p.type}</td>
                    <td style="padding: 0.75rem 0.6rem;"><span class="badge badge-low">${p.language}</span></td>
                    <td style="padding: 0.75rem 0.6rem;"><span class="badge badge-good">${p.status}</span></td>
                    <td style="padding: 0.75rem 0.6rem;">
                        <button class="btn btn-outline btn-sm open-project-btn" data-id="${p.id}" data-req="${encodeURIComponent(p.requirement)}" data-lang="${p.language}">Open</button>
                    </td>
                </tr>
            `;
        });

        html += `</tbody></table>`;
        container.innerHTML = html;

        // Attach event listener for Open buttons
        container.querySelectorAll(".open-project-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const reqText = decodeURIComponent(btn.getAttribute("data-req"));
                const lang = btn.getAttribute("data-lang");

                document.getElementById("analyzer-req-input").value = reqText;
                document.getElementById("analyzer-language").value = lang;
                switchTab("analyzer");
            });
        });
    }

    // =========================================================================
    // 3. Requirement Analyzer Logic
    // =========================================================================

    function setupAnalyzerActions() {
        // Ready-to-Use Demo Requirement Button
        document.getElementById("btn-load-demo-req").addEventListener("click", () => {
            const preset = PRESETS.student;
            document.getElementById("analyzer-req-input").value = preset.req;
            document.getElementById("analyzer-language").value = preset.lang;
            document.getElementById("analyzer-project-type").value = preset.type;
            document.getElementById("analyzer-complexity").value = preset.complexity;
        });

        document.getElementById("btn-run-analyzer").addEventListener("click", () => {
            const requirement = document.getElementById("analyzer-req-input").value.trim();
            if (!requirement) {
                alert("Please enter a software requirement to analyze.");
                return;
            }

            const project_type = document.getElementById("analyzer-project-type").value;
            const language = document.getElementById("analyzer-language").value;
            const complexity = document.getElementById("analyzer-complexity").value;

            // UI Loading state
            document.getElementById("analyzer-loading").style.display = "flex";
            document.getElementById("analyzer-output").style.display = "none";

            fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ requirement, project_type, language, complexity })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("analyzer-loading").style.display = "none";

                if (data.success && data.analysis) {
                    state.currentProjectId = data.project_id;
                    state.currentRequirement = requirement;
                    renderAnalysisOutput(data.analysis, requirement, language);
                    fetchAppStatus(); // Refresh counters
                } else {
                    alert(data.error || "Analysis failed.");
                }
            })
            .catch(err => {
                document.getElementById("analyzer-loading").style.display = "none";
                alert("Server error running requirement analysis.");
                console.error(err);
            });
        });

        // Proceed to Code Gen button
        document.getElementById("btn-proceed-to-code").addEventListener("click", () => {
            document.getElementById("gen-req-input").value = state.currentRequirement;
            document.getElementById("gen-language").value = document.getElementById("analyzer-language").value;
            switchTab("generator");
        });
    }

    function renderAnalysisOutput(analysis, requirement, language) {
        const outputDiv = document.getElementById("analyzer-output");
        outputDiv.style.display = "block";

        // Render Ambiguity Warning Banner if required
        const warnBox = document.getElementById("ambiguity-warning-box");
        if (analysis.is_ambiguous || (analysis.ambiguities && analysis.ambiguities.length > 0)) {
            warnBox.innerHTML = `
                <div class="ambiguity-banner">
                    <div class="ambiguity-title">⚠️ Your requirement is ambiguous. Additional information is recommended.</div>
                    <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">Detected Ambiguities / Missing Info:</p>
                    <ul style="margin-left: 1.25rem; font-size: 0.85rem;">
                        ${(analysis.ambiguities || []).map(a => `<li>${a}</li>`).join("")}
                        ${(analysis.missing_information || []).map(m => `<li>Missing Spec: ${m}</li>`).join("")}
                    </ul>
                </div>
            `;
        } else {
            warnBox.innerHTML = "";
        }

        // Problem Statement
        document.getElementById("res-problem-statement").innerText = analysis.problem_statement || "No problem statement specified.";

        // Functional Reqs
        document.getElementById("res-functional-reqs").innerHTML = 
            (analysis.functional_requirements || []).map(item => `<li>${item}</li>`).join("");

        // Non-Functional Reqs
        document.getElementById("res-nonfunctional-reqs").innerHTML = 
            (analysis.non_functional_requirements || []).map(item => `<li>${item}</li>`).join("");

        // Actors, Inputs, Outputs Pills
        document.getElementById("res-actors").innerHTML = 
            (analysis.actors || []).map(act => `<span class="detail-pill">👤 ${act}</span>`).join("");
        document.getElementById("res-inputs").innerHTML = 
            (analysis.inputs || []).map(inp => `<span class="detail-pill">📥 ${inp}</span>`).join("");
        document.getElementById("res-outputs").innerHTML = 
            (analysis.outputs || []).map(out => `<span class="detail-pill">📤 ${out}</span>`).join("");

        // Constraints & Suggestions
        document.getElementById("res-constraints").innerHTML = 
            (analysis.constraints || []).map(c => `<li>${c}</li>`).join("");
        document.getElementById("res-suggestions").innerHTML = 
            (analysis.suggestions || []).map(s => `<li>${s}</li>`).join("");
    }

    // =========================================================================
    // 4. Code Generator Logic
    // =========================================================================

    function setupGeneratorActions() {
        document.getElementById("btn-run-generator").addEventListener("click", () => {
            const requirement = document.getElementById("gen-req-input").value.trim();
            if (!requirement) {
                alert("Please specify a software requirement for code generation.");
                return;
            }

            const language = document.getElementById("gen-language").value;
            const complexity = document.getElementById("gen-complexity").value;
            const code_style = document.getElementById("gen-style").value;

            document.getElementById("generator-loading").style.display = "flex";
            document.getElementById("generator-output").style.display = "none";

            fetch("/api/generate-code", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    requirement,
                    language,
                    complexity,
                    code_style,
                    project_id: state.currentProjectId
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("generator-loading").style.display = "none";

                if (data.success && data.data) {
                    state.generatedCode = data.data.code;
                    renderGeneratedCode(data.data, language);
                    fetchAppStatus();
                } else {
                    alert(data.error || "Code generation failed.");
                }
            })
            .catch(err => {
                document.getElementById("generator-loading").style.display = "none";
                alert("Server error during code generation.");
                console.error(err);
            });
        });

        // Copy Code Button
        document.getElementById("btn-copy-code").addEventListener("click", () => {
            navigator.clipboard.writeText(state.generatedCode);
            alert("Source code copied to clipboard!");
        });

        // Download Code Button
        document.getElementById("btn-download-code").addEventListener("click", () => {
            const lang = document.getElementById("gen-language").value.toLowerCase();
            const extMap = { python: "py", javascript: "js", "c++": "cpp", java: "java" };
            const ext = extMap[lang] || "txt";

            const blob = new Blob([state.generatedCode], { type: "text/plain" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `codemind_solution.${ext}`;
            a.click();
            URL.revokeObjectURL(url);
        });

        // Shortcut to Review Generated Code
        document.getElementById("btn-review-generated").addEventListener("click", () => {
            document.getElementById("review-code-input").value = state.generatedCode;
            document.getElementById("review-language").value = document.getElementById("gen-language").value;
            switchTab("reviewer");
        });

        // Shortcut to Explain Generated Code
        document.getElementById("btn-explain-generated").addEventListener("click", () => {
            document.getElementById("explain-code-input").value = state.generatedCode;
            document.getElementById("explain-language").value = document.getElementById("gen-language").value;
            switchTab("explainer");
        });
    }

    function renderGeneratedCode(data, language) {
        document.getElementById("generator-output").style.display = "block";

        document.getElementById("code-lang-label").innerText = language;
        document.getElementById("generated-code-box").innerText = data.code || "// Code generation empty.";
        document.getElementById("gen-algorithm-text").innerText = data.algorithm || "Standard Modular Algorithm";

        document.getElementById("gen-time-complexity").innerText = `Time: ${data.time_complexity || 'O(N)'}`;
        document.getElementById("gen-space-complexity").innerText = `Space: ${data.space_complexity || 'O(1)'}`;
    }

    // =========================================================================
    // 5. Code Reviewer Logic
    // =========================================================================

    function setupReviewerActions() {
        document.getElementById("btn-run-reviewer").addEventListener("click", () => {
            const code = document.getElementById("review-code-input").value.trim();
            if (!code) {
                alert("Please paste source code to perform code review.");
                return;
            }

            const language = document.getElementById("review-language").value;

            document.getElementById("reviewer-loading").style.display = "flex";
            document.getElementById("reviewer-output").style.display = "none";

            fetch("/api/review-code", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code, language, project_id: state.currentProjectId })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("reviewer-loading").style.display = "none";

                if (data.success && data.data) {
                    renderReviewOutput(data.data);
                    fetchAppStatus();
                } else {
                    alert(data.error || "Code review failed.");
                }
            })
            .catch(err => {
                document.getElementById("reviewer-loading").style.display = "none";
                alert("Server error during code review.");
                console.error(err);
            });
        });

        document.getElementById("btn-copy-improved").addEventListener("click", () => {
            const improved = document.getElementById("improved-code-box").innerText;
            navigator.clipboard.writeText(improved);
            alert("Refactored code copied to clipboard!");
        });
    }

    function renderReviewOutput(data) {
        document.getElementById("reviewer-output").style.display = "block";

        // Score Badge
        document.getElementById("review-score-badge").innerText = data.score || 85;

        // Issues List
        const issuesContainer = document.getElementById("review-issues-list");
        if (!data.issues || data.issues.length === 0) {
            issuesContainer.innerHTML = `<p style="font-size: 0.88rem; color: var(--success);">No issues found! Excellent code quality.</p>`;
        } else {
            issuesContainer.innerHTML = data.issues.map(issue => {
                const sevClass = `badge-${(issue.severity || 'medium').toLowerCase()}`;
                return `
                    <div style="background-color: var(--bg-main); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                            <span style="font-weight: 700; font-size: 0.9rem;">${issue.title}</span>
                            <span class="badge ${sevClass}">${issue.severity}</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">${issue.description}</p>
                        <span style="font-size: 0.75rem; color: var(--primary); font-weight: 600;">Category: ${issue.category}</span>
                    </div>
                `;
            }).join("");
        }

        // Suggestions
        document.getElementById("review-suggestions-list").innerHTML = 
            (data.suggestions || []).map(s => `<li>${s}</li>`).join("");

        // Improved Code
        document.getElementById("improved-code-box").innerText = data.improved_code || "// No refactoring required.";
    }

    // =========================================================================
    // 6. Code Explainer Logic
    // =========================================================================

    function setupExplainerActions() {
        document.getElementById("btn-run-explainer").addEventListener("click", () => {
            const code = document.getElementById("explain-code-input").value.trim();
            if (!code) {
                alert("Please paste source code for explanation.");
                return;
            }

            const language = document.getElementById("explain-language").value;

            document.getElementById("explainer-loading").style.display = "flex";
            document.getElementById("explainer-output").style.display = "none";

            fetch("/api/explain-code", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code, language })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("explainer-loading").style.display = "none";

                if (data.success && data.data) {
                    renderExplainerOutput(data.data);
                } else {
                    alert(data.error || "Explanation failed.");
                }
            })
            .catch(err => {
                document.getElementById("explainer-loading").style.display = "none";
                alert("Server error generating explanation.");
                console.error(err);
            });
        });
    }

    function renderExplainerOutput(data) {
        document.getElementById("explainer-output").style.display = "block";

        document.getElementById("exp-summary").innerText = data.summary || "Code breakdown available.";

        document.getElementById("exp-steps-list").innerHTML = 
            (data.step_by_step || []).map(step => `<li>${step}</li>`).join("");

        document.getElementById("exp-components-list").innerHTML = 
            (data.key_components || []).map(c => `<li><strong>${c.name}</strong>: ${c.description}</li>`).join("");

        document.getElementById("exp-variables-list").innerHTML = 
            (data.important_variables || []).map(v => `<li><code>${v.name}</code>: ${v.description}</li>`).join("");
    }

    // =========================================================================
    // 7. Documentation Generator Logic
    // =========================================================================

    function setupDocsActions() {
        document.getElementById("btn-run-docs").addEventListener("click", () => {
            const requirement = document.getElementById("docs-req-input").value.trim() || state.currentRequirement;
            if (!requirement) {
                alert("Please specify a software requirement to generate documentation.");
                return;
            }

            const project_type = document.getElementById("docs-project-type").value;
            const language = document.getElementById("docs-language").value;

            document.getElementById("docs-loading").style.display = "flex";
            document.getElementById("docs-output").style.display = "none";

            fetch("/api/generate-docs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    requirement,
                    project_type,
                    language,
                    project_id: state.currentProjectId
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("docs-loading").style.display = "none";

                if (data.success && data.markdown) {
                    state.docMarkdown = data.markdown;
                    renderMarkdownDocs(data.markdown);
                } else {
                    alert(data.error || "Documentation generation failed.");
                }
            })
            .catch(err => {
                document.getElementById("docs-loading").style.display = "none";
                alert("Server error generating documentation.");
                console.error(err);
            });
        });

        // Copy Markdown
        document.getElementById("btn-copy-doc").addEventListener("click", () => {
            navigator.clipboard.writeText(state.docMarkdown);
            alert("Documentation Markdown copied to clipboard!");
        });

        // Download Markdown
        document.getElementById("btn-download-doc-md").addEventListener("click", () => {
            const blob = new Blob([state.docMarkdown], { type: "text/markdown" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "CodeMind_SRS_Documentation.md";
            a.click();
            URL.revokeObjectURL(url);
        });

        // Download PDF
        document.getElementById("btn-download-doc-pdf").addEventListener("click", () => {
            fetch("/api/export-pdf", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    markdown: state.docMarkdown,
                    title: "CodeMind_SRS_Documentation"
                })
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "CodeMind_SRS_Documentation.pdf";
                a.click();
                URL.revokeObjectURL(url);
            })
            .catch(err => {
                alert("Error exporting PDF");
                console.error(err);
            });
        });
    }

    function renderMarkdownDocs(markdown) {
        document.getElementById("docs-output").style.display = "block";
        const container = document.getElementById("markdown-doc-body");

        // Basic clean HTML parser for Markdown sections
        let html = markdown
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            .replace(/\n\n/gim, '<br>');

        container.innerHTML = html;
    }

    // =========================================================================
    // 8. Project History Logic
    // =========================================================================

    function setupHistoryActions() {
        // Table loads when switching to tab
    }

    function loadHistoryTable() {
        const container = document.getElementById("history-projects-table");
        container.innerHTML = `<p style="color: var(--text-muted);">Loading saved history...</p>`;

        fetch("/api/projects")
            .then(res => res.json())
            .then(data => {
                const projects = data.projects || [];
                if (projects.length === 0) {
                    container.innerHTML = `<p style="color: var(--text-muted);">No history records yet.</p>`;
                    return;
                }

                let html = `
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                        <thead>
                            <tr style="text-align: left; border-bottom: 2px solid var(--border-color); color: var(--text-muted);">
                                <th style="padding: 0.75rem;">ID</th>
                                <th style="padding: 0.75rem;">Project Title</th>
                                <th style="padding: 0.75rem;">Language</th>
                                <th style="padding: 0.75rem;">Type</th>
                                <th style="padding: 0.75rem;">Date</th>
                                <th style="padding: 0.75rem; text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                projects.forEach(p => {
                    html += `
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 0.75rem; color: var(--text-muted);">#${p.id}</td>
                            <td style="padding: 0.75rem; font-weight: 600;">${p.name}</td>
                            <td style="padding: 0.75rem;"><span class="badge badge-low">${p.language}</span></td>
                            <td style="padding: 0.75rem; color: var(--text-muted);">${p.type}</td>
                            <td style="padding: 0.75rem; color: var(--text-muted); font-size: 0.8rem;">${p.created_at}</td>
                            <td style="padding: 0.75rem; text-align: right;">
                                <button class="btn btn-outline btn-sm hist-open" data-id="${p.id}" data-req="${encodeURIComponent(p.requirement)}" data-lang="${p.language}">Open</button>
                                <button class="btn btn-outline btn-sm hist-dup" data-id="${p.id}">Duplicate</button>
                                <button class="btn btn-outline btn-sm hist-del" data-id="${p.id}" style="color: var(--danger); border-color: #fecaca;">Delete</button>
                            </td>
                        </tr>
                    `;
                });

                html += `</tbody></table>`;
                container.innerHTML = html;

                // Bind Action Handlers
                container.querySelectorAll(".hist-open").forEach(btn => {
                    btn.addEventListener("click", () => {
                        const reqText = decodeURIComponent(btn.getAttribute("data-req"));
                        const lang = btn.getAttribute("data-lang");
                        document.getElementById("analyzer-req-input").value = reqText;
                        document.getElementById("analyzer-language").value = lang;
                        switchTab("analyzer");
                    });
                });

                container.querySelectorAll(".hist-dup").forEach(btn => {
                    btn.addEventListener("click", () => {
                        const id = btn.getAttribute("data-id");
                        fetch(`/api/projects/${id}/duplicate`, { method: "POST" })
                            .then(res => res.json())
                            .then(() => loadHistoryTable());
                    });
                });

                container.querySelectorAll(".hist-del").forEach(btn => {
                    btn.addEventListener("click", () => {
                        const id = btn.getAttribute("data-id");
                        if (confirm("Are you sure you want to delete this project history entry?")) {
                            fetch(`/api/projects/${id}/delete`, { method: "DELETE" })
                                .then(res => res.json())
                                .then(() => loadHistoryTable());
                        }
                    });
                });
            });
    }
});
