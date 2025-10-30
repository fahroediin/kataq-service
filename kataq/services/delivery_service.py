# kataq/services/delivery_service.py
import requests
from flask import current_app

def send_whatsapp(to_number, body):
    """
    Mengirim permintaan ke layanan Node.js untuk mengirim pesan WhatsApp.
    """
    sender_url = current_app.config.get('WHATSAPP_SENDER_URL')
    if not sender_url:
        print("ERROR: WHATSAPP_SENDER_URL tidak diatur di konfigurasi.")
        return

    # Pastikan nomor dimulai dengan 62 dan bukan 0 untuk konsistensi
    if to_number.startswith('0'):
        to_number = '62' + to_number[1:]

    payload = {
        "number": to_number,
        "message": body
    }

    try:
        # Timeout 20 detik untuk memberi waktu pada whatsapp-web.js
        response = requests.post(sender_url, json=payload, timeout=20)
        if response.status_code == 200:
            print(f"Permintaan pengiriman WhatsApp ke {to_number} berhasil dikirim ke sender service.")
        else:
            print(f"Gagal mengirim permintaan ke sender service: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Tidak dapat terhubung ke WhatsApp sender service: {e}")

def send_telegram(chat_id, body):
    """
    Mengirim pesan ke Telegram Bot. (Fungsi ini tidak berubah)
    """
    token = current_app.config['TELEGRAM_BOT_TOKEN']
    if not token:
        print("ERROR: Token Telegram Bot tidak ditemukan. Pengiriman Telegram dilewati.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": body,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        if response_data.get("ok"):
            print(f"Pesan Telegram berhasil dikirim ke chat_id {chat_id}")
        else:
            print(f"Gagal mengirim Telegram: {response_data.get('description')}")
    except Exception as e:
        print(f"Gagal mengirim Telegram ke {chat_id}: {e}")