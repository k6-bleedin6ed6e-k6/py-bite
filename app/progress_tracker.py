import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")


def _load() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def mark_lesson_complete(lesson_id: str):
    data = _load()
    if "completed_lessons" not in data:
        data["completed_lessons"] = []
    if lesson_id not in data["completed_lessons"]:
        data["completed_lessons"].append(lesson_id)
    _save(data)


def is_lesson_complete(lesson_id: str) -> bool:
    data = _load()
    return lesson_id in data.get("completed_lessons", [])


def save_quiz_result(chapter_id: str, score: int, total: int):
    data = _load()
    if "quiz_results" not in data:
        data["quiz_results"] = {}
    data["quiz_results"][chapter_id] = {
        "score": score,
        "total": total,
        "passed": score >= total * 0.7
    }
    _save(data)


def get_quiz_result(chapter_id: str) -> dict:
    data = _load()
    return data.get("quiz_results", {}).get(chapter_id, {})


def get_progress_summary(chapters: list) -> dict:
    data = _load()
    completed = set(data.get("completed_lessons", []))
    quiz_results = data.get("quiz_results", {})

    summary = {
        "total_lessons": 0,
        "completed_lessons": 0,
        "chapters": []
    }

    for ch in chapters:
        ch_total = len(ch["lessons"])
        ch_done = sum(1 for l in ch["lessons"] if l["id"] in completed)
        quiz = quiz_results.get(ch["id"], {})
        summary["total_lessons"] += ch_total
        summary["completed_lessons"] += ch_done
        summary["chapters"].append({
            "id": ch["id"],
            "title": ch["title"],
            "number": ch["number"],
            "total_lessons": ch_total,
            "completed_lessons": ch_done,
            "quiz_passed": quiz.get("passed", False),
            "quiz_score": quiz.get("score", 0),
            "quiz_total": quiz.get("total", 0),
        })

    return summary
