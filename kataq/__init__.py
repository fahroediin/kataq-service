# kataq/__init__.py
from flask import Flask
from config import Config
from .extensions import db
from .admin import init_admin
from .services.gemini_service import configure_gemini

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi
    db.init_app(app)
    init_admin(app)
        
    # Konfigurasi API Key Gemini saat aplikasi dibuat
    try:
        configure_gemini()
    except ValueError as e:
        print(f"PERINGATAN: {e}")
        print("Fungsi generator quote tidak akan bekerja.")

    return app