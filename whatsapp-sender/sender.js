// sender.js
const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

const port = 3000;

console.log('Menginisialisasi WhatsApp Client...');

// Menggunakan LocalAuth untuk menyimpan sesi dan menghindari scan berulang
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Event untuk menampilkan QR Code di terminal saat pertama kali dijalankan
client.on('qr', qr => {
    console.log('================================================');
    console.log('Pindai QR Code ini dengan aplikasi WhatsApp Anda:');
    qrcode.generate(qr, { small: true });
    console.log('================================================');
});

// Event saat client berhasil terhubung dan siap
client.on('ready', () => {
    console.log('✅ WhatsApp Client siap digunakan!');
});

// Event jika otentikasi gagal
client.on('auth_failure', msg => {
    console.error('❌ Gagal Otentikasi!', msg);
    process.exit(1); // Keluar dari aplikasi jika sesi tidak valid
});

client.initialize();

// Endpoint API untuk menerima permintaan pengiriman pesan dari layanan Python
app.post('/send-message', async (req, res) => {
    const { number, message } = req.body;

    if (!number || !message) {
        return res.status(400).json({ success: false, error: 'Nomor dan pesan diperlukan.' });
    }

    // Format nomor ke format ID WhatsApp (contoh: 6281... -> 6281...@c.us)
    const chatId = `${number}@c.us`;

    try {
        await client.sendMessage(chatId, message);
        console.log(`Pesan berhasil dikirim ke ${number}`);
        res.status(200).json({ success: true, message: 'Pesan berhasil dikirim.' });
    } catch (error) {
        console.error(`Gagal mengirim pesan ke ${number}:`, error.message);
        res.status(500).json({ success: false, error: 'Gagal mengirim pesan. Pastikan nomor valid dan terdaftar di WhatsApp.' });
    }
});

app.listen(port, () => {
    console.log(`WhatsApp Sender Service berjalan di http://localhost:${port}`);
});