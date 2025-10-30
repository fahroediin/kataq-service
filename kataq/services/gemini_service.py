# kataq/services/gemini_service.py
import google.generativeai as genai
import os
import json

def configure_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY tidak ditemukan di environment variables.")
    genai.configure(api_key=api_key)

def generate_quote_with_gemini(jenis: str, gaya: str) -> dict | None:
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Buatkan saya satu kutipan (quote) orisinal yang unik.
        Spesifikasi:
        - Tema: {jenis}
        - Gaya bahasa: {gaya}
        - Penulis: Buat nama penulis fiktif yang sesuai, atau "Anonim".
        Format output harus dalam bentuk JSON yang valid seperti ini, tanpa teks tambahan:
        {{
            "teks": "Isi kutipan di sini.",
            "penulis": "Nama penulis fiktif di sini."
        }}
        """
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        quote_data = json.loads(cleaned_response)
            
        if "teks" in quote_data and "penulis" in quote_data:
            return quote_data
        return None
    
    except Exception as e:
        print(f"Error saat generate quote dengan Gemini: {e}")
        return None