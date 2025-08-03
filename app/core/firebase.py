import firebase_admin
from firebase_admin import credentials
from app.core.config import settings
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_firebase():
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    logger.info(f"Attempting to initialize Firebase with credentials file: {cred_path}")
    
    if not os.path.exists(cred_path):
        logger.error(f"Firebase credentials file not found at: {cred_path}")
        return

    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")

