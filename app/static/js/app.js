'use strict';

const PROGRESS_KEY = 'pybite.progress.v1';

function announceStatus(message) {
    const status = document.getElementById('app-status');
    if (status) status.textContent = message;
}

function readProgress() {
    try {
        const parsed = JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}');
        return {
            completedLessons: Array.isArray(parsed.completedLessons) ? parsed.completedLessons.filter(id => COURSE_DATA.lessonIds.includes(id)) : [],
            quizzes: parsed.quizzes && typeof parsed.quizzes === 'object' && !Array.isArray(parsed.quizzes) ? parsed.quizzes : {},
            updatedAt: parsed.updatedAt || null
        };
    } catch {
        return { completedLessons: [], quizzes: {}, updatedAt: null };
    }
}

function saveProgress(progress) {
    progress.updatedAt = new Date().toISOString();
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
}

function updateGlobalProgress() {
    const progress = readProgress();
    const total = COURSE_DATA.lessonIds.length;
    const pct = total ? Math.round(progress.completedLessons.length / total * 100) : 0;
    const fill = document.getElementById('global-progress-fill');
    const text = document.getElementById('global-progress-text');
    if (fill) fill.style.width = `${pct}%`;
    if (text) text.textContent = `${pct}% complete`;

    const completedStat = document.getElementById('dashboard-completed');
    if (completedStat) completedStat.textContent = progress.completedLessons.length;
    const passedStat = document.getElementById('dashboard-passed');
    if (passedStat) passedStat.textContent = Object.values(progress.quizzes).filter(result => result?.passed).length;

    const completeButton = document.getElementById('mark-complete-btn');
    if (completeButton && progress.completedLessons.includes(completeButton.dataset.lesson)) {
        completeButton.textContent = 'Completed ✓';
        completeButton.disabled = true;
        completeButton.classList.add('btn-secondary');
        completeButton.classList.remove('btn-primary');
        const badge = document.getElementById('completion-badge');
        if (badge) { badge.textContent = 'Completed'; badge.classList.remove('badge-pending'); badge.classList.add('badge-completed'); }
    }

    document.querySelectorAll('.lesson-row[data-lesson]').forEach(row => {
        if (progress.completedLessons.includes(row.dataset.lesson)) {
            row.classList.add('is-complete');
            const link = row.querySelector('.btn');
            if (link) link.setAttribute('aria-label', `Open completed lesson: ${row.querySelector('h3')?.textContent || ''}`);
        }
    });
    document.querySelectorAll('.chapter-card[data-chapter]').forEach(card => {
        const chapter = COURSE_DATA.chapters[card.dataset.chapter];
        if (!chapter) return;
        const completed = chapter.lessonIds.filter(id => progress.completedLessons.includes(id)).length;
        const bar = card.querySelector('.progress-fill');
        const label = card.querySelector('.progress-text');
        if (bar) bar.style.width = `${chapter.lessonIds.length ? completed / chapter.lessonIds.length * 100 : 0}%`;
        if (label) label.textContent = `${completed}/${chapter.lessonIds.length} lessons`;
        const quiz = progress.quizzes[card.dataset.chapter];
        if (quiz?.passed && !card.querySelector('.badge-passed')) {
            const badge = document.createElement('span');
            badge.className = 'badge badge-passed';
            badge.textContent = `Quiz Passed (${quiz.score}/${quiz.total})`;
            card.insertBefore(badge, card.querySelector('a.btn'));
        }
    });
}

