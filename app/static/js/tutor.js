// Floating "ask the tutor" widget — talks to the shared kontor-tutor-worker
// (same backend Athena uses). No key here, ever — the Worker holds it.
const TUTOR_WORKER_URL = 'https://kontor-tutor-worker.kwasikontor45-995.workers.dev';
const REQUEST_TIMEOUT_MS = 14000;
const MAX_QUESTION_LENGTH = 500;
const MAX_REPLY_LENGTH = 2500;
const MAX_RESPONSE_BYTES = 8192;

function currentLessonTitle() {
  return document.title.replace(/\s*\|\s*Python Tutor\s*$/, '').trim() || 'Python basics';
}

async function readBoundedJson(response) {
  const length = Number(response.headers.get('Content-Length'));
  if (Number.isFinite(length) && length > MAX_RESPONSE_BYTES) throw new Error('response too large');
  if (!response.headers.get('Content-Type')?.toLowerCase().includes('application/json')) throw new Error('unexpected response type');
  const reader = response.body?.getReader();
  if (!reader) throw new Error('empty response');
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > MAX_RESPONSE_BYTES) {
        await reader.cancel().catch(() => {});
        throw new Error('response too large');
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes));
}

async function askTutor(question) {
  if (typeof question !== 'string' || !question.trim() || question.trim().length > MAX_QUESTION_LENGTH) {
    return { error: 'Enter a question of 1–500 characters.' };
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const res = await fetch(TUTOR_WORKER_URL, {
      method: 'POST',
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ site: 'py-bite', lessonTitle: currentLessonTitle().slice(0, 120), question: question.trim() }),
    });
    let data;
    try { data = await readBoundedJson(res); } catch { return { error: 'The tutor returned an invalid response.' }; }
    if (!res.ok) return { error: res.status === 429 ? 'The tutor is busy. Try again in a little while.' : 'The tutor is unavailable right now.' };
    if (typeof data?.reply !== 'string' || !data.reply.trim() || data.reply.trim().length > MAX_REPLY_LENGTH) {
      return { error: 'The tutor returned an invalid reply.' };
    }
    return { reply: data.reply.trim() };
  } catch {
    return { error: controller.signal.aborted ? 'The tutor took too long. Try again.' : 'The tutor is unavailable right now.' };
  } finally {
    clearTimeout(timeout);
  }
}

function buildWidget() {
  const wrap = document.createElement('div');
  wrap.className = 'tutor-widget';
  wrap.innerHTML = `
    <button type="button" class="tutor-widget__toggle" aria-label="Ask the AI tutor" aria-expanded="false" aria-controls="tutor-panel">🐍 ask</button>
    <div class="tutor-widget__panel" id="tutor-panel" hidden>
      <div class="tutor-widget__reply" hidden aria-live="polite"></div>
      <p class="tutor-widget__privacy">When you ask, your question and this lesson title go to our shared AI tutor and external AI provider. Avoid names, passwords, or private information.</p>
      <div class="tutor-widget__row">
        <input class="tutor-widget__input" placeholder="what's tripping you up?" maxlength="500" aria-label="Question for the AI tutor" />
        <button class="tutor-widget__send" type="button">ask</button>
      </div>
      <p class="tutor-widget__error" hidden role="status"></p>
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
    toggle.setAttribute('aria-expanded', String(!panel.hidden));
    if (!panel.hidden) input.focus();
  });

  async function handleAsk() {
    const q = input.value.trim();
    if (!q) return;
    send.disabled = true;
    input.disabled = true;
    send.setAttribute('aria-busy', 'true');
    send.textContent = '…';
    error.hidden = true;
    const result = await askTutor(q);
    send.disabled = false;
    input.disabled = false;
    send.removeAttribute('aria-busy');
    send.textContent = 'ask';
    if (result.error) {
      error.textContent = result.error;
      error.hidden = false;
      input.focus();
      return;
    }
    reply.textContent = '🐍 ' + result.reply;
    reply.hidden = false;
  }

  send.addEventListener('click', handleAsk);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') handleAsk(); });
}

document.addEventListener('DOMContentLoaded', buildWidget);
