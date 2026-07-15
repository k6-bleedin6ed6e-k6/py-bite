from flask import Blueprint, render_template, jsonify, request
from .content import CHAPTERS, get_chapter, get_lesson, get_resource
from .quizzes import get_quiz
from .progress_tracker import (
    mark_lesson_complete,
    is_lesson_complete,
    save_quiz_result,
    get_progress_summary,
)
from .code_runner import run_code

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    summary = get_progress_summary(CHAPTERS)
    return render_template("index.html", chapters=CHAPTERS, summary=summary)


@bp.route("/chapter/<chapter_id>")
def chapter(chapter_id):
    ch = get_chapter(chapter_id)
    if not ch:
        return "Chapter not found", 404
    return render_template("chapter.html", chapter=ch)


@bp.route("/lesson/<lesson_id>")
def lesson(lesson_id):
    lesson_data, ch = get_lesson(lesson_id)
    if not lesson_data:
        return "Lesson not found", 404
    completed = is_lesson_complete(lesson_id)
    return render_template("lesson.html", lesson=lesson_data, chapter=ch, completed=completed)


@bp.route("/resource/<slug>")
def resource(slug):
    res = get_resource(slug)
    if not res:
        return "Resource not found", 404
    return render_template("resource.html", resource=res)


@bp.route("/quiz/<chapter_id>")
def quiz(chapter_id):
    quiz_data = get_quiz(chapter_id)
    ch = get_chapter(chapter_id)
    if not quiz_data or not ch:
        return "Quiz not found", 404
    return render_template("quiz.html", quiz=quiz_data, chapter=ch)


@bp.route("/api/progress/lesson/<lesson_id>", methods=["POST"])
def api_mark_lesson(lesson_id):
    mark_lesson_complete(lesson_id)
    return jsonify({"status": "ok", "completed": True})


@bp.route("/api/progress")
def api_progress():
    return jsonify(get_progress_summary(CHAPTERS))


@bp.route("/api/quiz/<chapter_id>/submit", methods=["POST"])
def api_submit_quiz(chapter_id):
    quiz_data = get_quiz(chapter_id)
    if not quiz_data:
        return jsonify({"error": "Quiz not found"}), 404

    answers = request.get_json(force=True)
    score = 0
    total = len(quiz_data["questions"])

    for q in quiz_data["questions"]:
        qid = q["id"]
        user_answer = answers.get(qid)
        if q["type"] == "multiple_choice":
            try:
                if int(user_answer) == q["answer"]:
                    score += 1
            except (ValueError, TypeError):
                pass
        elif q["type"] == "true_false":
            if str(user_answer).lower() == str(q["answer"]).lower():
                score += 1

    save_quiz_result(chapter_id, score, total)
    passed = score >= total * 0.7

    return jsonify({
        "score": score,
        "total": total,
        "passed": passed,
        "percentage": round(score / total * 100, 1)
    })


@bp.route("/api/run", methods=["POST"])
def api_run_code():
    data = request.get_json(force=True)
    source = data.get("code", "")
    mode = data.get("mode", "full")
    result = run_code(source, mode=mode)
    return jsonify(result)
