# kataq/admin.py
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField  # <-- 1. IMPORT SelectField
from .extensions import db, admin
from .models import User, Setting, DailyQuote

# Pilihan dropdown untuk form admin
JENIS_CHOICES = ['semangat', 'romantis', 'sedih', 'bahagia', 'keluarga', 'sahabat']
GAYA_CHOICES = ['santai', 'serius', 'formal', 'sarkas', 'satire', 'humor']

class UserAdminView(ModelView):
    column_list = ('nama', 'email', 'whatsapp_number', 'telegram_chat_id', 'pref_jenis', 'pref_gaya', 'send_time')
    form_columns = ('nama', 'email', 'whatsapp_number', 'telegram_chat_id', 'pref_jenis', 'pref_gaya', 'send_time')

    # --- 2. TAMBAHKAN form_overrides ---
    # Memberitahu Flask-Admin untuk menggunakan SelectField untuk kolom-kolom ini
    form_overrides = {
        'pref_jenis': SelectField,
        'pref_gaya': SelectField
    }

    # --- 3. form_args SEKARANG AKAN BEKERJA DENGAN BENAR ---
    # Karena field-nya sudah menjadi SelectField, ia akan menerima 'choices'
    form_args = {
        'pref_jenis': {
            'label': 'Jenis Quote',  # Menambahkan label agar lebih jelas
            'choices': JENIS_CHOICES
        },
        'pref_gaya': {
            'label': 'Gaya Bahasa', # Menambahkan label agar lebih jelas
            'choices': GAYA_CHOICES
        }
    }

class SettingAdminView(ModelView):
    can_create = False
    can_delete = False

class DailyQuoteAdminView(ModelView):
    can_create = False
    column_filters = ('tanggal', 'jenis', 'gaya_bahasa')
    column_list = ('tanggal', 'jenis', 'gaya_bahasa', 'teks', 'penulis')

def init_admin(app):
    admin.init_app(app)
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(SettingAdminView(Setting, db.session))
    admin.add_view(DailyQuoteAdminView(DailyQuote, db.session, name="Generated Quotes"))
