from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://yukesshwaran8:Yukessh8072.@cluster0.urf10sa.mongodb.net/?appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "quizapp")

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print(f"[OK] Connected to MongoDB: {DATABASE_NAME}")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("[CLOSED] MongoDB connection closed")

def get_db():
    return db
