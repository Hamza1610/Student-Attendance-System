import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv 
import os
load_dotenv()
# Path to your service account key file
SERVICE_ACCOUNT_PATH =os.environ.get('FIREBASE_ADMIN_PATH')


def initalize_firebase_admin():

    if not SERVICE_ACCOUNT_PATH:
        raise ValueError("No FIREBASE_ADMIN_PATH set for firebase admin sdk")

    print(SERVICE_ACCOUNT_PATH)
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)