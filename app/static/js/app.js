// ===== Global Progress =====
async function updateGlobalProgress() {
    try {
        const res = await fetch('/api/progress');
        const data = await res.json();
        const pct = data.total_lessons ? Math.round(data.completed_lessons / data.total_lessons * 100) : 0;
        const fill = document.getElementById('global-progress-fill');
        const text = document.getElementById('global-progress-text');
        if (fill) fill.style.width = pct + '%';
        if (text) text.textContent = pct + '% complete';
    } catch (e) {
        console.error('Failed to load progress', e);
    }
}

updateGlobalProgress();

// ===== Run Code =====
async function runCode(source, outputEl) {
    outputEl.textContent = 'Running...';
    outputEl.className = 'code-output';

    try {
        const res = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: source, mode: 'full' })
        });
        const data = await res.json();

        if (data.success) {
            outputEl.classList.add('success');
            outputEl.textContent = data.stdout || '(No output)';
        } else {
            outputEl.classList.add('error');
            outputEl.textContent = data.stderr || data.stdout || '(Execution failed)';
        }
    } catch (e) {
        outputEl.classList.add('error');
        outputEl.textContent = 'Network error: ' + e.message;
    }
}

function runExercise() {
    const editor = document.getElementById('code-editor');
    const output = document.getElementById('code-output');
    if (!editor || !output) return;
    runCode(editor.value, output);
}

function resetExercise() {
    const editor = document.getElementById('code-editor');
    if (!editor) return;
    if (typeof ORIGINAL_CODE !== 'undefined') {
        editor.value = ORIGINAL_CODE;
    }
    const output = document.getElementById('code-output');
    if (output) {
        output.textContent = '';
        output.className = 'code-output';
    }
}

function runInEditor(btn) {
    const source = btn.dataset.code;
    const editor = document.getElementById('code-editor');
    const output = document.getElementById('code-output');
    if (editor && source) {
        editor.value = source;
    }
    if (output) {
        runCode(source, output);
        output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// ===== Mark Lesson Complete =====
async function markComplete(lessonId) {
    try {
        const res = await fetch(`/api/progress/lesson/${lessonId}`, { method: 'POST' });
        const data = await res.json();
        if (data.completed) {
            const btn = document.getElementById('mark-complete-btn');
            if (btn) {
                btn.textContent = 'Completed ✓';
                btn.disabled = true;
                btn.classList.add('btn-secondary');
                btn.classList.remove('btn-primary');
            }
            const badge = document.getElementById('completion-badge');
            if (badge) {
                badge.textContent = 'Completed';
                badge.classList.remove('badge-pending');
                badge.classList.add('badge-completed');
            }
            updateGlobalProgress();
        }
    } catch (e) {
        console.error('Failed to mark complete', e);
    }
}

// ===== Quiz =====
document.addEventListener('DOMContentLoaded', () => {
    const quizForm = document.getElementById('quiz-form');
    if (!quizForm) return;

    quizForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const chapterId = quizForm.dataset.chapter;
        const formData = new FormData(quizForm);
        const answers = {};
        for (const [key, value] of formData.entries()) {
            answers[key] = value;
        }

        try {
            const res = await fetch(`/api/quiz/${chapterId}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(answers)
            });
            const data = await res.json();

            // Show explanations and highlight answers
            const questions = quizForm.querySelectorAll('.quiz-question');
            questions.forEach(qEl => {
                const qid = qEl.dataset.question;
                const meta = QUIZ_ANSWERS[qid];
                if (!meta) return;
                const explanation = qEl.querySelector('.explanation');
                const options = qEl.querySelectorAll('.option');
                const userVal = answers[qid];

                options.forEach((opt, idx) => {
                    const input = opt.querySelector('input');
                    let isCorrect = false;
                    if (meta.type === 'multiple_choice') {
                        isCorrect = idx === meta.answer;
                    } else if (meta.type === 'true_false') {
                        const boolAnswer = String(meta.answer).toLowerCase() === 'true';
                        const boolUser = String(userVal).toLowerCase() === 'true';
                        isCorrect = (input.value === 'true') === boolAnswer;
                    }
                    if (isCorrect) {
                        opt.classList.add('correct');
                    } else if (input.checked) {
                        opt.classList.add('wrong');
                    }
                });

                if (explanation) {
                    explanation.textContent = meta.explanation;
                    explanation.classList.add('visible');
                }
            });

            const resultBox = document.getElementById('quiz-result');
            const resultTitle = document.getElementById('result-title');
            const resultMessage = document.getElementById('result-message');

            if (data.passed) {
                resultBox.classList.add('passed');
                resultBox.classList.remove('failed');
                resultTitle.textContent = '🎉 Quiz Passed!';
            } else {
                resultBox.classList.add('failed');
                resultBox.classList.remove('passed');
                resultTitle.textContent = '💪 Keep Practicing';
            }
            resultMessage.textContent = `You scored ${data.score} out of ${data.total} (${data.percentage}%).`;
            resultBox.classList.remove('hidden');
            resultBox.scrollIntoView({ behavior: 'smooth' });
            updateGlobalProgress();
        } catch (err) {
            alert('Failed to submit quiz: ' + err.message);
        }
    });
});
