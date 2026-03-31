"""
MathArena Mock Test Generator
Career Launcher — CAT & IPM QA Mock Tests
"""

import json
import time
import random
import re
import io
from pathlib import Path
import streamlit as st
from fpdf import FPDF

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MathArena Mock Tests",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ─────────────────────────────────────────────────────────────────
TOPIC_COLORS = {
    "Algebra":      "#2563EB",
    "PnC":          "#7C3AED",
    "Logarithms":   "#DB2777",
    "Number System":"#D97706",
    "SI/CI":        "#059669",
    "Functions":    "#4F46E5",
    "Mixtures":     "#0D9488",
    "TSD":          "#EA580C",
    "Ratios":       "#CA8A04",
    "Geometry":     "#DC2626",
    "Co-Geo":       "#E11D48",
    "Profit/Loss":  "#16A34A",
    "Time & Work":  "#0284C7",
    "Progressions": "#9333EA",
}

CAT_TIME = 40 * 60   # 40 minutes in seconds
IPM_TIME = 90 * 60   # 90 minutes in seconds

CAT_MARKING  = {"correct": 3,  "wrong": -1, "unattempted": 0}
IPM_MARKING  = {"correct": 4,  "wrong": -1, "unattempted": 0}

EXAM_META = {
    # CAT Practice Sets
    "CAT_SET_1A": {"label": "CAT Practice Set 1A", "exam": "CAT"},
    "CAT_SET_1B": {"label": "CAT Practice Set 1B", "exam": "CAT"},
    "CAT_SET_1C": {"label": "CAT Practice Set 1C", "exam": "CAT"},
    "CAT_SET_2A": {"label": "CAT Practice Set 2A", "exam": "CAT"},
    "CAT_SET_2B": {"label": "CAT Practice Set 2B", "exam": "CAT"},
    "CAT_SET_2C": {"label": "CAT Practice Set 2C", "exam": "CAT"},
    "CAT_SET_3A": {"label": "CAT Practice Set 3A", "exam": "CAT"},
    "CAT_SET_3B": {"label": "CAT Practice Set 3B", "exam": "CAT"},
    "CAT_SET_3C": {"label": "CAT Practice Set 3C", "exam": "CAT"},
    # CAT Full Mocks
    "CAT_MOCK_1": {"label": "CAT Full Mock 1",     "exam": "CAT"},
    "CAT_MOCK_2": {"label": "CAT Full Mock 2",     "exam": "CAT"},
    "CAT_MOCK_3": {"label": "CAT Full Mock 3",     "exam": "CAT"},
    "CAT_MOCK_4": {"label": "CAT Full Mock 4",     "exam": "CAT"},
    "CAT_MOCK_5": {"label": "CAT Full Mock 5",     "exam": "CAT"},
    "CAT_MOCK_6": {"label": "CAT Full Mock 6",     "exam": "CAT"},
    "CAT_MOCK_7": {"label": "CAT Full Mock 7",     "exam": "CAT"},
    "CAT_MOCK_8": {"label": "CAT Full Mock 8",     "exam": "CAT"},
    # IPM Full Mocks
    "IPM_MOCK_1": {"label": "IPM Full Mock 1",     "exam": "IPM"},
    "IPM_MOCK_2": {"label": "IPM Full Mock 2",     "exam": "IPM"},
    "IPM_MOCK_3": {"label": "IPM Full Mock 3",     "exam": "IPM"},
    "IPM_MOCK_4": {"label": "IPM Full Mock 4",     "exam": "IPM"},
    "IPM_MOCK_5": {"label": "IPM Full Mock 5",     "exam": "IPM"},
    "IPM_MOCK_6": {"label": "IPM Full Mock 6",     "exam": "IPM"},
}

# ─── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_questions():
    data_path = Path(__file__).parent / "data" / "questions.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"

def clean_html(text: str) -> str:
    """Strip basic HTML tags from question text."""
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def get_marking(exam: str) -> dict:
    return IPM_MARKING if exam == "IPM" else CAT_MARKING

