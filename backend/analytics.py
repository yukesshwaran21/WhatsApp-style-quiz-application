from fastapi import APIRouter
from database import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# ─── DAILY ACTIVE USERS ───────────────────────────────────────────────────────
@router.get("/daily-active-users")
async def daily_active_users():
    db = get_db()
    pipeline = [
        {"$group": {"_id": {"date": "$date", "user": "$user_id"}}},
        {"$group": {"_id": "$_id.date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$limit": 30},
    ]
    result = await db.sessions.aggregate(pipeline).to_list(30)
    return [{"date": r["_id"], "users": r["count"]} for r in result]

# ─── WEEKLY ACTIVE USERS ──────────────────────────────────────────────────────
@router.get("/weekly-active-users")
async def weekly_active_users():
    db = get_db()
    now = datetime.utcnow()
    weeks = []
    for i in range(8):
        week_start = now - timedelta(weeks=i+1)
        week_end = now - timedelta(weeks=i)
        ws = week_start.date().isoformat()
        we = week_end.date().isoformat()
        pipeline = [
            {"$match": {"date": {"$gte": ws, "$lt": we}}},
            {"$group": {"_id": "$user_id"}},
            {"$count": "users"},
        ]
        res = await db.sessions.aggregate(pipeline).to_list(1)
        weeks.append({"week": f"W{8-i}", "users": res[0]["users"] if res else 0})
    weeks.reverse()
    return weeks

# ─── QUESTIONS SERVED & ANSWERED ─────────────────────────────────────────────
@router.get("/questions-stats")
async def questions_stats():
    db = get_db()
    total_served = await db.sessions.aggregate([
        {"$group": {"_id": None, "total": {"$sum": "$answered_questions"}}}
    ]).to_list(1)
    total_answered = await db.answers.count_documents({})
    total_correct = await db.answers.count_documents({"is_correct": True})

    # Daily breakdown last 14 days
    now = datetime.utcnow()
    daily = []
    for i in range(14):
        day = (now - timedelta(days=13-i)).date().isoformat()
        served = await db.answers.count_documents({"date": day})
        correct = await db.answers.count_documents({"date": day, "is_correct": True})
        daily.append({"date": day, "served": served, "correct": correct})

    return {
        "total_questions_served": total_served[0]["total"] if total_served else 0,
        "total_answered": total_answered,
        "total_correct": total_correct,
        "accuracy_rate": round(total_correct / max(total_answered, 1) * 100, 1),
        "daily": daily,
    }

# ─── AVERAGE RESPONSE TIME ────────────────────────────────────────────────────
@router.get("/avg-response-time")
async def avg_response_time():
    db = get_db()
    pipeline = [
        {"$group": {
            "_id": "$date",
            "avg_time": {"$avg": "$response_duration_seconds"},
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id": 1}},
        {"$limit": 14},
    ]
    result = await db.answers.aggregate(pipeline).to_list(14)
    overall = await db.answers.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$response_duration_seconds"}}}
    ]).to_list(1)

    return {
        "overall_avg_seconds": round(overall[0]["avg"], 1) if overall else 0,
        "daily": [{"date": r["_id"], "avg_seconds": round(r["avg_time"], 1), "count": r["count"]} for r in result],
    }

# ─── QUIZ COMPLETION RATE ─────────────────────────────────────────────────────
@router.get("/completion-rate")
async def completion_rate():
    db = get_db()
    total = await db.sessions.count_documents({})
    completed = await db.sessions.count_documents({"is_completed": True})
    rate = round(completed / max(total, 1) * 100, 1)

    # By exam
    exams = await db.exams.find().to_list(10)
    by_exam = []
    for exam in exams:
        e_total = await db.sessions.count_documents({"exam_id": str(exam["_id"])})
        e_completed = await db.sessions.count_documents({"exam_id": str(exam["_id"]), "is_completed": True})
        by_exam.append({
            "exam": exam["name"],
            "total": e_total,
            "completed": e_completed,
            "rate": round(e_completed / max(e_total, 1) * 100, 1),
        })

    return {"total": total, "completed": completed, "rate": rate, "by_exam": by_exam}

# ─── DROP-OFF ANALYSIS ────────────────────────────────────────────────────────
@router.get("/dropoff")
async def dropoff_analysis():
    db = get_db()
    sessions = await db.sessions.find({}, {"total_questions": 1, "answered_questions": 1}).to_list(500)

    buckets = {"0-25%": 0, "25-50%": 0, "50-75%": 0, "75-99%": 0, "100%": 0}
    for s in sessions:
        total = s.get("total_questions", 1)
        answered = s.get("answered_questions", 0)
        pct = answered / max(total, 1) * 100
        if pct == 100:
            buckets["100%"] += 1
        elif pct >= 75:
            buckets["75-99%"] += 1
        elif pct >= 50:
            buckets["50-75%"] += 1
        elif pct >= 25:
            buckets["25-50%"] += 1
        else:
            buckets["0-25%"] += 1

    return [{"range": k, "count": v} for k, v in buckets.items()]

# ─── PEAK ACTIVITY HOURS ──────────────────────────────────────────────────────
@router.get("/peak-hours")
async def peak_hours():
    db = get_db()
    pipeline = [
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    result = await db.answers.aggregate(pipeline).to_list(24)
    hours_map = {r["_id"]: r["count"] for r in result}
    return [{"hour": h, "count": hours_map.get(h, 0)} for h in range(24)]

# ─── AVERAGE QUESTIONS PER SESSION ───────────────────────────────────────────
@router.get("/avg-questions-per-session")
async def avg_questions_per_session():
    db = get_db()
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_questions": {"$avg": "$answered_questions"},
            "total_sessions": {"$sum": 1},
            "max_questions": {"$max": "$answered_questions"},
        }}
    ]
    result = await db.sessions.aggregate(pipeline).to_list(1)
    if not result:
        return {"avg_questions": 0, "total_sessions": 0}

    # By exam breakdown
    exams = await db.exams.find().to_list(10)
    by_exam = []
    for exam in exams:
        res = await db.sessions.aggregate([
            {"$match": {"exam_id": str(exam["_id"])}},
            {"$group": {"_id": None, "avg": {"$avg": "$answered_questions"}, "count": {"$sum": 1}}}
        ]).to_list(1)
        by_exam.append({
            "exam": exam["name"],
            "avg": round(res[0]["avg"], 1) if res else 0,
            "sessions": res[0]["count"] if res else 0,
        })

    return {
        "avg_questions": round(result[0]["avg_questions"], 1),
        "total_sessions": result[0]["total_sessions"],
        "max_in_session": result[0]["max_questions"],
        "by_exam": by_exam,
    }

