# katakita/models.py
from .extensions import db
from sqlalchemy import Time, Date, UniqueConstraint
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    whatsapp_number = db.Column(db.String(20), unique=True, nullable=True)
    telegram_chat_id = db.Column(db.String(50), unique=True, nullable=True)
    pref_jenis = db.Column(db.String(50), default='semangat')
    pref_gaya = db.Column(db.String(50), default='santai')
    send_time = db.Column(Time, nullable=True)

    def __repr__(self):
        return f'<User {self.nama}>'

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Setting {self.key}>'

class DailyQuote(db.Model):
    __tablename__ = 'daily_quotes'
    id = db.Column(db.Integer, primary_key=True)
    teks = db.Column(db.Text, nullable=False)
    penulis = db.Column(db.String(255), nullable=False)
    jenis = db.Column(db.String(50), nullable=False)
    gaya_bahasa = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(Date, nullable=False, default=datetime.date.today)
    __table_args__ = (UniqueConstraint('tanggal', 'jenis', 'gaya_bahasa', name='_tanggal_jenis_gaya_uc'),)

    def __repr__(self):
        return f'<DailyQuote {self.tanggal} - {self.jenis}/{self.gaya_bahasa}>'