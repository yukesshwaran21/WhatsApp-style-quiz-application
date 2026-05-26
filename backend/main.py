from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection, get_db
from routes import router as quiz_router
from analytics import router as analytics_router
from seed_data import generate_dummy_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    db = get_db()

    # Seed data if collections are empty
    exam_count = await db.exams.count_documents({})
    if exam_count == 0:
        print("[SEED] Seeding database with dummy data...")
        data = generate_dummy_data(db)
        if data["exams"]:
            await db.exams.insert_many(data["exams"])
        if data["subjects"]:
            await db.subjects.insert_many(data["subjects"])
        if data["chapters"]:
            await db.chapters.insert_many(data["chapters"])
        if data["questions"]:
            await db.questions.insert_many(data["questions"])
        if data["users"]:
            await db.users.insert_many(data["users"])
        if data["sessions"]:
            await db.sessions.insert_many(data["sessions"])
        if data["answers"]:
            await db.answers.insert_many(data["answers"])
        print(f"[OK] Seeded: {len(data['exams'])} exams, {len(data['subjects'])} subjects, "
              f"{len(data['chapters'])} chapters, {len(data['questions'])} questions, "
              f"{len(data['users'])} users, {len(data['sessions'])} sessions, "
              f"{len(data['answers'])} answers")
    else:
        print(f"[OK] Database already has data ({exam_count} exams). Skipping seed.")

    yield
    await close_mongo_connection()

app = FastAPI(
    title="WhatsApp Quiz API",
    description="Quiz application with analytics",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router)
app.include_router(analytics_router)

@app.get("/")
async def root():
    return {"message": "WhatsApp Quiz API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
