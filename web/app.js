/**
 * Apply on Job — Talent Acquisition AI Engine & Funnel Intelligence
 * Interactive Client Controller & Visualization Suite (app.js)
 */

let dashboardData = {
    kpis: {
        total_applications: 50000,
        passed_triage: 12450,
        interviews: 4280,
        offers: 1240,
        hires: 890
    },
    funnel: [
        { stage: "1. Total Applications", count: 50000, conversion: 100.0, drop_off: 0.0 },
        { stage: "2. Qualified by Triage", count: 12450, conversion: 24.9, drop_off: 75.1 },
        { stage: "3. Technical Interviews", count: 4280, conversion: 34.4, drop_off: 65.6 },
        { stage: "4. Offers Extended", count: 1240, conversion: 29.0, drop_off: 71.0 },
        { stage: "5. Placements / Hires", count: 890, conversion: 71.8, drop_off: 28.2 }
    ],
    channels: [
        { name: "Apply on Job Direct", hires: 420 },
        { name: "LinkedIn Job Slots", hires: 230 },
        { name: "Indeed Featured", hires: 110 },
        { name: "Tech Community Referral", hires: 95 },
        { name: "GitHub Inbound Sourcing", hires: 35 }
    ],
    candidates: [
        {
            id: "CAND-004812",
            token: "TOKEN-ANON-89421",
            role: "Senior Data Scientist",
            exp: "6 Years",
            match_score: 91.5,
            category: "DIRECT_APPLICABLE",
            summary: "Candidate exhibits a 91.5% composite fit with core competencies in Python, SQL, and DuckDB. Experience exceeds target with zero adversarial security flags.",
            question: "How would you architect an in-memory OLAP pipeline using DuckDB to process 50k events without saturating L3 cache?",
            feedback: "Strong algorithmic match; recommend expanding practical exposure to distributed Kafka event streaming.",
            skills: [95, 90, 92, 85, 78, 88],
            req_skills: [90, 85, 80, 80, 75, 85]
        },
        {
            id: "CAND-001205",
            token: "TOKEN-ANON-34902",
            role: "Lead AI / ML Solutions Architect",
            exp: "9 Years",
            match_score: 86.0,
            category: "DIRECT_APPLICABLE",
            summary: "Exceptional architecture background with PyTorch, LLMs, and Kubernetes orchestration. Proven enterprise deployment track record.",
            question: "Describe your strategy for deploying quantized ONNX models in edge gateways with <20ms p99 latency.",
            feedback: "Strong architectural mastery; recommended for direct hiring committee interview.",
            skills: [98, 92, 88, 95, 90, 85],
            req_skills: [95, 90, 85, 90, 85, 80]
        },
        {
            id: "CAND-008931",
            token: "TOKEN-ANON-12940",
            role: "Data Analyst / Analytics Engineer",
            exp: "14 Years",
            match_score: 72.4,
            category: "HUMAN_REVIEW_FLAGGED",
            summary: "Overqualification anomaly: 14 years experience applying for Mid-Level role; potential salary expectation mismatch (>35% above budget).",
            question: "What motivations lead you to target this individual contributor role given your extensive senior background?",
            feedback: "Profile exceeds seniority baseline; recruiter should verify salary alignment and scope expectations.",
            skills: [85, 95, 70, 60, 65, 80],
            req_skills: [70, 85, 80, 75, 70, 75]
        },
        {
            id: "CAND-003310",
            token: "TOKEN-ANON-59123",
            role: "BI & Decision Intelligence Specialist",
            exp: "4 Years",
            match_score: 64.8,
            category: "HUMAN_REVIEW_FLAGGED",
            summary: "Borderline fit: High Power BI and SQL skills, but missing required experience in Snowflake and dbt semantic modeling.",
            question: "How have you modeled dimensional star schemas in VertiPaq when source data lacked pre-aggregated marts?",
            feedback: "Solid BI foundation; building hands-on dbt semantic projects will solidify senior eligibility.",
            skills: [65, 85, 90, 50, 55, 70],
            req_skills: [75, 80, 85, 80, 75, 80]
        },
        {
            id: "CAND-009104",
            token: "TOKEN-ANON-77821",
            role: "Junior Data Engineer",
            exp: "0 Years",
            match_score: 41.2,
            category: "AUTO_REJECT",
            summary: "Low fit: Missing required foundational experience in Python ETL and Docker containerization.",
            question: "N/A - Candidate auto-disqualified prior to recruiter screening.",
            feedback: "Thank you for applying. We encourage completing foundational projects in Python and Git to qualify for future cycles.",
            skills: [40, 45, 30, 20, 25, 40],
            req_skills: [60, 65, 50, 50, 45, 60]
        }
    ],
    fairness: [
        { group: "Group Alpha", rate: 26.4, dir: 1.00, status: "Reference" },
        { group: "Group Beta", rate: 24.8, dir: 0.939, status: "Compliant" },
        { group: "Group Gamma", rate: 23.5, dir: 0.890, status: "Compliant" },
        { group: "Group Delta", rate: 23.3, dir: 0.884, status: "Compliant" }
    ]
};

let currentFilter = "ALL";
let chartInstances = {};

// DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("data/dashboard_data.json");
        if (response.ok) {
            const dynamic = await response.json();
            dashboardData.kpis = dynamic.kpis || dashboardData.kpis;
            dashboardData.funnel = dynamic.funnel || dashboardData.funnel;
            dashboardData.channels = dynamic.channels || dashboardData.channels;
        }
    } catch (e) {
        console.log("Telemetry loaded from embedded core.");
    }

    renderKPIs();
    initFunnelChart();
    initChannelChart();
    initRadarChart();
    initFairnessChart();
    renderTriageTable();
});

// Tab Switcher
function switchTab(tabId) {
    document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
    document.querySelectorAll(".tab-button").forEach(el => el.classList.remove("active"));

    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.remove("hidden");

    const activeBtn = document.getElementById(`btn-${tabId}`);
    if (activeBtn) activeBtn.classList.add("active");

    // Trigger Chart Resize
    Object.values(chartInstances).forEach(chart => chart.resize());
}

function renderKPIs() {
    document.getElementById("kpi-total-apps").textContent = Number(dashboardData.kpis.total_applications).toLocaleString();
    document.getElementById("kpi-passed-triage").textContent = Number(dashboardData.kpis.passed_triage).toLocaleString();
    document.getElementById("kpi-interviews").textContent = Number(dashboardData.kpis.interviews).toLocaleString();
    document.getElementById("kpi-offers").textContent = Number(dashboardData.kpis.offers).toLocaleString();
    document.getElementById("kpi-hires").textContent = Number(dashboardData.kpis.hires).toLocaleString();
}

function initFunnelChart() {
    const ctx = document.getElementById("funnelChart").getContext("2d");
    const labels = dashboardData.funnel.map(f => f.stage);
    const dataCounts = dashboardData.funnel.map(f => f.count);

    chartInstances.funnel = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Candidates in Stage",
                data: dataCounts,
                backgroundColor: [
                    "rgba(56, 189, 248, 0.8)",
                    "rgba(52, 211, 153, 0.8)",
                    "rgba(129, 140, 248, 0.8)",
                    "rgba(251, 191, 36, 0.8)",
                    "rgba(14, 165, 233, 0.8)"
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "#0b0f19",
                    titleColor: "#f8fafc",
                    bodyColor: "#94a3b8",
                    borderColor: "#334155",
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return ` Volume: ${context.parsed.x.toLocaleString()} candidates`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: "rgba(51, 65, 85, 0.25)" },
                    ticks: { color: "#94a3b8", font: { family: 'Inter', size: 11 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: "#f8fafc", font: { family: 'Inter', size: 11, weight: '500' } }
                }
            }
        }
    });
}

function initChannelChart() {
    const ctx = document.getElementById("channelChart").getContext("2d");
    const labels = dashboardData.channels.map(c => c.name);
    const dataHires = dashboardData.channels.map(c => c.hires);

    chartInstances.channel = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: dataHires,
                backgroundColor: [
                    "#0284c7",
                    "#38bdf8",
                    "#818cf8",
                    "#34d399",
                    "#fbbf24"
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#94a3b8", font: { family: 'Inter', size: 10 }, boxWidth: 12, padding: 12 }
                }
            },
            cutout: "72%"
        }
    });
}

function initRadarChart() {
    const ctx = document.getElementById("radarChart").getContext("2d");
    chartInstances.radar = new Chart(ctx, {
        type: "radar",
        data: {
            labels: ["Python/Math", "SQL/OLAP", "Architecture", "ML Modeling", "Cloud Ops", "Product Fit"],
            datasets: [
                {
                    label: "Candidate Profile",
                    data: dashboardData.candidates[0].skills,
                    borderColor: "#38bdf8",
                    backgroundColor: "rgba(56, 189, 248, 0.25)",
                    borderWidth: 2,
                    pointBackgroundColor: "#38bdf8"
                },
                {
                    label: "Role Benchmark",
                    data: dashboardData.candidates[0].req_skills,
                    borderColor: "#818cf8",
                    backgroundColor: "rgba(129, 140, 248, 0.1)",
                    borderWidth: 1.5,
                    borderDash: [4, 4],
                    pointBackgroundColor: "#818cf8"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: "rgba(51, 65, 85, 0.4)" },
                    grid: { color: "rgba(51, 65, 85, 0.3)" },
                    pointLabels: { color: "#94a3b8", font: { size: 10, family: 'Inter' } },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { size: 10 }, boxWidth: 10 }
                }
            }
        }
    });
}

function initFairnessChart() {
    const ctx = document.getElementById("fairnessChart").getContext("2d");
    chartInstances.fairness = new Chart(ctx, {
        type: "bar",
        data: {
            labels: dashboardData.fairness.map(f => f.group),
            datasets: [
                {
                    label: "Selection Rate %",
                    data: dashboardData.fairness.map(f => f.rate),
                    backgroundColor: "rgba(52, 211, 153, 0.75)",
                    borderRadius: 6,
                    borderWidth: 0
                },
                {
                    label: "Disparate Impact Ratio (DIR)",
                    data: dashboardData.fairness.map(f => f.dir * 25), // scaled for visualization
                    backgroundColor: "rgba(56, 189, 248, 0.5)",
                    borderRadius: 6,
                    borderWidth: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { size: 10 }, boxWidth: 12 }
                }
            },
            scales: {
                x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
                y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(51, 65, 85, 0.25)" } }
            }
        }
    });
}

function renderTriageTable() {
    const tbody = document.getElementById("triage-table-body");
    tbody.innerHTML = "";

    const filtered = dashboardData.candidates.filter(c => {
        if (currentFilter === "ALL") return true;
        return c.category === currentFilter;
    });

    filtered.forEach(c => {
        const tr = document.createElement("tr");
        tr.className = "hover:bg-slate-900/60 transition-colors border-b border-slate-800/40";

        let badgeClass = "badge-reject";
        let badgeIcon = "fa-circle-xmark";
        if (c.category === "DIRECT_APPLICABLE") {
            badgeClass = "badge-direct";
            badgeIcon = "fa-circle-check";
        } else if (c.category === "HUMAN_REVIEW_FLAGGED") {
            badgeClass = "badge-review";
            badgeIcon = "fa-triangle-exclamation";
        }

        tr.innerHTML = `
            <td class="py-3.5 px-4 font-mono font-medium text-slate-200">${c.id}</td>
            <td class="py-3.5 px-4 text-slate-100 font-semibold">${c.role}</td>
            <td class="py-3.5 px-4 text-slate-400">${c.exp}</td>
            <td class="py-3.5 px-4 text-center">
                <span class="inline-flex items-center font-bold font-mono text-sky-400 bg-sky-500/10 border border-sky-500/20 px-2 py-0.5 rounded">
                    ${c.match_score}%
                </span>
            </td>
            <td class="py-3.5 px-4">
                <span class="${badgeClass}">
                    <i class="fa-solid ${badgeIcon} mr-1.5 text-[10px]"></i>
                    ${c.category.replace(/_/g, ' ')}
                </span>
            </td>
            <td class="py-3.5 px-4 text-right">
                <button onclick="inspectCandidate('${c.id}')" class="inline-flex items-center space-x-1.5 text-xs font-semibold text-sky-400 hover:text-sky-300 bg-slate-800/80 hover:bg-slate-800 px-3 py-1 rounded-lg border border-slate-700 transition-all">
                    <i class="fa-solid fa-eye text-[10px]"></i>
                    <span>Inspect</span>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterTriage(category) {
    currentFilter = category;
    document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
    
    if (category === "ALL") document.getElementById("btn-all").classList.add("active");
    if (category === "DIRECT_APPLICABLE") document.getElementById("btn-direct").classList.add("active");
    if (category === "HUMAN_REVIEW_FLAGGED") document.getElementById("btn-review").classList.add("active");
    if (category === "AUTO_REJECT") document.getElementById("btn-reject").classList.add("active");

    renderTriageTable();
}

function inspectCandidate(candidateId) {
    const cand = dashboardData.candidates.find(c => c.id === candidateId);
    if (!cand) return;

    // Switch to Copilot Tab
    switchTab("tab-copilot");

    document.getElementById("briefing-cand-token").textContent = `${cand.token} • (${cand.role})`;
    document.getElementById("briefing-summary").textContent = cand.summary;
    document.getElementById("briefing-question").textContent = `"${cand.question}"`;
    document.getElementById("briefing-feedback").textContent = cand.feedback;

    // Update Radar Chart Dataset
    if (chartInstances.radar) {
        chartInstances.radar.data.datasets[0].data = cand.skills;
        chartInstances.radar.data.datasets[1].data = cand.req_skills;
        chartInstances.radar.update();
    }
}
