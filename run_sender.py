# run_sender.py
from apscheduler.schedulers.blocking import BlockingScheduler
from kataq import create_app
from kataq.extensions import db
from kataq.models import User, Setting, DailyQuote
from kataq.services import delivery_service
import datetime

app = create_app()

def job_kirim_quote():
    with app.app_context():
        now = datetime.datetime.now().time().replace(second=0, microsecond=0)
        today = datetime.date.today()
        
        global_setting = Setting.query.filter_by(key='global_send_time').first()
        if not global_setting: return
        
        global_time = datetime.datetime.strptime(global_setting.value, '%H:%M:%S').time()

        users_to_send = User.query.filter(
            (User.send_time == now) |
            ((User.send_time == None) & (global_time == now))
        ).all()

        if not users_to_send: return
        
        print(f"[{datetime.datetime.now()}] Menemukan {len(users_to_send)} user untuk dikirimi quote.")
        for user in users_to_send:
            quote = DailyQuote.query.filter_by(
                tanggal=today, jenis=user.pref_jenis, gaya_bahasa=user.pref_gaya
            ).first()
            
            if quote:
                pesan = f"Quote harian untukmu, {user.nama}!\n\n\"{quote.teks}\"\n- {quote.penulis}"
                
                # --- BLOK EMAIL DIHAPUS DARI SINI ---

                if user.whatsapp_number:
                    delivery_service.send_whatsapp(user.whatsapp_number, pesan)
                if user.telegram_chat_id:
                    delivery_service.send_telegram(user.telegram_chat_id, pesan)
            else:
                print(f"GAGAL: Quote untuk {user.pref_jenis}/{user.pref_gaya} tanggal {today} tidak ditemukan.")

scheduler = BlockingScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_kirim_quote, 'interval', minutes=1)

print("Scheduler Pengiriman dimulai... Berjalan setiap menit.")
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass