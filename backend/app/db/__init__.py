from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() # Load the environment variables
import os

db_url = os.getenv("DATABASE_URL")

if not db_url: # Check if the environment variable`
    print('Environment variable MONGODB_URL not set')

client = MongoClient(db_url)
db = client['student_attendance_system'] # Database intance is created here, 