def generate_pdf(questions, label, exam, include_answers=False):
    """Generate a downloadable PDF question paper."""
    marking = get_marking(exam)
    total_q  = len(questions)
    max_marks = total_q * marking["correct"]
    duration  = "90 minutes" if exam == "IPM" else "40 minutes"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Header ──────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "MathArena — Career Launcher", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, label, ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6,
        f"Questions: {total_q}   |   Max Marks: {max_marks}   |   Duration: {duration}   |   "
        f"Marking: +{marking['correct']} / {marking['wrong']} (MCQ) / 0 (TITA)",
        ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(37, 99, 235)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # ── Instructions ────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "Instructions:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    instructions = [
        f"1. This paper has {total_q} questions. Each MCQ has 4 options; TITA requires a numeric answer.",
        f"2. MCQ: +{marking['correct']} for correct, {marking['wrong']} for wrong, 0 for unattempted.",
        "3. TITA: +3 for correct, 0 for wrong/unattempted (no negative marking).",
        f"4. Total time: {duration}. Manage your time wisely.",
    ]
    for ins in instructions:
        pdf.multi_cell(0, 5, ins)
    pdf.ln(4)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # ── Questions ────────────────────────────────────────────────────────────
    for i, q in enumerate(questions, 1):
        q_text = clean_html(q.get("q", ""))
        q_type = q.get("type", "MCQ")
        topic  = q.get("topic", "")
        opts   = q.get("opts", [])

        # Question number + type badge
        pdf.set_font("Helvetica", "B", 10)
        badge = f"[{q_type}]"
        pdf.set_fill_color(239, 246, 255)
        pdf.cell(0, 6, f"Q{i}.  {badge}  [{topic}]", ln=True, fill=True)

        # Question text
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, q_text, border=0)
        pdf.ln(1)

        # Options
        if q_type == "MCQ" and opts:
            option_labels = ["(A)", "(B)", "(C)", "(D)"]
            for j, opt in enumerate(opts[:4]):
                pdf.set_font("Helvetica", "", 10)
                label_text = option_labels[j] if j < len(option_labels) else f"({j+1})"
                pdf.cell(10, 5, label_text)
                pdf.multi_cell(0, 5, clean_html(str(opt)))
        else:
            pdf.set_font("Helvetica", "I", 9)
            pdf.cell(0, 5, "Answer: _____________ (Write numeric answer)", ln=True)

        # Answer (if answer key mode)
        if include_answers:
            ans = q.get("ans", "")
            pdf.set_font("Helvetica", "BI", 9)
            pdf.set_text_color(22, 163, 74)
            if q_type == "MCQ" and opts and ans in opts:
                ans_label = ["A","B","C","D"][opts.index(ans)]
                pdf.cell(0, 5, f"  Ans: ({ans_label}) {ans}", ln=True)
            else:
                pdf.cell(0, 5, f"  Ans: {ans}", ln=True)
            pdf.set_text_color(0, 0, 0)

        pdf.ln(3)

    # ── Answer Key page (if not inline) ─────────────────────────────────────
    if not include_answers:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Answer Key", ln=True, align="C")
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)
        cols = 4
        col_w = 45
        for i, q in enumerate(questions, 1):
            ans  = q.get("ans", "")
            opts = q.get("opts", [])
            if q.get("type") == "MCQ" and opts and ans in opts:
                ans_disp = ["A","B","C","D"][opts.index(ans)]
            else:
                ans_disp = str(ans)
            pdf.cell(col_w, 7, f"Q{i:2d}: {ans_disp}", border=1)
            if i % cols == 0:
                pdf.ln()
        pdf.ln(10)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()

def score_answers(questions, answers, exam):
    marking = get_marking(exam)
    total = 0
    correct = 0
    wrong = 0
    unattempted = 0
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        if user_ans is None or user_ans == "":
            unattempted += 1
            total += marking["unattempted"]
        else:
            correct_ans = q["ans"]
            if q["type"] == "MCQ":
                if str(user_ans) == str(correct_ans):
                    correct += 1
                    total += marking["correct"]
                else:
                    wrong += 1
                    total += marking["wrong"]
            else:  # TITA
                try:
                    if abs(float(str(user_ans)) - float(str(correct_ans))) < 0.01:
                        correct += 1
                        total += marking["correct"]
                    else:
                        wrong += 1
                        # No penalty for TITA
                except (ValueError, TypeError):
                    if str(user_ans).strip().lower() == str(correct_ans).strip().lower():
                        correct += 1
                        total += marking["correct"]
                    else:
                        wrong += 1
    return {"total": total, "correct": correct, "wrong": wrong, "unattempted": unattempted}

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #cbd5e1 !important; }

