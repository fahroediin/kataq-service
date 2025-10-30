# run_generator.py
from apscheduler.schedulers.blocking import BlockingScheduler
from kataq import create_app
from kataq.extensions import db
from kataq.models import DailyQuote
from kataq.services.gemini_service import generate_quote_with_gemini
from kataq.admin import JENIS_CHOICES, GAYA_CHOICES
from datetime import date
import time

app = create_app()

def populate_quotes_for_today():
    """
    Fungsi utama untuk mengisi database dengan quote harian.
    """
    today = date.today()
    print(f"--- Memulai proses pembuatan quote untuk tanggal: {today} ---")

    with app.app_context():
        for jenis in JENIS_CHOICES:
            for gaya in GAYA_CHOICES:
                exists = DailyQuote.query.filter_by(tanggal=today, jenis=jenis, gaya_bahasa=gaya).first()
                if exists:
                    print(f"[*] Quote untuk [{jenis}/{gaya}] sudah ada. Dilewati.")
                    continue

                print(f"[+] Membuat quote untuk [{jenis}/{gaya}]...")
                quote_data = generate_quote_with_gemini(jenis, gaya)

                if quote_data:
                    new_quote = DailyQuote(
                        teks=quote_data['teks'], penulis=quote_data['penulis'],
                        jenis=jenis, gaya_bahasa=gaya, tanggal=today
                    )
                    db.session.add(new_quote)
                    db.session.commit()
                    print(f"    -> Berhasil disimpan.")
                else:
                    print(f"    -> GAGAL membuat quote untuk [{jenis}/{gaya}].")
                time.sleep(2)
    print("--- Proses pembuatan quote selesai. ---")


# --- PERUBAHAN UTAMA DI SINI ---
# Blok ini hanya akan dieksekusi jika Anda menjalankan "python run_generator.py"
if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Jakarta")
    
    # Menjalankan job setiap hari pada jam 01:00 pagi
    scheduler.add_job(populate_quotes_for_today, 'cron', hour=1, minute=0)
    
    print("Generator Harian dimulai... Akan berjalan setiap jam 1 pagi.")
    print("Untuk menjalankan generator secara manual sekali, gunakan perintah:")
    print('python -c "from run_generator import populate_quotes_for_today; populate_quotes_for_today()"')
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass