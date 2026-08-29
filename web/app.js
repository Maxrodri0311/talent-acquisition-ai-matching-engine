/**
 * Apply on Job — Talent Acquisition AI Engine
 * Client-Side Interactive Dashboard Controller (app.js)
 */

// Sample Data Payload (Will be supplemented/overwritten by pipeline's dashboard_data.json)
let dashboardData = {
    kpis: {
        total_applications: 50000,
        passed_triage: 12450,
        interviews: 4280,
        offers: 1240,
        hires: 890
    },
    funnel: [
        { stage: "1. Total Applications", count: 50000, conversion: 100.0 },
        { stage: "2. Passed Initial Triage", count: 12450, conversion: 24.9 },
        { stage: "3. Technical Interviews", count: 4280, conversion: 34.4 },
        { stage: "4. Offers Extended", count: 1240, conversion: 29.0 },
        { stage: "5. Placements / Hires", count: 890, conversion: 71.8 }
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
            summary: "Candidate exhibits a 91.5% composite fit with core competencies in Python, SQL, and DuckDB. Experience exceeds the 5-year target.",
            question: "How would you architect an in-memory OLAP pipeline using DuckDB to process 50k events without saturating L3 cache?",
            feedback: "Strong algorithmic match; recommend expanding practical exposure to distributed Kafka event streaming."
        },
        {
            id: "CAND-001205",
            token: "TOKEN-ANON-34902",
            role: "Lead AI / ML Solutions Architect",
            exp: "9 Years",
            match_score: 86.0,
            category: "DIRECT_APPLICABLE",
            summary: "Exceptional architecture background with PyTorch, LLMs, and Kubernetes orchestration.",
            question: "Describe your strategy for deploying quantized ONNX models in edge gateways with <20ms p99 latency.",
            feedback: "Strong architectural mastery; recommended for direct hiring committee interview."
        },
        {
            id: "CAND-008931",
            token: "TOKEN-ANON-12940",
            role: "Data Analyst / Analytics Engineer",
            exp: "14 Years",
            match_score: 72.4,
            category: "HUMAN_REVIEW_FLAGGED",
            summary: "Overqualification flag: 14 years experience applying for Mid-Level role; potential salary expectation mismatch.",
            question: "What motivations lead you to target this individual contributor role given your extensive senior background?",
            feedback: "Profile exceeds seniority baseline; recruiter should verify salary alignment and scope expectations."
        },
        {
            id: "CAND-003310",
            token: "TOKEN-ANON-59123",
            role: "BI & Decision Intelligence Specialist",
            exp: "4 Years",
            match_score: 64.8,
            category: "HUMAN_REVIEW_FLAGGED",
            summary: "Borderline fit: High Power BI and SQL skills, but missing required experience in Snowflake and dbt.",
            question: "How have you modeled dimensional star schemas in VertiPaq when source data lacked pre-aggregated marts?",
            feedback: "Solid BI foundation; building hands-on dbt semantic projects will solidify senior eligibility."
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
            feedback: "Thank you for applying. We encourage completing foundational projects in Python and Git to qualify for future cycles."
        }
    ]
};

let currentFilter = "ALL";

// Initialize Dashboard on DOM Load
document.addEventListener("DOMContentLoaded", async () => {
    // Try to load dynamic data from dashboard_data.json if exists
    try {
        const response = await fetch("data/dashboard_data.json");
        if (response.ok) {
            dashboardData = await response.json();
        }
    } catch (e) {
        console.log("Using embedded live dashboard telemetry.");
    }

    renderKPIs();
    renderFunnelChart();
    renderChannelChart();
    renderTriageTable();
});

function renderKPIs() {
    document.getElementById("kpi-total-apps").textContent = dashboardData.kpis.total_applications.toLocaleString();
    document.getElementById("kpi-passed-triage").textContent = dashboardData.kpis.passed_triage.toLocaleString();
    document.getElementById("kpi-interviews").textContent = dashboardData.kpis.interviews.toLocaleString();
    document.getElementById("kpi-offers").textContent = dashboardData.kpis.offers.toLocaleString();
    document.getElementById("kpi-hires").textContent = dashboardData.kpis.hires.toLocaleString();
}

function renderFunnelChart() {
    const ctx = document.getElementById("funnelChart").getContext("2d");
    const labels = dashboardData.funnel.map(f => f.stage);
    const dataCounts = dashboardData.funnel.map(f => f.count);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Candidate Volume",
                data: dataCounts,
                backgroundColor: [
                    "rgba(56, 189, 248, 0.7)",
                    "rgba(52, 211, 153, 0.7)",
                    "rgba(129, 140, 248, 0.7)",
                    "rgba(251, 191, 36, 0.7)",
                    "rgba(14, 165, 233, 0.7)"
                ],
                borderColor: [
                    "#38bdf8",
                    "#34d399",
                    "#818cf8",
                    "#fbbf24",
                    "#0ea5e9"
                ],
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "#0f172a",
                    titleColor: "#f8fafc",
                    bodyColor: "#94a3b8",
                    borderColor: "#334155",
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: "#94a3b8", font: { size: 10 } }
                },
                y: {
                    grid: { color: "rgba(51, 65, 85, 0.3)" },
                    ticks: { color: "#94a3b8", font: { size: 10 } }
                }
            }
        }
    });
}

function renderChannelChart() {
    const ctx = document.getElementById("channelChart").getContext("2d");
    const labels = dashboardData.channels.map(c => c.name);
    const dataHires = dashboardData.channels.map(c => c.hires);

    new Chart(ctx, {
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
                    labels: { color: "#94a3b8", font: { size: 10 }, boxWidth: 12 }
                }
            },
            cutout: "68%"
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
        tr.className = "hover:bg-slate-800/40 transition-colors";

        let badgeClass = "badge-reject";
        if (c.category === "DIRECT_APPLICABLE") badgeClass = "badge-direct";
        else if (c.category === "HUMAN_REVIEW_FLAGGED") badgeClass = "badge-review";

        tr.innerHTML = `
            <td class="py-2.5 px-3 font-mono font-medium text-slate-200">${c.id}</td>
            <td class="py-2.5 px-3 text-slate-300 font-semibold">${c.role}</td>
            <td class="py-2.5 px-3 text-slate-400">${c.exp}</td>
            <td class="py-2.5 px-3 text-center">
                <span class="font-bold text-sky-400">${c.match_score}%</span>
            </td>
            <td class="py-2.5 px-3">
                <span class="${badgeClass}">${c.category.replace('_', ' ')}</span>
            </td>
            <td class="py-2.5 px-3 text-right">
                <button onclick="inspectCandidate('${c.id}')" class="text-[11px] font-semibold text-sky-400 hover:text-sky-300 underline">
                    Inspect AI Brief
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

    document.getElementById("briefing-cand-token").textContent = cand.token;
    document.getElementById("briefing-cand-role").textContent = `(${cand.role})`;
    document.getElementById("briefing-summary").textContent = cand.summary;
    document.getElementById("briefing-question").textContent = `"${cand.question}"`;
    document.getElementById("briefing-feedback").textContent = cand.feedback;
}
