// Floating "ask the tutor" widget — talks to the shared kontor-tutor-worker
// (same backend Athena uses). No key here, ever — the Worker holds it.
const TUTOR_WORKER_URL = 'https://kontor-tutor-worker.kwasikontor45-995.workers.dev';

function currentLessonTitle() {
  return document.title.replace(/\s*\|\s*Python Tutor\s*$/, '').trim() || 'Python basics';
}

async function askTutor(question) {
  try {
    const res = await fetch(TUTOR_WORKER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ site: 'py-bite', lessonTitle: currentLessonTitle(), question }),
    });
    const data = await res.json();
    if (!res.ok) return { error: data.error || 'tutor is unavailable right now' };
    return { reply: data.reply };
  } catch {
    return { error: 'tutor is unavailable right now' };
  }
}

function buildWidget() {
  const wrap = document.createElement('div');
  wrap.className = 'tutor-widget';
  wrap.innerHTML = `
    <button class="tutor-widget__toggle" aria-label="ask the tutor">🐍 ask</button>
    <div class="tutor-widget__panel" hidden>
      <div class="tutor-widget__reply" hidden></div>
      <div class="tutor-widget__row">
        <input class="tutor-widget__input" placeholder="what's tripping you up?" maxlength="500" />
        <button class="tutor-widget__send">ask</button>
      </div>
      <p class="tutor-widget__error" hidden></p>
    </div>
  `;
  document.body.appendChild(wrap);

  const toggle = wrap.querySelector('.tutor-widget__toggle');
  const panel  = wrap.querySelector('.tutor-widget__panel');
  const input  = wrap.querySelector('.tutor-widget__input');
  const send   = wrap.querySelector('.tutor-widget__send');
  const reply  = wrap.querySelector('.tutor-widget__reply');
  const error  = wrap.querySelector('.tutor-widget__error');

  toggle.addEventListener('click', () => {
    panel.hidden = !panel.hidden;
    if (!panel.hidden) input.focus();
  });

  async function handleAsk() {
    const q = input.value.trim();
    if (!q) return;
    send.disabled = true;
    send.textContent = '…';
    error.hidden = true;
    const result = await askTutor(q);
    send.disabled = false;
    send.textContent = 'ask';
    if (result.error) {
      error.textContent = result.error;
      error.hidden = false;
      return;
    }
    reply.textContent = '🐍 ' + result.reply;
    reply.hidden = false;
  }

  send.addEventListener('click', handleAsk);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') handleAsk(); });
}

document.addEventListener('DOMContentLoaded', buildWidget);
