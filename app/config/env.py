from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variable
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017/")
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID","")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET","")
SECRET_KEY = os.getenv("SECRET_KEY", "=i!%%1!pzk8mukf$o$e%*%=5lg(hhb=8tbwfq$=4=!qa$&cqp$")
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")