function exportProgress() {
    const payload = { format: 'py-bite-progress', version: 1, exportedAt: new Date().toISOString(), progress: readProgress() };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `py-bite-progress-${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    URL.revokeObjectURL(link.href);
    announceStatus('Progress export downloaded.');
}

async function importProgress(file) {
    if (!file || file.size > 100_000) throw new Error('Progress file is too large.');
    const payload = JSON.parse(await file.text());
    if (payload?.format !== 'py-bite-progress' || payload.version !== 1 || !payload.progress) throw new Error('This is not a supported Py-Bite progress export.');
    const imported = payload.progress;
    const completedLessons = Array.isArray(imported.completedLessons) ? [...new Set(imported.completedLessons.filter(id => COURSE_DATA.lessonIds.includes(id)))] : [];
    const quizzes = {};
    for (const [id, result] of Object.entries(imported.quizzes || {})) {
        const chapter = COURSE_DATA.chapters[id];
        if (chapter && Number.isInteger(result?.score) && Number.isInteger(result?.total) && result.total === chapter.quizTotal && result.score >= 0 && result.score <= result.total) {
            quizzes[id] = { score: result.score, total: result.total, passed: result.score >= result.total * 0.7 };
        }
    }
    saveProgress({ completedLessons, quizzes });
    updateGlobalProgress();
}

function showOutput(output, text, kind = '') {
    output.className = `code-output${kind ? ` ${kind}` : ''}`;
    output.textContent = text;
}

function runCode(source, output) {
    if (source.length > 100000) {
        showOutput(output, 'Stopped: source is limited to 100,000 characters.', 'error');
        return;
    }
    showOutput(output, 'Starting isolated browser Python…');
    const worker = new Worker('/static/js/python-worker.js', { type: 'module', name: 'py-bite-python' });
    let timeout = setTimeout(() => {
        worker.terminate();
        showOutput(output, 'The browser Python runtime did not become ready in time. Check your connection and try again.', 'error');
    }, 60000);
    worker.onmessage = ({ data }) => {
        if (data.ready) {
            clearTimeout(timeout);
            showOutput(output, 'Running in an isolated browser worker…');
            timeout = setTimeout(() => {
                worker.terminate();
                showOutput(output, 'Stopped: execution exceeded 5 seconds.', 'error');
            }, 5000);
            return;
        }
        clearTimeout(timeout);
        worker.terminate();
        if (data.error) showOutput(output, data.error, 'error');
        else showOutput(output, data.stdout || '(No output)', 'success');
    };
    worker.onerror = () => {
        clearTimeout(timeout);
        worker.terminate();
        showOutput(output, 'The local Python runtime could not start. Reload the page and try again.', 'error');
    };
    worker.postMessage({ source });
}

function runExercise() {
    const editor = document.getElementById('code-editor');
    const output = document.getElementById('code-output');
    if (editor && output) runCode(editor.value, output);
}

function resetExercise() {
    const editor = document.getElementById('code-editor');
    const output = document.getElementById('code-output');
    if (editor) editor.value = editor.dataset.originalCode || '';
    if (output) showOutput(output, '');
}

function markComplete(lessonId, button) {
    const progress = readProgress();
    if (!progress.completedLessons.includes(lessonId)) progress.completedLessons.push(lessonId);
    saveProgress(progress);
    updateGlobalProgress();
    if (button) {
        button.textContent = 'Completed ✓';
        button.disabled = true;
        button.classList.add('btn-secondary');
        button.classList.remove('btn-primary');
    }
    const badge = document.getElementById('completion-badge');
    if (badge) {
        badge.textContent = 'Completed';
        badge.classList.remove('badge-pending');
        badge.classList.add('badge-completed');
    }
}

function submitQuiz(form) {
    const answers = new FormData(form);
    const questions = [...form.querySelectorAll('.quiz-question')];
    let score = 0;
    for (const question of questions) {
        const id = question.dataset.question;
        const type = question.dataset.answerType;
        const expected = question.dataset.answer;
        const answer = answers.get(id);
        const correct = type === 'multiple_choice' ? String(answer) === expected : String(answer).toLowerCase() === expected.toLowerCase();
        if (correct) score++;
        question.querySelectorAll('.option').forEach(option => {
            const input = option.querySelector('input');
            const optionCorrect = type === 'multiple_choice' ? input.value === expected : input.value.toLowerCase() === expected.toLowerCase();
            if (optionCorrect) option.classList.add('correct');
            else if (input.checked) option.classList.add('wrong');
        });
        const explanation = question.querySelector('.explanation');
        if (explanation) {
            explanation.textContent = question.dataset.explanation;
            explanation.classList.add('visible');
        }
    }
    const total = questions.length;
    const passed = score >= total * 0.7;
    const progress = readProgress();
    progress.quizzes[form.dataset.chapter] = { score, total, passed };
    saveProgress(progress);
    updateGlobalProgress();
    const resultBox = document.getElementById('quiz-result');
    resultBox.classList.toggle('passed', passed);
    resultBox.classList.toggle('failed', !passed);
    document.getElementById('result-title').textContent = passed ? '🎉 Quiz Passed!' : '💪 Keep Practicing';
    document.getElementById('result-message').textContent = `You scored ${score} out of ${total} (${Math.round(score / total * 100)}%). This result is saved in this browser.`;
    resultBox.classList.remove('hidden');
    resultBox.scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('click', event => {
    const action = event.target.closest('[data-action]');
    if (!action) return;
    if (action.dataset.action === 'run-example') {
        const editor = document.getElementById('code-editor');
        const output = document.getElementById('code-output');
        if (editor && output) {
            editor.value = action.dataset.code || '';
            runCode(editor.value, output);
            output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    } else if (action.dataset.action === 'run-exercise') runExercise();
    else if (action.dataset.action === 'reset-exercise') resetExercise();
    else if (action.dataset.action === 'mark-complete') markComplete(action.dataset.lesson, action);
});

document.addEventListener('DOMContentLoaded', () => {
    updateGlobalProgress();
    document.getElementById('export-progress')?.addEventListener('click', exportProgress);
    document.getElementById('import-progress')?.addEventListener('change', async event => {
        try {
            await importProgress(event.target.files[0]);
            announceStatus('Progress imported for this browser.');
        } catch (error) {
            announceStatus(error.message || 'Could not import progress.');
        } finally { event.target.value = ''; }
    });
    document.getElementById('quiz-form')?.addEventListener('submit', event => {
        event.preventDefault();
        submitQuiz(event.currentTarget);
    });
});