# ─── OVERVIEW SUMMARY ─────────────────────────────────────────────────────────
@router.get("/overview")
async def analytics_overview():
    db = get_db()
    now = datetime.utcnow()
    today = now.date().isoformat()
    week_ago = (now - timedelta(days=7)).date().isoformat()

    total_users = await db.users.count_documents({})
    total_sessions = await db.sessions.count_documents({})
    total_answers = await db.answers.count_documents({})
    total_correct = await db.answers.count_documents({"is_correct": True})
    completed_sessions = await db.sessions.count_documents({"is_completed": True})

    dau_res = await db.sessions.aggregate([
        {"$match": {"date": today}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"},
    ]).to_list(1)

    wau_res = await db.sessions.aggregate([
        {"$match": {"date": {"$gte": week_ago}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"},
    ]).to_list(1)

    avg_rt = await db.answers.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$response_duration_seconds"}}}
    ]).to_list(1)

    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_questions_served": total_answers,
        "total_correct": total_correct,
        "accuracy_rate": round(total_correct / max(total_answers, 1) * 100, 1),
        "completion_rate": round(completed_sessions / max(total_sessions, 1) * 100, 1),
        "daily_active_users": dau_res[0]["count"] if dau_res else 0,
        "weekly_active_users": wau_res[0]["count"] if wau_res else 0,
        "avg_response_time_seconds": round(avg_rt[0]["avg"], 1) if avg_rt else 0,
    }
