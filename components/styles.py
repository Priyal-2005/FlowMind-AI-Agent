"""
Custom CSS Styles — Enterprise Dark Theme

Glassmorphism cards, animated status indicators, premium typography,
and color-coded status badges for the Command Center dashboard.
"""


def get_main_styles() -> str:
    """Return the main CSS stylesheet."""
    return """
<style>
    /* ── IMPORTS ──────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── ROOT VARIABLES ──────────────────────────── */
    :root {
        --bg-primary: #0E1117;
        --bg-secondary: #1A1C2E;
        --bg-card: rgba(26, 28, 46, 0.7);
        --bg-card-hover: rgba(26, 28, 46, 0.9);
        --accent-primary: #00D4AA;
        --accent-secondary: #6C63FF;
        --accent-warning: #FFB800;
        --accent-error: #FF4B4B;
        --accent-info: #45B7D1;
        --text-primary: #FAFAFA;
        --text-secondary: #8B8FA3;
        --text-muted: #5A5E73;
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-glow: rgba(0, 212, 170, 0.3);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 30px rgba(0, 212, 170, 0.1);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
    }

    /* ── GLOBAL OVERRIDES ────────────────────────── */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp > header {
        background: transparent !important;
    }

    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }

    /* ── HEADER ───────────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        margin-bottom: 1.5rem;
        position: relative;
    }

    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #00D4AA 0%, #6C63FF 50%, #F093FB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .main-header .subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.03em;
    }

    /* ── MODE BADGE (global scope) ──────────────── */
    .mode-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(108, 99, 255, 0.15);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 20px;
        color: #6C63FF;
        font-size: 0.75rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── SUMMARY BANNER ──────────────────────────── */
    .summary-banner {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.08), rgba(108, 99, 255, 0.08));
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 40px rgba(0, 212, 170, 0.05);
        animation: fade-in 0.6s ease-out;
    }

    .summary-banner-inner {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
    }

    .summary-stat {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
    }

    .summary-stat-icon {
        font-size: 1.3rem;
        margin-bottom: 0.2rem;
    }

    .summary-stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
        line-height: 1;
        margin: 0.2rem 0;
    }

    .summary-stat-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }

    .summary-divider {
        width: 1px;
        height: 50px;
        background: var(--border-subtle);
        flex-shrink: 0;
    }

    .summary-banner-label {
        text-align: center;
        margin-top: 0.75rem;
        font-size: 0.75rem;
        color: var(--accent-primary);
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── GLASSMORPHISM CARDS ──────────────────────── */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        box-shadow: var(--shadow-card);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glow);
    }

    .glass-card-accent {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        box-shadow: var(--shadow-card), var(--shadow-glow);
    }

    /* ── KPI METRIC TILES ────────────────────────── */
    .metric-tile {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-tile:hover {
        transform: translateY(-2px);
        border-color: var(--border-glow);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }

    .metric-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        margin: 0;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .metric-green .metric-value { color: var(--accent-primary); }
    .metric-blue .metric-value { color: var(--accent-info); }
    .metric-yellow .metric-value { color: var(--accent-warning); }
    .metric-red .metric-value { color: var(--accent-error); }
    .metric-purple .metric-value { color: var(--accent-secondary); }

    /* ── PIPELINE AGENT CARDS ────────────────────── */
    .pipeline-container {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        padding: 1rem 0;
        overflow-x: auto;
    }

    .agent-card {
        flex: 1;
        min-width: 120px;
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 0.75rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--border-subtle);
        transition: all 0.4s ease;
    }

    .agent-card.idle { opacity: 0.5; }

    .agent-card.running {
        border-color: var(--accent-info);
        box-shadow: 0 0 20px rgba(69, 183, 209, 0.2);
        opacity: 1;
        animation: agent-pulse 1.5s ease-in-out infinite;
    }

    .agent-card.running::before {
        background: linear-gradient(90deg, var(--accent-info), var(--accent-secondary));
    }

    .agent-card.complete {
        border-color: var(--accent-primary);
        opacity: 1;
    }

    .agent-card.complete::before {
        background: var(--accent-primary);
    }

    .agent-card.error {
        border-color: var(--accent-error);
        opacity: 1;
    }

    .agent-card.error::before {
        background: var(--accent-error);
    }

    .agent-icon {
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }

    .agent-name {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.15rem;
    }

    .agent-status {
        font-size: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        padding: 0.1rem 0.4rem;
        border-radius: 10px;
        display: inline-block;
    }

    .status-idle { background: rgba(90, 94, 115, 0.3); color: var(--text-muted); }
    .status-running { background: rgba(69, 183, 209, 0.2); color: var(--accent-info); }
    .status-complete { background: rgba(0, 212, 170, 0.2); color: var(--accent-primary); }
    .status-error { background: rgba(255, 75, 75, 0.2); color: var(--accent-error); }

    .agent-time {
        font-size: 0.6rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.2rem;
    }

    .pipeline-arrow {
        color: var(--text-muted);
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .pipeline-arrow.active {
        color: var(--accent-primary);
    }

    /* ── STATUS BADGES ───────────────────────────── */
    .badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.03em;
    }

    .badge-completed { background: rgba(0, 212, 170, 0.15); color: #00D4AA; border: 1px solid rgba(0, 212, 170, 0.3); }
    .badge-in-progress { background: rgba(69, 183, 209, 0.15); color: #45B7D1; border: 1px solid rgba(69, 183, 209, 0.3); }
    .badge-pending { background: rgba(139, 143, 163, 0.15); color: #8B8FA3; border: 1px solid rgba(139, 143, 163, 0.3); }
    .badge-delayed { background: rgba(255, 184, 0, 0.15); color: #FFB800; border: 1px solid rgba(255, 184, 0, 0.3); }
    .badge-blocked { background: rgba(255, 75, 75, 0.15); color: #FF4B4B; border: 1px solid rgba(255, 75, 75, 0.3); }

    .badge-p0 { background: rgba(255, 75, 75, 0.15); color: #FF4B4B; border: 1px solid rgba(255, 75, 75, 0.3); }
    .badge-p1 { background: rgba(255, 184, 0, 0.15); color: #FFB800; border: 1px solid rgba(255, 184, 0, 0.3); }
    .badge-p2 { background: rgba(69, 183, 209, 0.15); color: #45B7D1; border: 1px solid rgba(69, 183, 209, 0.3); }

    .badge-high { background: rgba(255, 75, 75, 0.15); color: #FF4B4B; border: 1px solid rgba(255, 75, 75, 0.3); }
    .badge-medium { background: rgba(255, 184, 0, 0.15); color: #FFB800; border: 1px solid rgba(255, 184, 0, 0.3); }
    .badge-low { background: rgba(0, 212, 170, 0.15); color: #00D4AA; border: 1px solid rgba(0, 212, 170, 0.3); }

    /* ── TASK TABLE ───────────────────────────────── */
    .task-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 0.4rem;
    }

    .task-table thead th {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-secondary);
        padding: 0.5rem 0.75rem;
        text-align: left;
        border-bottom: 1px solid var(--border-subtle);
    }

    .task-table tbody tr {
        background: var(--bg-card);
        transition: all 0.2s ease;
    }

    .task-table tbody tr:hover {
        background: var(--bg-card-hover);
        transform: translateX(2px);
    }

    .task-table tbody tr.row-delayed {
        background: rgba(255, 184, 0, 0.04);
    }

    .task-table tbody tr.row-blocked {
        background: rgba(255, 75, 75, 0.04);
    }

    .task-table tbody tr.row-completed {
        background: rgba(0, 212, 170, 0.03);
    }

    .task-table tbody td {
        padding: 0.6rem 0.75rem;
        font-size: 0.8rem;
        color: var(--text-primary);
        border-top: 1px solid var(--border-subtle);
        border-bottom: 1px solid var(--border-subtle);
    }

    .task-table tbody td:first-child {
        border-left: 1px solid var(--border-subtle);
        border-radius: 8px 0 0 8px;
    }

    .task-table tbody td:last-child {
        border-right: 1px solid var(--border-subtle);
        border-radius: 0 8px 8px 0;
    }

    .task-id {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        color: var(--accent-secondary);
        font-size: 0.75rem;
    }

    /* ── AUDIT LOG ────────────────────────────────── */
    .audit-entry {
        padding: 0.5rem 0.75rem;
        border-left: 3px solid var(--border-subtle);
        margin-bottom: 0.4rem;
        background: rgba(26, 28, 46, 0.4);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        transition: all 0.2s ease;
        font-size: 0.8rem;
    }

    .audit-entry:hover {
        background: rgba(26, 28, 46, 0.7);
        transform: translateX(3px);
    }

    .audit-entry .timestamp {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-muted);
        font-size: 0.7rem;
    }

    .audit-entry .agent-tag {
        font-weight: 600;
        font-size: 0.75rem;
    }

    .audit-entry .action-text {
        color: var(--text-primary);
        font-size: 0.8rem;
    }

    .audit-entry .reasoning-text {
        color: var(--text-secondary);
        font-size: 0.7rem;
        font-style: italic;
        margin-top: 0.15rem;
    }

    /* Agent-specific border colors */
    .audit-orchestrator { border-left-color: #6C63FF; }
    .audit-extraction { border-left-color: #00D4AA; }
    .audit-intelligence { border-left-color: #FFB800; }
    .audit-execution { border-left-color: #FF6B6B; }
    .audit-tracking { border-left-color: #45B7D1; }
    .audit-decision { border-left-color: #F093FB; }

    /* ── ACTION CARDS ────────────────────────────── */
    .action-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }

    .action-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transform: translateX(2px);
    }

    .action-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.35rem;
    }

    .action-type-badge {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--accent-primary);
    }

    .action-task-id {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: var(--accent-secondary);
        background: rgba(108, 99, 255, 0.1);
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
    }

    .action-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .action-detail {
        font-size: 0.78rem;
        color: var(--text-primary);
        margin-bottom: 0.2rem;
    }

    .action-reasoning {
        font-size: 0.7rem;
        color: var(--text-secondary);
        font-style: italic;
        line-height: 1.4;
    }

    .owner-change {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        margin: 0.2rem 0;
        font-size: 0.75rem;
    }

    .owner-from {
        background: rgba(255, 75, 75, 0.1);
        color: #FF4B4B;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        text-decoration: line-through;
    }

    .owner-to {
        background: rgba(0, 212, 170, 0.1);
        color: #00D4AA;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    .escalation-badge {
        display: inline-block;
        margin-top: 0.3rem;
        font-size: 0.65rem;
        color: #FF4B4B;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    .escalation-card {
        border-left: 3px solid var(--accent-error);
    }

    .reminder-card {
        border-left: 3px solid var(--accent-warning);
    }

    .assignment-card {
        border-left: 3px solid var(--accent-primary);
    }

    /* ── ACTION STAT CARDS ──────────────────────── */
    .action-stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 0.75rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .action-stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        line-height: 1;
    }

    .action-stat-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        margin-top: 0.2rem;
        font-weight: 500;
    }

    .action-stat-blue .action-stat-value { color: #45B7D1; }
    .action-stat-red .action-stat-value { color: #FF4B4B; }
    .action-stat-yellow .action-stat-value { color: #FFB800; }

    /* ── DAY SELECTOR ────────────────────────────── */
    .day-description {
        margin-top: 0.6rem;
        padding: 0.6rem 0.9rem;
        border-left: 3px solid var(--accent-primary);
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        font-size: 0.82rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    .day-description b {
        color: var(--text-primary);
    }

    /* ── SECTION HEADERS ─────────────────────────── */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-subtle);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .section-header .header-icon {
        font-size: 1.2rem;
    }

    .section-header .header-badge {
        font-size: 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        padding: 0.1rem 0.4rem;
        border-radius: 8px;
        background: rgba(108, 99, 255, 0.15);
        color: var(--accent-secondary);
        margin-left: auto;
    }

    /* ── PROCESSING LOG ──────────────────────────── */
    .log-container {
        background: rgba(14, 17, 23, 0.8);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-secondary);
        max-height: 200px;
        overflow-y: auto;
        line-height: 1.6;
    }

    .log-container .log-line {
        padding: 0.1rem 0;
    }

    /* ── ANIMATIONS ──────────────────────────────── */
    @keyframes agent-pulse {
        0%, 100% { box-shadow: 0 0 10px rgba(69, 183, 209, 0.1); }
        50% { box-shadow: 0 0 25px rgba(69, 183, 209, 0.3); }
    }

    @keyframes fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slide-in-right {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 212, 170, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 170, 0.4); }
    }

    .animate-fade-in {
        animation: fade-in 0.5s ease-out;
    }

    .animate-slide-in {
        animation: slide-in-right 0.4s ease-out;
    }

    /* ── SIDEBAR STYLES ──────────────────────────── */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }

    /* ── BUTTON STYLES ───────────────────────────── */
    .stButton > button {
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00D4AA, #00B894) !important;
        border: none !important;
        color: #0E1117 !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 25px rgba(0, 212, 170, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── EXPANDER ─────────────────────────────────── */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        background: var(--bg-card) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ── TAB STYLES ──────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        background: var(--bg-card);
        padding: 0.25rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
        color: var(--text-secondary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(108, 99, 255, 0.15) !important;
        color: var(--text-primary) !important;
    }

    /* ── SCROLLBAR ────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

    /* ── PROGRESS BAR ────────────────────────────── */
    .progress-bar-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        height: 6px;
        overflow: hidden;
        width: 100%;
    }

    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    .progress-green { background: linear-gradient(90deg, #00D4AA, #00B894); }
    .progress-blue { background: linear-gradient(90deg, #45B7D1, #6C63FF); }
    .progress-yellow { background: linear-gradient(90deg, #FFB800, #FF9500); }
    .progress-red { background: linear-gradient(90deg, #FF4B4B, #FF6B6B); }
    
    /* ── HIDE DEFAULT STREAMLIT STUFF ─────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
"""
