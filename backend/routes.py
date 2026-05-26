from fastapi import APIRouter, HTTPException
from database import get_db
from bson import ObjectId

router = APIRouter(prefix="/api", tags=["quiz"])

def serialize(doc):
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

def serialize_list(docs):
    return [serialize(d) for d in docs]

# ─── EXAMS ───────────────────────────────────────────────────────────────────
@router.get("/exams")
async def get_exams():
    db = get_db()
    exams = await db.exams.find().to_list(100)
    return serialize_list(exams)

# ─── SUBJECTS ────────────────────────────────────────────────────────────────
@router.get("/subjects/{exam_id}")
async def get_subjects(exam_id: str):
    db = get_db()
    subjects = await db.subjects.find({"exam_id": exam_id}).to_list(100)
    return serialize_list(subjects)

# ─── CHAPTERS ────────────────────────────────────────────────────────────────
@router.get("/chapters/{subject_id}")
async def get_chapters(subject_id: str):
    db = get_db()
    chapters = await db.chapters.find({"subject_id": subject_id}).to_list(100)
    return serialize_list(chapters)

# ─── START QUIZ SESSION ───────────────────────────────────────────────────────
@router.post("/session/start")
async def start_session(data: dict):
    db = get_db()
    from datetime import datetime
    user_id = data.get("user_id")
    chapter_id = data.get("chapter_id")
    subject_id = data.get("subject_id")
    exam_id = data.get("exam_id")

    # Fetch questions for this chapter
    questions = await db.questions.find({"chapter_id": chapter_id}).to_list(50)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this chapter")

    import random
    random.shuffle(questions)

    session = {
        "_id": ObjectId(),
        "user_id": user_id,
        "exam_id": exam_id,
        "subject_id": subject_id,
        "chapter_id": chapter_id,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "is_completed": False,
        "total_questions": len(questions),
        "answered_questions": 0,
        "score": 0,
        "question_ids": [str(q["_id"]) for q in questions],
        "date": datetime.utcnow().date().isoformat(),
        "hour": datetime.utcnow().hour,
    }
    result = await db.sessions.insert_one(session)

    # Return session + first question
    first_q = serialize(questions[0])
    return {
        "session_id": str(result.inserted_id),
        "total_questions": len(questions),
        "question": first_q,
        "question_index": 0,
    }

# ─── SUBMIT ANSWER ────────────────────────────────────────────────────────────
@router.post("/session/answer")
async def submit_answer(data: dict):
    db = get_db()
    from datetime import datetime

    session_id = data.get("session_id")
    question_id = data.get("question_id")
    selected_option = data.get("selected_option")
    question_shown_at = data.get("question_shown_at")
    answer_submitted_at = data.get("answer_submitted_at")

    if question_shown_at and isinstance(question_shown_at, str):
        question_shown_at = datetime.fromisoformat(question_shown_at.replace("Z", "+00:00"))
    if answer_submitted_at and isinstance(answer_submitted_at, str):
        answer_submitted_at = datetime.fromisoformat(answer_submitted_at.replace("Z", "+00:00"))

    # Get session
    session = await db.sessions.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get question
    question = await db.questions.find_one({"_id": ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = selected_option == question["correct_option"]
    if question_shown_at and answer_submitted_at:
        response_duration = (answer_submitted_at - question_shown_at).total_seconds()
    else:
        response_duration = 30

    now = datetime.utcnow()

    # Store answer
    answer_doc = {
        "_id": ObjectId(),
        "session_id": session_id,
        "question_id": question_id,
        "user_id": session["user_id"],
        "selected_option": selected_option,
        "is_correct": is_correct,
        "question_shown_at": question_shown_at or now,
        "answer_submitted_at": answer_submitted_at or now,
        "response_duration_seconds": max(0, response_duration),
        "date": now.date().isoformat(),
        "hour": now.hour,
    }
    await db.answers.insert_one(answer_doc)

    # Update session
    score_inc = 1 if is_correct else 0
    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$inc": {"answered_questions": 1, "score": score_inc}}
    )

    # Get next question
    question_ids = session.get("question_ids", [])
    answered_count = session["answered_questions"] + 1
    next_question = None
    if answered_count < len(question_ids):
        next_q_id = question_ids[answered_count]
        next_q = await db.questions.find_one({"_id": ObjectId(next_q_id)})
        next_question = serialize(next_q) if next_q else None

    return {
        "is_correct": is_correct,
        "correct_option": question["correct_option"],
        "explanation": question.get("explanation", ""),
        "next_question": next_question,
        "question_index": answered_count,
        "total_questions": len(question_ids),
    }

# ─── FINISH SESSION ───────────────────────────────────────────────────────────
@router.post("/session/finish")
async def finish_session(data: dict):
    db = get_db()
    from datetime import datetime
    session_id = data.get("session_id")

    session = await db.sessions.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"is_completed": True, "completed_at": datetime.utcnow()}}
    )

    updated = await db.sessions.find_one({"_id": ObjectId(session_id)})
    return {
        "session_id": session_id,
        "score": updated["score"],
        "total_questions": updated["total_questions"],
        "answered_questions": updated["answered_questions"],
        "percentage": round(updated["score"] / max(updated["total_questions"], 1) * 100, 1),
    }

# ─── GET USERS (for selection) ────────────────────────────────────────────────
@router.get("/users")
async def get_users():
    db = get_db()
    users = await db.users.find().to_list(50)
    return serialize_list(users)
