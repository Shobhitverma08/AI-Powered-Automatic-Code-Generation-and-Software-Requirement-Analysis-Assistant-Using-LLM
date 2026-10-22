/**
 * CodeMind AI — Frontend Developer Studio Engine
 * Handles single-page state, Lucide iconography, API calls, dynamic rendering, and filtering.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Application State Store
    const state = {
        activeTab: "dashboard",
        isDemoMode: true,
        currentProjectId: null,
        currentRequirement: "",
        generatedCode: "",
        docMarkdown: "",
        historyProjects: []
    };

    // Preset Software Engineering Blueprints
    const PRESETS = {
        student: {
            title: "Student Management System",
            req: "Create a Python student management system where an administrator can add, update, delete and search student records with data persistence and input validation.",
            lang: "Python",
            type: "CLI / Console",
            complexity: "Intermediate"
        },
        ecommerce: {
            title: "E-Commerce REST API",
            req: "Design a RESTful API in JavaScript/Node.js for an e-commerce platform allowing users to browse catalog items, manage cart state, checkout, and process order payments securely.",
            lang: "JavaScript",
            type: "REST API",
            complexity: "Advanced"
        },
        library: {
            title: "Library Management System",
            req: "Build a C++ library inventory management application for cataloging books, tracking active member loans, calculating late return fines, and generating inventory audit summaries.",
            lang: "C++",
            type: "CLI / Console",
            complexity: "Intermediate"
        }
    };

    // Initialize Subsystems
    initLucide();
    initSidebar();
    initAppStatus();
    initDashboardActions();
    initAnalyzerActions();
    initGeneratorActions();
    initReviewerActions();
    initExplainerActions();
    initDocsActions();
    initHistoryActions();

    // =========================================================================
    // 1. Icon & Layout Management
    // =========================================================================

    function initLucide() {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    function refreshIcons() {
        setTimeout(() => {
            if (window.lucide) {
                window.lucide.createIcons();
            }
        }, 10);
    }

    function initSidebar() {
        const sidebar = document.getElementById("app-sidebar");
        const toggleBtn = document.getElementById("btn-collapse-sidebar");
        const mobileBtn = document.getElementById("btn-mobile-menu");
        const backdrop = document.getElementById("sidebar-backdrop");

        // Restore collapsed state from localStorage
        const isCollapsed = localStorage.getItem("codemind_sidebar_collapsed") === "true";
        if (isCollapsed && window.innerWidth > 768) {
            sidebar.classList.add("collapsed");
            document.body.classList.add("sidebar-collapsed-layout");
        }

        if (toggleBtn) {
            toggleBtn.addEventListener("click", () => {
                sidebar.classList.toggle("collapsed");
                const nowCollapsed = sidebar.classList.contains("collapsed");
                document.body.classList.toggle("sidebar-collapsed-layout", nowCollapsed);
                localStorage.setItem("codemind_sidebar_collapsed", nowCollapsed);
                refreshIcons();
            });
        }

        if (mobileBtn && backdrop) {
            mobileBtn.addEventListener("click", () => {
                sidebar.classList.add("mobile-open");
                backdrop.classList.add("active");
            });

            backdrop.addEventListener("click", () => {
                sidebar.classList.remove("mobile-open");
                backdrop.classList.remove("active");
            });
        }

        // Navigation Menu Item Binding
        document.querySelectorAll(".nav-item").forEach(item => {
            item.addEventListener("click", () => {
                const targetTab = item.getAttribute("data-tab");
                if (targetTab) {
                    switchTab(targetTab);
                    if (window.innerWidth <= 768 && sidebar.classList.contains("mobile-open")) {
                        sidebar.classList.remove("mobile-open");
                        if (backdrop) backdrop.classList.remove("active");
                    }
                }
            });
        });

        // Global Nav Triggers
        document.addEventListener("click", (e) => {
            const trigger = e.target.closest(".nav-trigger");
            if (trigger) {
                const targetTab = trigger.getAttribute("data-tab");
                if (targetTab) switchTab(targetTab);
            }
        });
    }

    function switchTab(tabId) {
        state.activeTab = tabId;

        // Nav Menu items update
        document.querySelectorAll(".nav-item").forEach(el => {
            if (el.getAttribute("data-tab") === tabId) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });

        // View panels display toggle
        document.querySelectorAll(".tab-view").forEach(view => {
            view.classList.remove("active");
        });

        const activeView = document.getElementById(`view-${tabId}`);
        if (activeView) activeView.classList.add("active");

        // Header view titles
        const titles = {
            dashboard: { title: "Overview", desc: "Workspace analytics, active projects, and rapid engineering actions" },
            analyzer: { title: "Requirements Specification", desc: "Deconstruct natural language into structured requirements and detect ambiguities" },
            generator: { title: "Code Generator", desc: "Automated multi-language code synthesis with complexity analysis" },
            reviewer: { title: "Code Reviewer", desc: "Automated static analysis, security auditing, and quality scoring" },
            explainer: { title: "Code Explainer", desc: "Step-by-step logic tracing, variable tracking, and component analysis" },
            docs: { title: "Documentation Generator", desc: "Compile standardized IEEE Software Requirement Specifications (SRS)" },
            history: { title: "Project History", desc: "Saved software engineering sessions and historical analyses" }
        };

        if (titles[tabId]) {
            document.getElementById("view-title").innerText = titles[tabId].title;
            document.getElementById("view-desc").innerText = titles[tabId].desc;
        }

        if (tabId === "history") {
            loadHistoryTable();
        }

        refreshIcons();
    }

    // =========================================================================
    // 2. Application Status & Health Check
    // =========================================================================

    function initAppStatus() {
        const testBtn = document.getElementById("btn-test-api");
        if (testBtn) {
            testBtn.addEventListener("click", () => verifyApiConnection(true));
        }

        fetchAppStatus();
    }

    function fetchAppStatus() {
        fetch("/api/status")
            .then(res => res.json())
            .then(data => {
                state.isDemoMode = data.is_demo_mode;

                // Update Demo Banner
                const demoBanner = document.getElementById("demo-mode-banner");
                if (demoBanner) {
                    demoBanner.style.display = state.isDemoMode ? "flex" : "none";
                }

                // Header Status Pill
                const statusDot = document.getElementById("header-status-dot");
                const statusText = document.getElementById("api-status-text");
                const engineDot = document.getElementById("sidebar-engine-dot");
                const engineName = document.getElementById("sidebar-engine-name");
                const engineMode = document.getElementById("sidebar-engine-mode");

                const model = data.model_name || "Gemini 3.8 Flash";

                if (state.isDemoMode) {
                    if (statusDot) statusDot.className = "status-dot warning";
                    if (statusText) statusText.innerText = "Demo Mode (Offline)";
                    if (engineDot) engineDot.className = "status-indicator-dot warning";
                    if (engineName) engineName.innerText = "Demo Engine";
                    if (engineMode) engineMode.innerText = "Offline Mock Responses";
                } else {
                    if (statusDot) statusDot.className = "status-dot";
                    if (statusText) statusText.innerText = `${model} Active`;
                    if (engineDot) engineDot.className = "status-indicator-dot";
                    if (engineName) engineName.innerText = model;
                    if (engineMode) engineMode.innerText = "Live Neural Engine Connected";
                }

                // Update Dashboard Metrics
                if (data.stats) {
                    const elProjects = document.getElementById("stat-projects");
                    const elGenerations = document.getElementById("stat-generations");
                    const elReviews = document.getElementById("stat-reviews");
                    const elAnalyses = document.getElementById("stat-analyses");

                    if (elProjects) elProjects.innerText = data.stats.projects || 0;
                    if (elGenerations) elGenerations.innerText = data.stats.code_generations || 0;
                    if (elReviews) elReviews.innerText = data.stats.reviews || 0;
                    if (elAnalyses) elAnalyses.innerText = data.stats.analyses || 0;
                }

                // Render Recent Projects in Dashboard
                renderRecentProjects(data.recent_projects || []);
                refreshIcons();
            })
            .catch(err => {
                console.error("Status fetch error:", err);
                const statusText = document.getElementById("api-status-text");
                if (statusText) statusText.innerText = "Status Unavailable";
            });
    }

    function verifyApiConnection(isUserTriggered = false) {
        const testBtn = document.getElementById("btn-test-api");
        const statusText = document.getElementById("api-status-text");

        if (testBtn) {
            testBtn.disabled = true;
            testBtn.innerHTML = `<div class="spinner" style="width: 14px; height: 14px; border-width: 2px;"></div><span>Testing...</span>`;
        }

        fetch("/api/test-connection")
            .then(res => res.json())
            .then(result => {
                if (testBtn) {
                    testBtn.disabled = false;
                    testBtn.innerHTML = `<i data-lucide="refresh-cw" class="icon-sm"></i><span>Verify API</span>`;
                }

                if (result.success) {
                    showToast(result.message || "Connected to Gemini Engine successfully", "success");
                } else {
                    showToast(result.message || "Operating in Demo Mode", "info");
                }

                fetchAppStatus();
                refreshIcons();
            })
            .catch(err => {
                if (testBtn) {
                    testBtn.disabled = false;
                    testBtn.innerHTML = `<i data-lucide="refresh-cw" class="icon-sm"></i><span>Verify API</span>`;
                }
                showToast("Connection verification request failed", "error");
                console.error(err);
                refreshIcons();
            });
    }

    // =========================================================================
    // 3. Dashboard Actions & Hero Input
    // =========================================================================

    function initDashboardActions() {
        const heroInput = document.getElementById("hero-prompt-input");

        // Action: Analyze Requirements from Hero Input
        const btnAnalyze = document.getElementById("hero-btn-analyze");
        if (btnAnalyze) {
            btnAnalyze.addEventListener("click", () => {
                const text = heroInput ? heroInput.value.trim() : "";
                if (text) {
                    document.getElementById("analyzer-req-input").value = text;
                }
                switchTab("analyzer");
            });
        }

        // Action: Generate Code from Hero Input
        const btnGenerate = document.getElementById("hero-btn-generate");
        if (btnGenerate) {
            btnGenerate.addEventListener("click", () => {
                const text = heroInput ? heroInput.value.trim() : "";
                if (text) {
                    document.getElementById("gen-req-input").value = text;
                }
                switchTab("generator");
            });
        }

        // Action: Review Code from Hero Input
        const btnReview = document.getElementById("hero-btn-review");
        if (btnReview) {
            btnReview.addEventListener("click", () => {
                const text = heroInput ? heroInput.value.trim() : "";
                if (text) {
                    document.getElementById("review-code-input").value = text;
                }
                switchTab("reviewer");
            });
        }

        // Action: Explain Code from Hero Input
        const btnExplain = document.getElementById("hero-btn-explain");
        if (btnExplain) {
            btnExplain.addEventListener("click", () => {
                const text = heroInput ? heroInput.value.trim() : "";
                if (text) {
                    document.getElementById("explain-code-input").value = text;
                }
                switchTab("explainer");
            });
        }

        // Preset Blueprints Loading
        document.querySelectorAll(".load-preset").forEach(btn => {
            btn.addEventListener("click", () => {
                const key = btn.getAttribute("data-preset");
                const preset = PRESETS[key];
                if (preset) {
                    document.getElementById("analyzer-req-input").value = preset.req;
                    document.getElementById("analyzer-language").value = preset.lang;
                    document.getElementById("analyzer-project-type").value = preset.type;
                    document.getElementById("analyzer-complexity").value = preset.complexity;
                    switchTab("analyzer");
                    showToast(`Loaded blueprint: ${preset.title}`, "info");
                }
            });
        });
    }

    function renderRecentProjects(projects) {
        const container = document.getElementById("recent-projects-list");
        if (!container) return;

        if (!projects || projects.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i data-lucide="folder-open" class="empty-state-icon"></i>
                    <span class="empty-state-title">No projects recorded yet</span>
                    <p class="empty-state-desc">Describe a requirement above or select a blueprint preset to run your first engineering analysis.</p>
                </div>
            `;
            refreshIcons();
            return;
        }

        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Project Title</th>
                        <th>Type</th>
                        <th>Language</th>
                        <th>Status</th>
                        <th style="text-align: right;">Action</th>
                    </tr>
                </thead>
                <tbody>
        `;

        projects.forEach(p => {
            html += `
                <tr>
                    <td class="project-name">${escapeHtml(p.name)}</td>
                    <td>${escapeHtml(p.type)}</td>
                    <td><span class="badge badge-info">${escapeHtml(p.language)}</span></td>
                    <td><span class="badge badge-success">${escapeHtml(p.status || 'Analyzed')}</span></td>
                    <td style="text-align: right;">
                        <button class="btn btn-outline btn-compact open-recent-btn" 
                            data-req="${encodeURIComponent(p.requirement || '')}" 
                            data-lang="${escapeHtml(p.language)}">
                            <span>Open</span>
                            <i data-lucide="arrow-up-right" class="icon-sm"></i>
                        </button>
                    </td>
                </tr>
            `;
        });

        html += `</tbody></table>`;
        container.innerHTML = html;

        container.querySelectorAll(".open-recent-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const reqText = decodeURIComponent(btn.getAttribute("data-req"));
                const lang = btn.getAttribute("data-lang");
                document.getElementById("analyzer-req-input").value = reqText;
                if (lang) document.getElementById("analyzer-language").value = lang;
                switchTab("analyzer");
            });
        });

        refreshIcons();
    }

    // =========================================================================
    // 4. Requirement Analyzer Subsystem
    // =========================================================================

    function initAnalyzerActions() {
        const loadDemoBtn = document.getElementById("btn-load-demo-req");
        if (loadDemoBtn) {
            loadDemoBtn.addEventListener("click", () => {
                const preset = PRESETS.student;
                document.getElementById("analyzer-req-input").value = preset.req;
                document.getElementById("analyzer-language").value = preset.lang;
                document.getElementById("analyzer-project-type").value = preset.type;
                document.getElementById("analyzer-complexity").value = preset.complexity;
                showToast("Sample student management requirement loaded", "info");
            });
        }

        const runBtn = document.getElementById("btn-run-analyzer");
        if (runBtn) {
            runBtn.addEventListener("click", () => {
                const requirement = document.getElementById("analyzer-req-input").value.trim();
                if (!requirement) {
                    showToast("Please enter a requirement specification to analyze", "error");
                    return;
                }

                const project_type = document.getElementById("analyzer-project-type").value;
                const language = document.getElementById("analyzer-language").value;
                const complexity = document.getElementById("analyzer-complexity").value;

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
                        renderAnalysisOutput(data.analysis);
                        fetchAppStatus();
                        showToast("Requirement specification analyzed successfully", "success");
                    } else {
                        showToast(data.error || "Analysis failed", "error");
                    }
                })
                .catch(err => {
                    document.getElementById("analyzer-loading").style.display = "none";
                    showToast("Server error during requirement analysis", "error");
                    console.error(err);
                });
            });
        }

        // Proceed to Code Generation Action
        const proceedBtn = document.getElementById("btn-proceed-to-code");
        if (proceedBtn) {
            proceedBtn.addEventListener("click", () => {
                document.getElementById("gen-req-input").value = state.currentRequirement;
                document.getElementById("gen-language").value = document.getElementById("analyzer-language").value;
                switchTab("generator");
            });
        }
    }

    function renderAnalysisOutput(analysis) {
        const outputDiv = document.getElementById("analyzer-output");
        outputDiv.style.display = "block";

        // Ambiguity Alert Box
        const warnBox = document.getElementById("ambiguity-warning-box");
        if (analysis.is_ambiguous || (analysis.ambiguities && analysis.ambiguities.length > 0)) {
            warnBox.innerHTML = `
                <div class="alert-banner warning ambiguity-panel">
                    <div class="alert-content" style="align-items: flex-start;">
                        <i data-lucide="alert-triangle" class="alert-icon" style="margin-top: 2px;"></i>
                        <div>
                            <strong>Ambiguity Detected:</strong> Specific details in this requirement are open to interpretation:
                            <ul style="margin: 0.35rem 0 0 1.25rem; font-size: 0.8rem; line-height: 1.5;">
                                ${(analysis.ambiguities || []).map(a => `<li>${escapeHtml(a)}</li>`).join("")}
                                ${(analysis.missing_information || []).map(m => `<li>Missing parameter: ${escapeHtml(m)}</li>`).join("")}
                            </ul>
                        </div>
                    </div>
                    <span class="badge badge-warning">ATTENTION</span>
                </div>
            `;
        } else {
            warnBox.innerHTML = "";
        }

        // Problem Statement
        document.getElementById("res-problem-statement").innerText = analysis.problem_statement || "No problem statement specified.";

        // Functional & Non-Functional Requirements
        document.getElementById("res-functional-reqs").innerHTML = 
            (analysis.functional_requirements || []).map(item => `<li>${escapeHtml(item)}</li>`).join("");

        document.getElementById("res-nonfunctional-reqs").innerHTML = 
            (analysis.non_functional_requirements || []).map(item => `<li>${escapeHtml(item)}</li>`).join("");

        // Actors, Inputs, Outputs as Clean Tags
        document.getElementById("res-actors").innerHTML = 
            (analysis.actors || []).map(act => `<span class="entity-pill">${escapeHtml(act)}</span>`).join("");

        document.getElementById("res-inputs").innerHTML = 
            (analysis.inputs || []).map(inp => `<span class="entity-pill">${escapeHtml(inp)}</span>`).join("");

        document.getElementById("res-outputs").innerHTML = 
            (analysis.outputs || []).map(out => `<span class="entity-pill">${escapeHtml(out)}</span>`).join("");

        // Constraints & Suggestions
        document.getElementById("res-constraints").innerHTML = 
            (analysis.constraints || []).map(c => `<li>${escapeHtml(c)}</li>`).join("");

        document.getElementById("res-suggestions").innerHTML = 
            (analysis.suggestions || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");

        refreshIcons();
    }

    // =========================================================================
    // 5. Code Generator Subsystem
    // =========================================================================

    function initGeneratorActions() {
        const runBtn = document.getElementById("btn-run-generator");
        if (runBtn) {
            runBtn.addEventListener("click", () => {
                const requirement = document.getElementById("gen-req-input").value.trim();
                if (!requirement) {
                    showToast("Please specify a software requirement for code synthesis", "error");
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
                        showToast("Source code generated successfully", "success");
                    } else {
                        showToast(data.error || "Code generation failed", "error");
                    }
                })
                .catch(err => {
                    document.getElementById("generator-loading").style.display = "none";
                    showToast("Server error during code generation", "error");
                    console.error(err);
                });
            });
        }

        // Copy Code
        const copyBtn = document.getElementById("btn-copy-code");
        if (copyBtn) {
            copyBtn.addEventListener("click", () => {
                if (!state.generatedCode) return;
                navigator.clipboard.writeText(state.generatedCode);
                showToast("Source code copied to clipboard", "success");
            });
        }

        // Download Code
        const dlBtn = document.getElementById("btn-download-code");
        if (dlBtn) {
            dlBtn.addEventListener("click", () => {
                if (!state.generatedCode) return;
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
                showToast(`Downloaded solution file (.${ext})`, "info");
            });
        }

        // Cross-feature shortcuts
        const explainShortcut = document.getElementById("btn-explain-generated");
        if (explainShortcut) {
            explainShortcut.addEventListener("click", () => {
                document.getElementById("explain-code-input").value = state.generatedCode;
                document.getElementById("explain-language").value = document.getElementById("gen-language").value;
                switchTab("explainer");
            });
        }

        const reviewShortcut = document.getElementById("btn-review-generated");
        if (reviewShortcut) {
            reviewShortcut.addEventListener("click", () => {
                document.getElementById("review-code-input").value = state.generatedCode;
                document.getElementById("review-language").value = document.getElementById("gen-language").value;
                switchTab("reviewer");
            });
        }
    }

    function renderGeneratedCode(data, language) {
        document.getElementById("generator-output").style.display = "block";
        document.getElementById("code-lang-label").innerText = language;
        document.getElementById("generated-code-box").innerText = data.code || "// Code synthesis returned empty.";
        document.getElementById("gen-algorithm-text").innerText = data.algorithm || "Standard Modular Architecture";

        document.getElementById("gen-time-complexity").innerText = data.time_complexity || 'O(N)';
        document.getElementById("gen-space-complexity").innerText = data.space_complexity || 'O(1)';
        refreshIcons();
    }

    // =========================================================================
    // 6. Code Reviewer Subsystem
    // =========================================================================

    function initReviewerActions() {
        const runBtn = document.getElementById("btn-run-reviewer");
        if (runBtn) {
            runBtn.addEventListener("click", () => {
                const code = document.getElementById("review-code-input").value.trim();
                if (!code) {
                    showToast("Please provide source code to audit", "error");
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
                        showToast("Static code audit completed", "success");
                    } else {
                        showToast(data.error || "Code review failed", "error");
                    }
                })
                .catch(err => {
                    document.getElementById("reviewer-loading").style.display = "none";
                    showToast("Server error during code review", "error");
                    console.error(err);
                });
            });
        }

        const copyImproved = document.getElementById("btn-copy-improved");
        if (copyImproved) {
            copyImproved.addEventListener("click", () => {
                const improved = document.getElementById("improved-code-box").innerText;
                if (!improved) return;
                navigator.clipboard.writeText(improved);
                showToast("Refactored code copied to clipboard", "success");
            });
        }
    }

    function renderReviewOutput(data) {
        document.getElementById("reviewer-output").style.display = "block";

        // Score Badge
        const score = data.score !== undefined ? data.score : 85;
        document.getElementById("review-score-badge").innerText = score;

        // Issues List
        const issuesContainer = document.getElementById("review-issues-list");
        if (!data.issues || data.issues.length === 0) {
            issuesContainer.innerHTML = `
                <div class="spec-box" style="display: flex; align-items: center; gap: 0.5rem; color: var(--success);">
                    <i data-lucide="check-circle" class="icon-sm"></i>
                    <span>Zero critical issues detected! Code adheres to robust quality standards.</span>
                </div>
            `;
        } else {
            issuesContainer.innerHTML = data.issues.map(issue => {
                const sev = (issue.severity || 'medium').toLowerCase();
                const sevBadgeClass = `badge-${sev}`;
                return `
                    <div class="issue-card">
                        <div class="issue-header">
                            <span class="issue-title">${escapeHtml(issue.title)}</span>
                            <span class="badge ${sevBadgeClass}">${escapeHtml(issue.severity || 'Medium')}</span>
                        </div>
                        <p class="issue-desc">${escapeHtml(issue.description)}</p>
                        <span class="issue-category">Category: ${escapeHtml(issue.category || 'General')}</span>
                    </div>
                `;
            }).join("");
        }

        // Suggestions
        document.getElementById("review-suggestions-list").innerHTML = 
            (data.suggestions || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");

        // Improved Code
        document.getElementById("improved-code-box").innerText = data.improved_code || "// No refactored code necessary.";
        refreshIcons();
    }

    // =========================================================================
    // 7. Code Explainer Subsystem
    // =========================================================================

    function initExplainerActions() {
        const runBtn = document.getElementById("btn-run-explainer");
        if (runBtn) {
            runBtn.addEventListener("click", () => {
                const code = document.getElementById("explain-code-input").value.trim();
                if (!code) {
                    showToast("Please provide source code for explanation", "error");
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
                        showToast("Code explanation generated", "success");
                    } else {
                        showToast(data.error || "Explanation generation failed", "error");
                    }
                })
                .catch(err => {
                    document.getElementById("explainer-loading").style.display = "none";
                    showToast("Server error during code explanation", "error");
                    console.error(err);
                });
            });
        }
    }

    function renderExplainerOutput(data) {
        document.getElementById("explainer-output").style.display = "block";
        document.getElementById("exp-summary").innerText = data.summary || "Summary breakdown not available.";

        document.getElementById("exp-steps-list").innerHTML = 
            (data.step_by_step || []).map(step => `<li>${escapeHtml(step)}</li>`).join("");

        document.getElementById("exp-components-list").innerHTML = 
            (data.key_components || []).map(c => `<li><strong>${escapeHtml(c.name)}</strong>: ${escapeHtml(c.description)}</li>`).join("");

        document.getElementById("exp-variables-list").innerHTML = 
            (data.important_variables || []).map(v => `<li><code>${escapeHtml(v.name)}</code>: ${escapeHtml(v.description)}</li>`).join("");

        refreshIcons();
    }

    // =========================================================================
    // 8. Documentation (SRS) Subsystem
    // =========================================================================

    function initDocsActions() {
        const runBtn = document.getElementById("btn-run-docs");
        if (runBtn) {
            runBtn.addEventListener("click", () => {
                const requirement = document.getElementById("docs-req-input").value.trim() || state.currentRequirement;
                if (!requirement) {
                    showToast("Please specify a software requirement to compile documentation", "error");
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
                        showToast("Software Requirement Specification compiled", "success");
                    } else {
                        showToast(data.error || "Documentation generation failed", "error");
                    }
                })
                .catch(err => {
                    document.getElementById("docs-loading").style.display = "none";
                    showToast("Server error compiling documentation", "error");
                    console.error(err);
                });
            });
        }

        // Copy Markdown
        const copyDoc = document.getElementById("btn-copy-doc");
        if (copyDoc) {
            copyDoc.addEventListener("click", () => {
                if (!state.docMarkdown) return;
                navigator.clipboard.writeText(state.docMarkdown);
                showToast("SRS Markdown copied to clipboard", "success");
            });
        }

        // Download Markdown
        const dlDoc = document.getElementById("btn-download-doc-md");
        if (dlDoc) {
            dlDoc.addEventListener("click", () => {
                if (!state.docMarkdown) return;
                const blob = new Blob([state.docMarkdown], { type: "text/markdown" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "CodeMind_SRS_Documentation.md";
                a.click();
                URL.revokeObjectURL(url);
                showToast("Downloaded documentation (.md)", "info");
            });
        }

        // Download PDF
        const pdfDoc = document.getElementById("btn-download-doc-pdf");
        if (pdfDoc) {
            pdfDoc.addEventListener("click", () => {
                if (!state.docMarkdown) return;
                showToast("Generating PDF document...", "info");

                fetch("/api/export-pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        markdown: state.docMarkdown,
                        title: "CodeMind_SRS_Documentation"
                    })
                })
                .then(response => {
                    if (!response.ok) throw new Error("PDF generation failed");
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "CodeMind_SRS_Documentation.pdf";
                    a.click();
                    URL.revokeObjectURL(url);
                    showToast("Downloaded PDF documentation", "success");
                })
                .catch(err => {
                    showToast("Failed to compile PDF export", "error");
                    console.error(err);
                });
            });
        }
    }

    function renderMarkdownDocs(markdown) {
        document.getElementById("docs-output").style.display = "block";
        const container = document.getElementById("markdown-doc-body");

        // Clean parser for headings, bullet points, and code blocks
        let html = escapeHtml(markdown)
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            .replace(/\n\n/gim, '<br>');

        container.innerHTML = html;
        refreshIcons();
    }

    // =========================================================================
    // 9. Project History Subsystem with Search & Filter
    // =========================================================================

    function initHistoryActions() {
        const searchInput = document.getElementById("history-search-input");
        const langFilter = document.getElementById("history-lang-filter");

        if (searchInput) {
            searchInput.addEventListener("input", () => filterAndRenderHistory());
        }

        if (langFilter) {
            langFilter.addEventListener("change", () => filterAndRenderHistory());
        }
    }

    function loadHistoryTable() {
        const container = document.getElementById("history-projects-table");
        if (!container) return;

        container.innerHTML = `<p class="text-muted-state" style="padding: 1.5rem; text-align: center;">Loading saved sessions from SQLite database...</p>`;

        fetch("/api/projects")
            .then(res => res.json())
            .then(data => {
                state.historyProjects = data.projects || [];
                filterAndRenderHistory();
            })
            .catch(err => {
                console.error("Error loading project history:", err);
                container.innerHTML = `<p class="text-muted-state" style="padding: 1.5rem; text-align: center; color: var(--danger);">Failed to retrieve project history.</p>`;
            });
    }

    function filterAndRenderHistory() {
        const container = document.getElementById("history-projects-table");
        if (!container) return;

        const searchVal = (document.getElementById("history-search-input")?.value || "").toLowerCase().trim();
        const langVal = document.getElementById("history-lang-filter")?.value || "ALL";

        let filtered = state.historyProjects || [];

        if (langVal !== "ALL") {
            filtered = filtered.filter(p => (p.language || "").toLowerCase() === langVal.toLowerCase());
        }

        if (searchVal) {
            filtered = filtered.filter(p => 
                (p.name || "").toLowerCase().includes(searchVal) ||
                (p.requirement || "").toLowerCase().includes(searchVal) ||
                (p.type || "").toLowerCase().includes(searchVal)
            );
        }

        if (filtered.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i data-lucide="archive-x" class="empty-state-icon"></i>
                    <span class="empty-state-title">No matching records found</span>
                    <p class="empty-state-desc">Try refining your search keyword or clearing the language filter.</p>
                </div>
            `;
            refreshIcons();
            return;
        }

        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">ID</th>
                        <th>Project Title</th>
                        <th>Language</th>
                        <th>Architecture</th>
                        <th>Timestamp</th>
                        <th style="text-align: right;">Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;

        filtered.forEach(p => {
            html += `
                <tr>
                    <td style="color: var(--text-tertiary); font-family: var(--font-mono); font-size: 0.75rem;">#${p.id}</td>
                    <td class="project-name">${escapeHtml(p.name)}</td>
                    <td><span class="badge badge-info">${escapeHtml(p.language)}</span></td>
                    <td>${escapeHtml(p.type)}</td>
                    <td style="color: var(--text-tertiary); font-size: 0.75rem;">${escapeHtml(p.created_at || '—')}</td>
                    <td style="text-align: right;">
                        <div class="btn-group" style="justify-content: flex-end;">
                            <button class="btn btn-outline btn-compact hist-open-btn" 
                                data-id="${p.id}" 
                                data-req="${encodeURIComponent(p.requirement || '')}" 
                                data-lang="${escapeHtml(p.language)}">
                                <i data-lucide="folder-open" class="icon-sm"></i>
                                <span>Open</span>
                            </button>
                            <button class="btn btn-outline btn-compact hist-dup-btn" data-id="${p.id}">
                                <i data-lucide="copy-plus" class="icon-sm"></i>
                                <span>Duplicate</span>
                            </button>
                            <button class="btn btn-outline btn-compact hist-del-btn" data-id="${p.id}" style="color: var(--danger); border-color: var(--danger-border);">
                                <i data-lucide="trash-2" class="icon-sm"></i>
                                <span>Delete</span>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });

        html += `</tbody></table>`;
        container.innerHTML = html;

        // Open handler
        container.querySelectorAll(".hist-open-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const reqText = decodeURIComponent(btn.getAttribute("data-req"));
                const lang = btn.getAttribute("data-lang");
                document.getElementById("analyzer-req-input").value = reqText;
                if (lang) document.getElementById("analyzer-language").value = lang;
                switchTab("analyzer");
            });
        });

        // Duplicate handler
        container.querySelectorAll(".hist-dup-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.getAttribute("data-id");
                fetch(`/api/projects/${id}/duplicate`, { method: "POST" })
                    .then(res => res.json())
                    .then(() => {
                        showToast(`Project #${id} duplicated`, "success");
                        loadHistoryTable();
                        fetchAppStatus();
                    })
                    .catch(() => showToast("Failed to duplicate project", "error"));
            });
        });

        // Delete handler
        container.querySelectorAll(".hist-del-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.getAttribute("data-id");
                if (confirm(`Permanently delete project #${id} from the database?`)) {
                    fetch(`/api/projects/${id}/delete`, { method: "DELETE" })
                        .then(res => res.json())
                        .then(() => {
                            showToast(`Project #${id} deleted`, "info");
                            loadHistoryTable();
                            fetchAppStatus();
                        })
                        .catch(() => showToast("Failed to delete project", "error"));
                }
            });
        });

        refreshIcons();
    }

    // =========================================================================
    // 10. Utilities & Toast System
    // =========================================================================

    function showToast(message, type = "info") {
        const container = document.getElementById("toast-container");
        if (!container) return;

        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;

        const iconName = type === "success" ? "check-circle" : (type === "error" ? "alert-circle" : "info");
        toast.innerHTML = `<i data-lucide="${iconName}" class="icon-sm"></i><span>${escapeHtml(message)}</span>`;

        container.appendChild(toast);
        refreshIcons();

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(8px)";
            setTimeout(() => toast.remove(), 250);
        }, 3200);
    }

    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
