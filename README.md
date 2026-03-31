# 🧮 MathArena Mock Test Generator

**Career Launcher** · CAT & IPM Quantitative Aptitude Mock Tests

A full-featured Streamlit web app for practising CAT and IPM QA using **721 real exam questions** (CAT 2017–2025, IPMAT 2020–2024).

---

## Features

- **28 real exam papers** — CAT (2017–2025, all slots) + IPMAT Indore (2020–2024)
- **Random Mock Mode** — auto-samples 22 (CAT) or 40 (IPM) questions from mixed years
- **Accurate marking** — CAT: +3/−1/0 · IPM: +4/−1/0 · No penalty for TITA/SA
- **Live countdown timer** — 40 min (CAT QA) · 90 min (IPM)
- **Question map** in sidebar — navigate by number, see answered/flagged/unanswered at a glance
- **Flag for review** — mark questions to revisit before submitting
- **Detailed results page**:
  - Score, accuracy, time taken
  - Topic-wise stacked bar chart (correct / wrong / skipped)
  - Per-question review with correct answer reveal
  - Filter by Correct / Wrong / Unattempted

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/matharena-mock.git
cd matharena-mock
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run locally

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploy on Streamlit Cloud (free)

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch `main`, file `app.py`.
4. Click **Deploy** — live in ~2 minutes.

No extra config needed. `requirements.txt` and `.streamlit/config.toml` are already set up.

---

## Project Structure

```
matharena-mock/
├── app.py                  # Main Streamlit application
├── data/
│   └── questions.json      # 721 questions across 28 exam sets
├── .streamlit/
│   └── config.toml         # Theme and server config
├── requirements.txt
└── README.md
```

---

## Question Data

All questions are sourced from the **MathArena** database (Career Launcher).

| Exam | Years | Sets | Questions |
|------|-------|------|-----------|
| CAT  | 2017–2025 | 24 slots | 612 |
| IPM (IPMAT Indore) | 2020–2024 | 4 papers | 109 |
| **Total** | | **28** | **721** |

**Topics covered:** Algebra · Geometry · Ratios · TSD · Number System · Progressions · Logarithms · Time & Work · SI/CI · Functions · Profit/Loss · PnC · Mixtures · Co-Geo

---

## Marking Schemes

| Exam | Correct | Wrong (MCQ) | TITA/SA | Unattempted |
|------|---------|-------------|---------|-------------|
| CAT  | +3      | −1          | 0       | 0           |
| IPM  | +4      | −1          | 0       | 0           |

---

## Tech Stack

- [Streamlit](https://streamlit.io) — UI framework
- Pure Python — no database, no backend
- Questions stored as a single `questions.json` file

---

*Built by Career Launcher · MathArena Project*
