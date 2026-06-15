---
title: APEX
emoji: ⚡
colorFrom: yellow
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# ⚡ APEX
### AI-Powered Executive Career Agent

> *"Don't just apply. Outperform."*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=flat-square)](https://langchain.com/langgraph)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%20%2B%20Haiku-CC785C?style=flat-square)](https://anthropic.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=flat-square&logo=huggingface)](https://huggingface.co)

---

**APEX** is a production-grade, multi-agent AI system that optimises every stage of the job application process — from ATS scoring to cover letter generation to interview preparation.

The architectural centrepiece is a **Critique→Rewrite→Re-score loop**: if your resume scores below the ATS threshold, the system critiques the weakest bullet points, rewrites them with injected keywords, and re-scores — repeating until the score crosses the threshold or the iteration limit is reached. This is a real agentic cycle, not a one-shot GPT call.

---

## 🏗️ Architecture

```
Input: Resume PDF + Job Description
            │
            ▼
    ┌───────────────┐
    │  Parser Agent │  ← Claude Haiku (fast structured extraction)
    │  resume + JD  │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │   ATS Agent   │  ← Deterministic skill match + Claude Sonnet semantic scoring
    │  score: 0-100 │
    └───────┬───────┘
            │
     score < 75?
      ┌─────┴─────┐
      YES         NO
      │           │
      ▼           │
 ┌─────────────┐  │
 │   Critique  │  │  ← Claude Sonnet (surgical gap analysis)
 │   Agent     │  │
 └──────┬──────┘  │
        │         │
        ▼         │
 ┌─────────────┐  │
 │   Rewrite   │  │  ← Claude Sonnet (keyword injection + bullet rewriting)
 │   Agent     │  │
 └──────┬──────┘  │
        │         │
        └──► ATS  │   ← Re-score loop (max 2 iterations)
             │    │
             └────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
  Cover Letter  Interview  Learning
    Agent        Agent     Roadmap
    (Sonnet)    (Haiku)    (Haiku)
        │         │         │
        └─────────┴─────────┘
                  │
                  ▼
        Streamlit Dashboard
        (5 tabs, live agent trace)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **ATS Scoring** | Dual-pass: deterministic skill match + Claude semantic analysis |
| 🔄 **Critique→Rewrite Loop** | Agentic self-improvement cycle with up to 2 iterations |
| ✏️ **Resume Optimisation** | Surgical bullet rewrites with keyword injection and diff view |
| 📝 **Cover Letter Agent** | Tailored, ATS-optimised, ~350 words, work permit aware |
| 🎤 **Interview Prep** | HR + Technical + Behavioral + Project-specific Q&A |
| 📚 **Learning Roadmap** | Gap → prioritised resources + portfolio project ideas |
| 📡 **Live Agent Trace** | Real-time pipeline execution visible in the UI |
| 🧩 **LangGraph Orchestration** | Real graph with conditional routing, not a linear chain |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/APEX.git
cd APEX

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Add: ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run

```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
APEX/
├── app.py                        # Streamlit entry point + results dashboard
├── config.py                     # All tunable parameters
├── agents/
│   ├── base_agent.py             # Shared Claude client + JSON extraction
│   ├── parser_agent.py           # Structured resume + JD extraction (Haiku)
│   ├── ats_agent.py              # ATS scoring engine (Sonnet)
│   ├── critique_agent.py         # Surgical gap analysis (Sonnet)
│   ├── rewrite_agent.py          # Keyword-injected bullet rewrites (Sonnet)
│   ├── cover_letter_agent.py     # Tailored cover letter generation (Sonnet)
│   ├── interview_agent.py        # Interview Q&A kit (Haiku)
│   └── learning_agent.py         # Learning roadmap (Haiku)
├── graph/
│   ├── state.py                  # LangGraph TypedDict shared state
│   └── orchestrator.py           # Graph definition + conditional routing
├── core/
│   ├── models.py                 # All Pydantic data contracts
│   └── document_processor.py    # PDF/text ingestion
├── ui/
│   └── styles.py                 # Dark amber theme CSS
├── requirements.txt
├── .env.example
└── Dockerfile
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph (StateGraph with conditional routing) |
| LLM | Claude Sonnet 4.5 (reasoning) + Haiku 4.5 (extraction) |
| Data Validation | Pydantic v2 (strict schemas across all agents) |
| PDF Processing | pdfplumber (text + table extraction) |
| Frontend | Streamlit (live agent trace, tabbed results) |
| Deployment | HuggingFace Spaces (Docker) |

---

## 📝 License

MIT — use freely, build on it, give credit if you'd like.

---

*Built by **Deep Prakashbhai Dobariya** — MSc Artificial Intelligence, BTU Cottbus-Senftenberg*
