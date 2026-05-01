#!/usr/bin/env bash
# py-bite.sh — local installer & manager for py-bite
# Usage: ./py-bite.sh [install|start|stop|restart|status|logs|update|uninstall]
#
# This script stays OUT of the git repo (add it to .gitignore if you copy it elsewhere).
# The actual project lives at: https://github.com/kwasikontor45/py-bite

set -e

REPO_URL="git@github.com:kwasikontor45/py-bite.git"
INSTALL_DIR="${HOME}/py-bite"
VENV_DIR="${INSTALL_DIR}/.venv"
PID_FILE="${INSTALL_DIR}/.pid"
LOG_FILE="${INSTALL_DIR}/.log"

CYAN='\033[0;36m'; BOLD='\033[1m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; RESET='\033[0m'
log() { echo -e " ${GREEN}✓${RESET} $1"; }
warn() { echo -e " ${YELLOW}⚠${RESET} $1"; }
err() { echo -e " ${RED}✗${RESET} $1"; exit 1; }
ask() { echo -e -n " ${CYAN}?${RESET} $1: "; }

# ── helpers ───────────────────────────────────

check_deps() {
  command -v git >/dev/null 2>&1 || err "git not found — install git first"
  if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
  else
    err "python not found — install Python 3.8+ first"
  fi

  PY_VERSION=$($PYTHON -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
  MIN_VERSION="3.8"
  if [ "$(printf '%s\n' "$MIN_VERSION" "$PY_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    err "Python $MIN_VERSION+ required. Found $PY_VERSION."
  fi
}

detect_uv() {
  command -v uv >/dev/null 2>&1
}

ensure_installed() {
  [ -d "${INSTALL_DIR}/.git" ] || err "py-bite not installed. Run: ./py-bite.sh install"
}

is_running() {
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE" 2>/dev/null)
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

# ── commands ──────────────────────────────────

cmd_install() {
  echo -e "\n${CYAN}${BOLD} PY-BITE${RESET} installer\n"
  check_deps

  if [ -d "${INSTALL_DIR}/.git" ]; then
    warn "py-bite already exists at ${INSTALL_DIR}"
    ask "Re-install from GitHub? This preserves data/progress.json. [y/N]"
    read -r CONFIRM
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
      cd "${INSTALL_DIR}"
      git fetch origin
      git reset --hard origin/main
      log "code reset to origin/main"
    else
      log "skipping clone"
    fi
  else
    log "cloning ${REPO_URL} → ${INSTALL_DIR}"
    git clone "${REPO_URL}" "${INSTALL_DIR}"
    log "clone complete"
  fi

  cd "${INSTALL_DIR}"

  # create virtual environment
  if detect_uv; then
    if [ ! -d "$VENV_DIR" ]; then
      log "creating venv with uv…"
      uv venv
    fi
    source "$VENV_DIR/bin/activate"
    log "installing deps with uv…"
    uv pip install -r requirements.txt
  else
    if [ ! -d "$VENV_DIR" ]; then
      log "creating venv with ${PYTHON}…"
      $PYTHON -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
    log "upgrading pip…"
    pip install --quiet --upgrade pip
    log "installing deps…"
    pip install --quiet -r requirements.txt
  fi

  # create data directory
  mkdir -p data
  if [ ! -f "data/progress.json" ]; then
    echo '{}' > data/progress.json
    log "created data/progress.json"
  fi

  echo -e "\n ${CYAN}${BOLD}py-bite installed${RESET}"
  echo -e " directory → ${INSTALL_DIR}"
  echo -e " start   → ./py-bite.sh start"
  echo -e " stop    → ./py-bite.sh stop"
  echo -e " status  → ./py-bite.sh status"
  echo -e " uninstall → ./py-bite.sh uninstall\n"
}

cmd_start() {
  ensure_installed

  if is_running; then
    warn "py-bite is already running (pid $(cat "$PID_FILE"))"
    echo -e " open → http://localhost:5000"
    return
  fi

  cd "${INSTALL_DIR}"

  if detect_uv && [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
  elif [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
  elif [ -d "venv" ]; then
    source "venv/bin/activate"
  fi

  log "starting py-bite on http://localhost:5000"
  nohup python run.py > "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  sleep 1

  if is_running; then
    log "py-bite started (pid $(cat "$PID_FILE"))"
    echo -e " open → http://localhost:5000"
  else
    err "failed to start. check logs: ./py-bite.sh logs"
  fi
}

cmd_stop() {
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID" 2>/dev/null && log "py-bite stopped (pid $PID)"
    else
      warn "process not running"
    fi
    rm -f "$PID_FILE"
  else
    warn "no pid file found — py-bite may not be running"
  fi
}

cmd_restart() {
  cmd_stop || true
  sleep 1
  cmd_start
}

cmd_status() {
  ensure_installed

  echo -e "\n${BOLD} install${RESET}"
  echo -e " directory → ${INSTALL_DIR}"
  echo -e " venv      → ${VENV_DIR}"

  echo -e "\n${BOLD} runtime${RESET}"
  if is_running; then
    log "running (pid $(cat "$PID_FILE"))"
    echo -e " url → http://localhost:5000"
  else
    warn "not running"
  fi

  echo -e "\n${BOLD} commands${RESET}"
  echo -e " start     → ./py-bite.sh start"
  echo -e " stop      → ./py-bite.sh stop"
  echo -e " logs      → ./py-bite.sh logs"
  echo -e " update    → ./py-bite.sh update"
  echo ""
}

cmd_logs() {
  ensure_installed
  if [ -f "$LOG_FILE" ]; then
    tail -n 50 -f "$LOG_FILE"
  else
    warn "no log file yet. start py-bite first."
  fi
}

cmd_update() {
  ensure_installed
  cmd_stop || true
  cd "${INSTALL_DIR}"
  log "pulling latest from GitHub…"
  git pull origin main
  log "reinstalling deps…"
  if detect_uv && [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    uv pip install -r requirements.txt
  elif [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    pip install --quiet -r requirements.txt
  fi
  log "restart to apply: ./py-bite.sh start"
}

cmd_uninstall() {
  if [ ! -d "${INSTALL_DIR}/.git" ]; then
    warn "nothing to uninstall at ${INSTALL_DIR}"
    return
  fi

  echo -e "\n${RED}${BOLD} UNINSTALL PY-BITE${RESET}\n"
  warn "This will remove:"
  echo " - the running server process"
  echo " - virtual environment"
  echo " - the entire ${INSTALL_DIR} directory"
  echo ""
  ask "Type 'DELETE' to confirm"
  read -r CONFIRM
  [ "$CONFIRM" = "DELETE" ] || { log "cancelled"; exit 0; }

  cmd_stop || true
  rm -rf "${INSTALL_DIR}"
  log "py-bite removed"
}

cmd_help() {
  echo -e "\n${CYAN}${BOLD} py-bite.sh${RESET} local manager\n"
  echo " install   clone repo, create venv, install deps"
  echo " start     launch Flask server on localhost:5000"
  echo " stop      kill the server process"
  echo " restart   stop + start"
  echo " status    show install path and running state"
  echo " logs      tail server log file"
  echo " update    pull latest code & reinstall deps"
  echo " uninstall DELETE everything (irreversible)"
  echo ""
}

# ── main ──────────────────────────────────────

case "${1:-help}" in
  install) cmd_install ;;
  start) cmd_start ;;
  stop) cmd_stop ;;
  restart) cmd_restart ;;
  status) cmd_status ;;
  logs) cmd_logs ;;
  update) cmd_update ;;
  uninstall) cmd_uninstall ;;
  *) cmd_help ;;
esac
