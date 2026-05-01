# 🐍 Python Tutor

A local Flask web app that mirrors your exact Python course syllabus — chapter by chapter, with quizzes, progress tracking, and an interactive code runner.

## Why This Exists

Instead of passively watching videos, you are **building the tool that teaches you Python**. Every feature you add (routes, templates, quiz logic) reinforces the concepts you're studying. That's the meta-move: the project *is* the learning.

## Features

- **5 Chapters** covering Python Basics, Control Flow, Functions, Collections, and Advanced Topics
- **Interactive Code Editor** with a live Python subprocess runner
- **Quiz Engine** with instant feedback and explanations
- **Progress Tracking** stored locally in JSON
- **Clean Dark UI** built with vanilla HTML/CSS/JS
- **One-Command Install** via `install.sh`

## Quick Start

```bash
# Clone the repo
git clone <your-repo-url>
cd python-tutor

# Install & run
bash install.sh
bash run.sh
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Manual Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Project Structure

```
python-tutor/
├── install.sh              # One-command setup
├── run.sh                  # Quick launcher
├── run.py                  # Flask entry point
├── requirements.txt        # Python deps
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
    └── progress.json       # Your local progress
```

## How It Works

- **Content** is stored in `app/content.py` as plain Python data structures — easy to edit and extend.
- **Quizzes** live in `app/quizzes.py`. Each chapter has 5 questions with multiple choice and true/false formats.
- **Progress** is saved to `data/progress.json` — no database needed.
- **Code Execution** runs in a subprocess with a 5-second timeout. Safe mode uses AST filtering for simple expressions.

## Customizing

Want to add a new chapter? Edit `app/content.py` and follow the existing structure. Add a quiz in `app/quizzes.py` using the same `chapter_id`. That's it.

## Tech Stack

- Python 3.8+
- Flask
- Vanilla HTML / CSS / JS

## License

MIT
