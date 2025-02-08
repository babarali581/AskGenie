import google.generativeai as genai
import os
from firebase_admin import credentials, firestore
import firebase_admin
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
GCP_KEY_PATH = os.getenv("GCP_KEY_PATH")

genai.configure(api_key=API_KEY)

cred = credentials.Certificate(GCP_KEY_PATH)
firebase_admin.initialize_app(cred)

model = genai.GenerativeModel(model_name=MODEL)
db = firestore.client()