from flask import Blueprint, render_template
from .content import CHAPTERS, get_chapter, get_lesson, get_resource
from .quizzes import get_quiz
from .progress_tracker import is_lesson_complete, get_progress_summary

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html", chapters=CHAPTERS, summary=get_progress_summary(CHAPTERS))


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
