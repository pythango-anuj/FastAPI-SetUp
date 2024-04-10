from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.env import MONGO_URI
from app.models.user import User
from app.models.task_workflow import Task, TaskRun, WorkFlow, WorkflowRun

# Database Configuration
client = AsyncIOMotorClient(MONGO_URI)
database = client.get_database()

# List of document models to register with db
document_models = [
    User,
    Task,
    TaskRun,
    WorkFlow,
    WorkflowRun
]

# Initialize Beanie
async def init_db():
    try:
        await init_beanie(database=database, document_models=document_models)
        print("Beanie initialized successfully.")
    except Exception as e:
        print(f"Error initializing Beanie: {e}")


# Get database instance
def get_db():
    return database
