# 🐍 py-bite

A Python learning course with chapter lessons, quizzes, private browser-local progress, and an isolated in-browser Python runner. Flask templates are rendered to static pages for Cloudflare Pages.

> **Formerly "python-tutor"** — renamed for brevity.

**Production:** [py-bite.pages.dev](https://py-bite.pages.dev)

**Custom domains:** [py-bite.kwasikontor.dev](https://py-bite.kwasikontor.dev) · [py-bite.kontor.studio](https://py-bite.kontor.studio) (served through the existing Cloudflare Workers).

## Why This Exists

Instead of passively watching videos, you are **building the tool that teaches you Python**. Every feature you add (routes, templates, quiz logic) reinforces the concepts you're studying. That's the meta-move: the project *is* the learning.

## Features

- **12 Chapters and 51 lessons** across Python, networking, automation, and security
- **Interactive Code Editor** running pinned Pyodide in a dedicated browser worker; course code never executes on the web host
- **Quiz Engine** with instant feedback and explanations
- **Progress Tracking** stored in this browser only, with JSON export/import for portability
- **Rose Pine Moon × Phosphor Noir UI** with circadian engine — phases shift color palette by canonical time of day (Nyx · Choice · Desire · Still-Pine)
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

## Cloudflare Pages

The production build is static. It has no server-side code-execution or progress API. Python runs in a browser worker using the locally hosted Pyodide 314.0.7 runtime; the worker has a separate CSP that allows only same-origin runtime assets and blocks remote connections, in addition to a five-second execution limit and bounded output. OS-specific examples that use `subprocess` need a real local Linux environment.

Progress and quiz scores are stored in browser `localStorage` on the current device and origin. They are not synced to a server. Use **Export progress** and **Import progress** to move a backup between browsers or devices. Previously stored host-side progress is not included in the static site and must be exported from its source if it is still available.

Build locally from a clean checkout:

```bash
python3 -m pip install -r requirements.txt
python3 tools/build-static.py
```

The Cloudflare Pages project is Git-connected to this repository and builds `main` with `python3 -m pip install --user -r requirements.txt && python3 tools/build-static.py`; pushes to `main` publish automatically. The two custom-domain Workers use the versioned proxy in `cloudflare/py-bite-pages-proxy.js`; it forwards only GET/HEAD and never forwards cookies or authorization headers. The generated output has 80 pages and 79 route redirects. Cloudflare security headers are generated into `dist/_headers`; there are no Pages Functions or app-owned server endpoints. Earlier Pages deployments remain available for rollback; the former PythonAnywhere and Render upstreams are not verified fallbacks.

The optional AI tutor remains an explicit external feature. When used, it sends the submitted question and page title to the shared `kontor-tutor-worker`; the widget displays this before the user submits a question.

---

## Project Structure

```text
py-bite/
├── app/content.py                 # Course lessons and resources
├── app/quizzes.py                 # Chapter quiz data
├── app/routes.py                  # Flask template routes used by the static builder
├── app/static/js/app.js           # Browser-local progress, quizzes, and editor UI
├── app/static/js/python-worker.js  # Isolated browser Python runner
├── app/static/vendor/pyodide/     # Pinned, self-hosted runtime and notices
├── app/templates/                 # Course page templates
├── tools/build-static.py          # Render the Pages site into dist/
└── wrangler.toml                  # Cloudflare Pages build output configuration
```

## How It Works

- Course content and quiz answers are rendered into static HTML during the build.
- Progress and quiz scores stay in the current browser's local storage. Export/import files are the portability mechanism; there is no shared progress database.
- Learner Python runs in a dedicated Web Worker using the bundled Pyodide runtime, with a five-second execution limit and bounded output. Server-side execution endpoints have been removed.
- OS-specific lessons that call `subprocess` are demonstrations for a real local Python/Linux environment; those commands cannot run in the browser sandbox.
- The optional tutor is a separate service. The widget explains what it sends before submission.

## Customizing

Want to add a new chapter? Edit `app/content.py` and follow the existing structure. Add a quiz in `app/quizzes.py` using the same `chapter_id`. That's it.

---

## Tech Stack

- Python 3.8+
- Flask (build-time template renderer)
- Cloudflare Pages (static hosting)
- Vanilla HTML / CSS / JS and Pyodide

## License

MIT