/* Header bar */
.header-bar {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
    padding: 1.2rem 1.8rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-bar h1 { color: #f8fafc; margin: 0; font-size: 1.6rem; }
.header-bar .subtitle { color: #94a3b8; font-size: 0.9rem; margin-top: 4px; }

/* Timer */
.timer-box {
    background: #1e293b;
    color: #f1f5f9;
    font-size: 2rem;
    font-weight: 800;
    padding: 0.5rem 1.2rem;
    border-radius: 10px;
    letter-spacing: 3px;
    font-family: monospace;
    text-align: center;
}
.timer-warning { background: #7c2d12; color: #fef2f2; }
.timer-critical { background: #991b1b; color: #fef2f2; animation: pulse 1s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.6} }

/* Question card */
.q-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563eb;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.q-meta { font-size: 0.78rem; color: #64748b; margin-bottom: 0.6rem; }
.q-text { font-size: 1.05rem; line-height: 1.7; color: #1e293b; white-space: pre-wrap; }

/* Topic pill */
.topic-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    color: white;
    margin-left: 8px;
}

/* Nav buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}

/* Score card */
.score-card {
    background: linear-gradient(135deg, #1e3a5f, #0f172a);
    color: white;
    padding: 2rem;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 1.5rem;
}
.score-big { font-size: 3.5rem; font-weight: 900; color: #38bdf8; }
.score-label { font-size: 1rem; color: #94a3b8; margin-top: 4px; }

/* Result row */
.res-correct { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.6rem; }
.res-wrong   { background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.6rem; }
.res-skip    { background: #f8fafc; border-left: 4px solid #94a3b8; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.6rem; }

/* Progress bar */
.prog-bar-outer { background: #e2e8f0; border-radius: 999px; height: 8px; overflow: hidden; margin: 6px 0; }
.prog-bar-inner { background: #2563eb; height: 100%; border-radius: 999px; transition: width 0.4s; }
</style>
""", unsafe_allow_html=True)

# ─── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page":       "home",        # home | test | results
        "set_key":    None,
        "questions":  [],
        "answers":    {},
        "q_index":    0,
        "start_time": None,
        "end_time":   None,
        "submitted":  False,
        "flagged":    set(),
        "q_times":    {},            # per-question time spent
        "q_start":    None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
all_questions = load_questions()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧮 MathArena")
    st.markdown("*Career Launcher*")
    st.divider()

    if st.session_state.page == "test":
        elapsed = time.time() - st.session_state.start_time
        exam = EXAM_META.get(st.session_state.set_key, {}).get("exam") or ("IPM" if "IPM" in st.session_state.set_key else "CAT")
        limit = IPM_TIME if exam == "IPM" else CAT_TIME
        remaining = max(0, limit - elapsed)
        css_class = "timer-critical" if remaining < 120 else ("timer-warning" if remaining < 300 else "")
        st.markdown(f'<div class="timer-box {css_class}">{fmt_time(remaining)}</div>', unsafe_allow_html=True)
        st.caption("Time remaining")
        st.divider()

        qs = st.session_state.questions
        answered = len([v for v in st.session_state.answers.values() if v is not None and v != ""])
        flagged  = len(st.session_state.flagged)
        st.markdown(f"**Progress:** {answered}/{len(qs)}")
        pct = answered / len(qs) if qs else 0
        st.markdown(f"""
        <div class="prog-bar-outer">
          <div class="prog-bar-inner" style="width:{pct*100:.0f}%"></div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"🚩 Flagged: **{flagged}**")
        st.divider()

        # Question map
        st.markdown("**Question Map**")
        cols_per_row = 5
        qs_len = len(qs)
        for row_start in range(0, qs_len, cols_per_row):
            row_qs = range(row_start, min(row_start + cols_per_row, qs_len))
            cols = st.columns(len(list(row_qs)))
            for col_idx, qi in enumerate(row_qs):
                with cols[col_idx]:
                    ans_val = st.session_state.answers.get(qi)
                    is_current = qi == st.session_state.q_index
                    is_flagged = qi in st.session_state.flagged
                    is_answered = ans_val is not None and ans_val != ""
                    if is_current:
                        btn_type = "primary"
                    else:
                        btn_type = "secondary"
                    label = f"{'🚩' if is_flagged else ('✓' if is_answered else str(qi+1))}"
                    if st.button(label, key=f"qmap_{qi}", type=btn_type, use_container_width=True):
                        st.session_state.q_index = qi
                        st.rerun()
        st.divider()
        if st.button("⏹ End Test", type="primary", use_container_width=True):
            st.session_state.submitted = True
            st.session_state.end_time = time.time()
            st.session_state.page = "results"
            st.rerun()

    elif st.session_state.page == "results":
        if st.button("🏠 New Mock Test", type="primary", use_container_width=True):
            for k in ["page","set_key","questions","answers","q_index",
                      "start_time","end_time","submitted","flagged","q_times","q_start"]:
                del st.session_state[k]
            init_state()
            st.rerun()

# ─── HOME PAGE ─────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("""
    <div class="header-bar">
      <div>
        <h1>🧮 MathArena Mock Tests</h1>
        <div class="subtitle">Career Launcher · CAT & IPM Quantitative Aptitude · Practice Mocks</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📋 Select Your Mock Test")
        exam_filter = st.radio("Exam", ["All", "CAT", "IPM"], horizontal=True)

        # Build options list
        options = {}
        for key, meta in EXAM_META.items():
            if exam_filter == "All" or meta["exam"] == exam_filter:
                options[meta["label"]] = key

        # Special: custom random mock
        options = {"🎲 Random CAT Mock (22 Qs from mixed years)": "__RANDOM_CAT__",
                   "🎲 Random IPM Mock (40 Qs from mixed years)": "__RANDOM_IPM__",
                   **options}

        selected_label = st.selectbox("Choose paper", list(options.keys()))
        selected_key   = options[selected_label]

        if selected_key.startswith("__RANDOM"):
            exam_type = "CAT" if "CAT" in selected_key else "IPM"
            all_pool = []
            for k, qs in all_questions.items():
                if k.startswith(exam_type):
                    all_pool.extend(qs)
            n = 22 if exam_type == "CAT" else 40
            preview_qs = random.sample(all_pool, min(n, len(all_pool)))
            st.info(f"Will generate {n} questions randomly sampled from all {exam_type} papers.")
        else:
            preview_qs = all_questions.get(selected_key, [])

        # Show quick stats
        n_total  = len(preview_qs)
        n_mcq    = sum(1 for q in preview_qs if q["type"] == "MCQ")
        n_tita   = sum(1 for q in preview_qs if q["type"] == "TITA")
        topics   = {}
        for q in preview_qs:
            topics[q["topic"]] = topics.get(q["topic"], 0) + 1

        exam_for_key = "IPM" if (not selected_key.startswith("__") and selected_key.startswith("IPM")) or "IPM" in selected_key else "CAT"
        time_limit = IPM_TIME if exam_for_key == "IPM" else CAT_TIME
        marking = get_marking(exam_for_key)

        m1, m2, m3 = st.columns(3)
        m1.metric("Questions", n_total)
        m2.metric("MCQ / TITA", f"{n_mcq} / {n_tita}")
        m3.metric("Time Limit", fmt_time(time_limit))

        st.markdown(f"**Marking:** +{marking['correct']} Correct · {marking['wrong']} Wrong MCQ · 0 Wrong TITA")

    with col2:
        st.markdown("### 📊 Topic Breakdown")
        if topics:
            sorted_topics = sorted(topics.items(), key=lambda x: -x[1])
            for topic, cnt in sorted_topics:
                color = TOPIC_COLORS.get(topic, "#64748b")
                pct   = cnt / n_total * 100
                st.markdown(f"""
                <div style="display:flex;align-items:center;margin-bottom:6px;">
                  <span style="width:120px;font-size:0.85rem;color:#1e293b;">{topic}</span>
                  <div style="flex:1;background:#e2e8f0;border-radius:999px;height:16px;overflow:hidden;margin:0 10px;">
                    <div style="background:{color};width:{pct:.0f}%;height:100%;border-radius:999px;"></div>
                  </div>
                  <span style="font-size:0.82rem;color:#475569;width:30px;text-align:right;">{cnt}</span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # ── PDF Download before starting ─────────────────────────────────────────
    if preview_qs and not selected_key.startswith("__RANDOM"):
        with st.expander("📄 Download this paper as PDF"):
            dl_label = EXAM_META.get(selected_key, {}).get("label", selected_key.replace("_"," "))
            dl_exam  = "IPM" if "IPM" in selected_key else "CAT"
            dc1, dc2 = st.columns(2)
            with dc1:
                paper_pdf = generate_pdf(preview_qs, dl_label, dl_exam, include_answers=False)
                st.download_button("⬇️ Question Paper (PDF)", data=paper_pdf,
                    file_name=f"{selected_key}_paper.pdf", mime="application/pdf",
                    use_container_width=True, type="primary")
            with dc2:
                ans_pdf = generate_pdf(preview_qs, dl_label + " — Answers", dl_exam, include_answers=True)
                st.download_button("⬇️ With Answer Key (PDF)", data=ans_pdf,
                    file_name=f"{selected_key}_answers.pdf", mime="application/pdf",
                    use_container_width=True)

    if st.button("🚀 Start Mock Test", type="primary", use_container_width=False):
        if selected_key.startswith("__RANDOM"):
            exam_type = "CAT" if "CAT" in selected_key else "IPM"
            all_pool = []
            for k, qs in all_questions.items():
                if k.startswith(exam_type):
                    all_pool.extend(qs)
            n = 22 if exam_type == "CAT" else 40
            qs = random.sample(all_pool, min(n, len(all_pool)))
            st.session_state.set_key = f"__RANDOM_{exam_type}__"
        else:
            qs = all_questions[selected_key]
            st.session_state.set_key = selected_key

        st.session_state.questions  = qs
        st.session_state.answers    = {}
        st.session_state.q_index    = 0
        st.session_state.start_time = time.time()
        st.session_state.q_start    = time.time()
        st.session_state.flagged    = set()
        st.session_state.q_times    = {}
        st.session_state.page       = "test"
        st.rerun()

# ─── TEST PAGE ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "test":
    qs      = st.session_state.questions
    qi      = st.session_state.q_index
    q       = qs[qi]
    set_key = st.session_state.set_key
    exam    = "IPM" if "IPM" in set_key else "CAT"
    marking = get_marking(exam)

    # Auto-submit on time expiry
    elapsed   = time.time() - st.session_state.start_time
    time_limit = IPM_TIME if exam == "IPM" else CAT_TIME
    remaining  = max(0, time_limit - elapsed)
    if remaining == 0 and not st.session_state.submitted:
        st.session_state.submitted = True
        st.session_state.end_time  = time.time()
        st.session_state.page      = "results"
        st.rerun()

    # Header
    label = EXAM_META.get(set_key, {}).get("label", set_key.replace("_", " "))
    answered_count = len([v for v in st.session_state.answers.values() if v is not None and v != ""])
    st.markdown(f"""
    <div class="header-bar">
      <div>
        <h1>{label}</h1>
        <div class="subtitle">Question {qi+1} of {len(qs)} · {answered_count} answered</div>
      </div>
      <div class="timer-box {'timer-warning' if remaining<300 else ''} {'timer-critical' if remaining<120 else ''}">{fmt_time(remaining)}</div>
    </div>
    """, unsafe_allow_html=True)

    # Question card
    topic = q["topic"]
    color = TOPIC_COLORS.get(topic, "#64748b")
    q_type_badge = "🔢 TITA" if q["type"] == "TITA" else "☑ MCQ"
    q_text = clean_html(q["q"])

    st.markdown(f"""
    <div class="q-card">
      <div class="q-meta">
        Q{qi+1} &nbsp;·&nbsp; {q_type_badge} &nbsp;·&nbsp;
        <span class="topic-pill" style="background:{color};">{topic}</span>
        &nbsp;·&nbsp; Marking: +{marking['correct']} / {marking['wrong'] if q['type']=='MCQ' else '0 (no penalty)'}
      </div>
      <div class="q-text">{q_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # Answer input
    current_answer = st.session_state.answers.get(qi)

    if q["type"] == "MCQ":
        opts = q.get("opts", [])
        if opts:
            opt_labels = [f"{chr(65+i)}. {clean_html(o)}" for i, o in enumerate(opts)]
            # Map stored index to label
            default_idx = None
            if current_answer is not None:
                try:
                    default_idx = int(current_answer)
                except:
                    default_idx = None

            chosen = st.radio(
                "Select your answer:",
                options=list(range(len(opt_labels))),
                format_func=lambda x: opt_labels[x],
                index=default_idx,
                key=f"mcq_{qi}",
            )
            st.session_state.answers[qi] = chosen
        else:
            st.warning("No options available for this question.")
    else:
        tita_val = st.text_input(
            "Enter your answer (numeric):",
            value=str(current_answer) if current_answer is not None else "",
            key=f"tita_{qi}",
            placeholder="Type your answer here…",
        )
        st.session_state.answers[qi] = tita_val if tita_val.strip() else None

    # Flag toggle
    is_flagged = qi in st.session_state.flagged
    flag_label = "🚩 Flagged — click to unflag" if is_flagged else "🏳 Flag for review"
    if st.button(flag_label, key=f"flag_{qi}"):
        if is_flagged:
            st.session_state.flagged.discard(qi)
        else:
            st.session_state.flagged.add(qi)
        st.rerun()

    st.divider()

    # Navigation
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        if st.button("⬅ Previous", disabled=(qi == 0), use_container_width=True):
            st.session_state.q_index = qi - 1
            st.rerun()
    with c2:
        if st.button("➡ Next", disabled=(qi == len(qs) - 1), use_container_width=True):
            st.session_state.q_index = qi + 1
            st.rerun()
    with c3:
        if st.button("⏭ Skip & Next", disabled=(qi == len(qs) - 1), use_container_width=True):
            st.session_state.answers[qi] = None
            st.session_state.q_index = qi + 1
            st.rerun()
    with c4:
        if st.button("✅ Submit Test", type="primary", use_container_width=True):
            st.session_state.submitted = True
            st.session_state.end_time  = time.time()
            st.session_state.page      = "results"
            st.rerun()

    # Auto-refresh every 10 seconds to update timer
    st.markdown("""
    <script>
    setTimeout(function() { window.location.reload(); }, 10000);
    </script>
    """, unsafe_allow_html=True)

# ─── RESULTS PAGE ──────────────────────────────────────────────────────────────
elif st.session_state.page == "results":
    qs      = st.session_state.questions
    answers = st.session_state.answers
    set_key = st.session_state.set_key
    exam    = "IPM" if "IPM" in set_key else "CAT"
    marking = get_marking(exam)

    result  = score_answers(qs, answers, exam)
    elapsed = (st.session_state.end_time or time.time()) - st.session_state.start_time
    label   = EXAM_META.get(set_key, {}).get("label", set_key.replace("_", " "))

    # ── Score banner ──────────────────────────────────────────────────────────
    max_score = len(qs) * marking["correct"]
    pct_score = result["total"] / max_score * 100 if max_score > 0 else 0

    st.markdown(f"""
    <div class="score-card">
      <div style="font-size:1rem;color:#94a3b8;margin-bottom:4px;">{label}</div>
      <div class="score-big">{result['total']}</div>
      <div class="score-label">out of {max_score} marks · {pct_score:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("✅ Correct",     result["correct"])
    m2.metric("❌ Wrong",       result["wrong"])
    m3.metric("⏭ Unattempted", result["unattempted"])
    m4.metric("⏱ Time Taken",  fmt_time(int(elapsed)))
    m5.metric("Accuracy",       f"{result['correct']/(result['correct']+result['wrong'])*100:.0f}%" if (result['correct']+result['wrong'])>0 else "—")

    st.divider()

    # ── Topic-wise analysis ───────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📊 Topic Analysis", "📝 Question Review"])

    with tab1:
        st.markdown("### Topic-wise Performance")
        topic_stats = {}
        for i, q in enumerate(qs):
            t = q["topic"]
            if t not in topic_stats:
                topic_stats[t] = {"correct": 0, "wrong": 0, "skip": 0, "total": 0}
            topic_stats[t]["total"] += 1
            user_ans = answers.get(i)
            if user_ans is None or user_ans == "":
                topic_stats[t]["skip"] += 1
            else:
                ca = q["ans"]
                if q["type"] == "MCQ":
                    if str(user_ans) == str(ca):
                        topic_stats[t]["correct"] += 1
                    else:
                        topic_stats[t]["wrong"] += 1
                else:
                    try:
                        if abs(float(str(user_ans)) - float(str(ca))) < 0.01:
                            topic_stats[t]["correct"] += 1
                        else:
                            topic_stats[t]["wrong"] += 1
                    except:
                        if str(user_ans).strip().lower() == str(ca).strip().lower():
                            topic_stats[t]["correct"] += 1
                        else:
                            topic_stats[t]["wrong"] += 1

        for topic, ts in sorted(topic_stats.items(), key=lambda x: -x[1]["total"]):
            color   = TOPIC_COLORS.get(topic, "#64748b")
            pct_cor = ts["correct"] / ts["total"] * 100 if ts["total"] > 0 else 0
            tc, tw, ts2 = st.columns([2, 5, 1])
            tc.markdown(f"<span style='font-weight:600;color:{color};'>{topic}</span>", unsafe_allow_html=True)
            with tw:
                st.markdown(f"""
                <div style="display:flex;gap:4px;align-items:center;height:28px;">
                  <div style="background:#22c55e;width:{ts['correct']/ts['total']*100:.0f}%;height:100%;border-radius:4px 0 0 4px;min-width:2px;"></div>
                  <div style="background:#ef4444;width:{ts['wrong']/ts['total']*100:.0f}%;height:100%;min-width:2px;"></div>
                  <div style="background:#e2e8f0;width:{ts['skip']/ts['total']*100:.0f}%;height:100%;border-radius:0 4px 4px 0;min-width:2px;"></div>
                </div>
                <div style="font-size:0.72rem;color:#64748b;margin-top:2px;">
                  ✅ {ts['correct']} &nbsp; ❌ {ts['wrong']} &nbsp; ⏭ {ts['skip']} &nbsp; of {ts['total']}
                </div>
                """, unsafe_allow_html=True)
            ts2.markdown(f"**{pct_cor:.0f}%**")

    with tab2:
        st.markdown("### Question-by-Question Review")
        filter_opt = st.radio("Show:", ["All", "Correct ✅", "Wrong ❌", "Unattempted ⏭"], horizontal=True)

        for i, q in enumerate(qs):
            user_ans = answers.get(i)
            ca       = q["ans"]
            q_type   = q["type"]

            # Determine status
            if user_ans is None or user_ans == "":
                status = "skip"
            elif q_type == "MCQ":
                status = "correct" if str(user_ans) == str(ca) else "wrong"
            else:
                try:
                    status = "correct" if abs(float(str(user_ans)) - float(str(ca))) < 0.01 else "wrong"
                except:
                    status = "correct" if str(user_ans).strip().lower() == str(ca).strip().lower() else "wrong"

            # Filter
            if filter_opt == "Correct ✅" and status != "correct": continue
            if filter_opt == "Wrong ❌"   and status != "wrong":   continue
            if filter_opt == "Unattempted ⏭" and status != "skip": continue

            css_class = {"correct": "res-correct", "wrong": "res-wrong", "skip": "res-skip"}[status]
            icon      = {"correct": "✅", "wrong": "❌", "skip": "⏭"}[status]
            color     = TOPIC_COLORS.get(q["topic"], "#64748b")

            q_text_short = clean_html(q["q"])
            if len(q_text_short) > 200:
                q_text_short = q_text_short[:200] + "…"

            # Format correct answer for display
            if q_type == "MCQ" and q.get("opts"):
                try:
                    correct_display = f"({chr(65+int(ca))}) {clean_html(q['opts'][int(ca)])}"
                    user_display    = f"({chr(65+int(user_ans))}) {clean_html(q['opts'][int(user_ans)])}" if user_ans is not None and user_ans != "" else "—"
                except:
                    correct_display = str(ca)
                    user_display    = str(user_ans) if user_ans is not None else "—"
            else:
                correct_display = str(ca)
                user_display    = str(user_ans) if user_ans not in (None, "") else "—"

            with st.expander(f"{icon} Q{i+1} · {q['topic']} · {q_type} — {q_text_short}"):
                st.markdown(f"**Full Question:**\n\n{clean_html(q['q'])}")
                if q_type == "MCQ" and q.get("opts"):
                    for oi, opt in enumerate(q["opts"]):
                        prefix = "✅ " if str(oi) == str(ca) else ("❌ " if str(oi) == str(user_ans) else "   ")
                        st.markdown(f"{prefix}**{chr(65+oi)}.** {clean_html(opt)}")
                col_a, col_b = st.columns(2)
                col_a.markdown(f"**Your answer:** {user_display}")
                col_b.markdown(f"**Correct answer:** {correct_display}")

    # ── PDF Downloads ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 📄 Download Question Paper")
    dl1, dl2 = st.columns(2)
    with dl1:
        paper_pdf = generate_pdf(qs, label, exam, include_answers=False)
        st.download_button(
            label="⬇️ Download Question Paper (PDF)",
            data=paper_pdf,
            file_name=f"{set_key}_question_paper.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    with dl2:
        ans_pdf = generate_pdf(qs, label + " — Answer Key", exam, include_answers=True)
        st.download_button(
            label="⬇️ Download with Answer Key (PDF)",
            data=ans_pdf,
            file_name=f"{set_key}_with_answers.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
