# 🐍 py-bite

A Flask web app that mirrors your exact Python course syllabus — chapter by chapter, with quizzes, progress tracking, and an interactive code runner.

> **Formerly "python-tutor"** — renamed for brevity.

**Live:** https://py-bite.kontor.studio (also https://py-bite.onrender.com)

## Why This Exists

Instead of passively watching videos, you are **building the tool that teaches you Python**. Every feature you add (routes, templates, quiz logic) reinforces the concepts you're studying. That's the meta-move: the project *is* the learning.

## Features

- **6 Chapters** covering Python Basics, Control Flow, Functions, Collections, Advanced Topics, and Object-Oriented Security Scripting (O-O/S-S)
- **Interactive Code Editor** with a live Python subprocess runner
- **Quiz Engine** with instant feedback and explanations
- **Progress Tracking** stored locally in JSON
- **Rose Pine Moon × Phosphor Noir UI** with circadian engine — phases shift color palette by time of day (renewal · choice · desire · nyx)
- **Manager Script** — install, start, stop, update, uninstall like `war-room`

---

## Quick Start (Local)

### Option A: Manager Script (recommended)

```bash
# 1. Copy py-bite.sh anywhere (Desktop, ~/scripts, etc.)
# 2. Run it
./py-bite.sh install   # clones repo, creates venv, installs deps
./py-bite.sh start     # launches on http://localhost:5000
./py-bite.sh stop      # kills the server
./py-bite.sh status    # shows running state
./py-bite.sh logs      # tail server output
./py-bite.sh update    # pull latest + reinstall deps
./py-bite.sh uninstall # DELETE everything (asks for confirmation)
```

### Option B: Manual

```bash
git clone git@github.com:kwasikontor45/py-bite.git
cd py-bite
bash install.sh
bash run.sh
```

### Option C: Really Manual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then open [http://localhost:5000](http://localhost:5000).

---

## Can I Run This on My Website?

**Short answer:** Not directly on static hosting (Cloudflare Pages, Netlify, GitHub Pages) because py-bite needs a Python backend to execute code and track progress.

**Options to make it web-accessible:**

| Option | Effort | Cost | Notes |
|--------|--------|------|-------|
| **Render** | Low | Free | Python web service tier. Auto-deploys from GitHub. Sleep after 15 min inactivity. |
| **PythonAnywhere** | Low | Free | Flask-ready. Limited daily CPU. Good for light use. |
| **Fly.io** | Medium | Free tier | Like war-room. Needs `fly.toml`. Stays awake if you add a credit card. |
| **Self-hosted VPS** | Medium | $5/mo | Linode, DigitalOcean, Hetzner. Full control. |
| **Static conversion** | High | Free | Lose code execution + progress tracking. Not recommended. |

**Recommended path:** Deploy to **Render** (free, zero-config for Flask) and iframe or link it from `kontor.studio/arc-lt-labs`.

---

## Project Structure

```
py-bite/
├── py-bite.sh              # Manager script (install/start/stop/update/uninstall)
├── install.sh              # One-command setup (alternative)
├── run.sh                  # Quick launcher
├── run.py                  # Flask entry point
├── requirements.txt        # Python deps
├── README.md
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # URL routes
│   ├── content.py          # Course content (5 chapters)
│   ├── quizzes.py          # Quiz data
│   ├── code_runner.py      # Safe code execution
│   ├── progress_tracker.py # JSON-based progress
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── chapter.html
│       ├── lesson.html
│       └── quiz.html
└── data/
    └── .gitkeep            # progress.json lives here (gitignored)
```

---

## How It Works

- **Content** is stored per-chapter in `app/` — easy to edit and extend.
- **Quizzes** live in `app/quizzes.py`. Each chapter has questions with multiple choice and true/false formats.
- **Progress** is saved to `data/progress.json` — no database needed.
- **Code Execution** runs in a subprocess with a 5-second timeout. Safe mode uses AST filtering for simple expressions.

---

## Customizing

Want to add a new chapter? Edit `app/content.py` and follow the existing structure. Add a quiz in `app/quizzes.py` using the same `chapter_id`. That's it.

---

## Tech Stack

- Python 3.8+
- Flask
- Vanilla HTML / CSS / JS

## License

MIT
