# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

    # Mengatur tema untuk Flask-Admin
    FLASK_ADMIN_SWATCH = 'cerulean'

    # --- KONFIGURASI BARU ---
    # URL untuk layanan Node.js WhatsApp Sender
    WHATSAPP_SENDER_URL = 'http://localhost:3000/send-message'

    # Konfigurasi Telegram (tetap sama)
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')