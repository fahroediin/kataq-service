# init_db.py
from kataq import create_app
from kataq.extensions import db
from kataq.models import Setting
import datetime

app = create_app()

with app.app_context():
    print("Membuat semua tabel database...")
    db.create_all()
    print("Tabel berhasil dibuat.")

    # Buat setting global jika belum ada
    if not Setting.query.filter_by(key='global_send_time').first():
        print("Membuat setting default 'global_send_time'...")
        default_time = datetime.time(7, 0).strftime('%H:%M:%S')
        new_setting = Setting(key='global_send_time', value=default_time)
        db.session.add(new_setting)
        db.session.commit()
        print("Setting default berhasil dibuat (07:00).")
    else:
        print("Setting 'global_send_time' sudah ada.")