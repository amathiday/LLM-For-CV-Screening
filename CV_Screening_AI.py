#CV-Screening
import google.generativeai as genai
import pandas as pd
import json
import time
import os
import PyPDF2 # Pastikan sudah install: pip install PyPDF2

# Konfigurasi API - API Key akan diisi otomatis oleh environment saat dijalankan
api_key = ""
genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    """Mengekstrak teks dari file PDF."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Gagal membaca file {pdf_path}: {e}")
    return text

def call_gemini_with_retry(prompt, system_instruction, retries=5):
    """Memanggil Gemini API dengan implementasi Exponential Backoff."""
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-09-2025",
        system_instruction=system_instruction
    )
    
    for i in range(retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                }
            )
            return response.text
        except Exception as e:
            if i < retries - 1:
                wait_time = 2**i
                time.sleep(wait_time)
            else:
                print(f"Gagal setelah {retries} percobaan: {str(e)}")
                return None

def process_cv_screening():
    # 1. Definisi Requirement HR yang lebih detail
    hr_requirements = """
    Posisi: Senior Sales Representative
    Kriteria Utama Penilaian:
    1. Pengalaman FMCG (Bobot: 30%): Minimal 3 tahun di industri barang konsumsi.
    2. Pencapaian Target (Bobot: 40%): Bukti angka pencapaian target di atas 100%.
    3. Skill Teknis/CRM (Bobot: 15%): Penguasaan Salesforce, Hubspot, atau alat CRM lainnya.
    4. Soft Skills & Bahasa (Bobot: 15%): Negosiasi, Komunikasi, dan Bahasa Inggris.
    """

    # 2. Deteksi File PDF
    current_dir = "."
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("Tidak ditemukan file PDF di folder ini.")
        return

    # 3. System Instruction yang lebih komprehensif
    system_prompt = f"""
    Anda adalah sistem ATS (Applicant Tracking System) cerdas. Tugas Anda adalah:
    1. Ekstrak SEMUA informasi dari teks CV (Nama, Kontak, Pendidikan, Ringkasan Pengalaman).
    2. Berikan penilaian DETAIL untuk setiap kategori berikut sesuai kriteria sales:
       - Pengalaman FMCG
       - Pencapaian Target/Sales Record
       - Penguasaan CRM & Teknologi
       - Komunikasi & Bahasa
    3. Untuk setiap kategori, berikan 'Skor' (0-100) dan 'Ringkasan Alasan'.
    
    Output HARUS dalam format JSON dengan struktur:
    {{
        "informasi_kandidat": {{
            "nama": "string",
            "pendidikan": "string",
            "kontak": "string",
            "total_tahun_pengalaman": "string",
            "ringkasan_profil": "string"
        }},
        "penilaian_kategori": {{
            "fmcg_experience": {{ "skor": 0, "ringkasan": "string" }},
            "sales_achievement": {{ "skor": 0, "ringkasan": "string" }},
            "crm_tech_skills": {{ "skor": 0, "ringkasan": "string" }},
            "comm_language_skills": {{ "skor": 0, "ringkasan": "string" }}
        }},
        "skor_kesesuaian_total": 0,
        "rekomendasi_akhir": "Lanjut / Cadangan / Tolak"
    }}
    """

    all_data_rows = []

    print(f"Ditemukan {len(pdf_files)} file. Memulai analisis mendalam...")

    for filename in pdf_files:
        print(f"Menganalisis: {filename}...")
        cv_text = extract_text_from_pdf(filename)
        
        if not cv_text.strip():
            continue

        raw_response = call_gemini_with_retry(f"Analisis CV ini: {cv_text}", system_prompt)
        
        if raw_response:
            try:
                data = json.loads(raw_response)
                
                # Flattening JSON untuk kebutuhan Tabel Excel
                row = {
                    "File Source": filename,
                    "Nama Kandidat": data['informasi_kandidat']['nama'],
                    "Pendidikan": data['informasi_kandidat']['pendidikan'],
                    "Kontak": data['informasi_kandidat']['kontak'],
                    "Total Exp (Tahun)": data['informasi_kandidat']['total_tahun_pengalaman'],
                    "Ringkasan Profil": data['informasi_kandidat']['ringkasan_profil'],
                    
                    # Kolom Penilaian & Skor
                    "Skor FMCG": data['penilaian_kategori']['fmcg_experience']['skor'],
                    "Alasan FMCG": data['penilaian_kategori']['fmcg_experience']['ringkasan'],
                    
                    "Skor Sales Record": data['penilaian_kategori']['sales_achievement']['skor'],
                    "Alasan Sales Record": data['penilaian_kategori']['sales_achievement']['ringkasan'],
                    
                    "Skor CRM/Tech": data['penilaian_kategori']['crm_tech_skills']['skor'],
                    "Alasan CRM/Tech": data['penilaian_kategori']['crm_tech_skills']['ringkasan'],
                    
                    "Skor Comm/English": data['penilaian_kategori']['comm_language_skills']['skor'],
                    "Alasan Comm/English": data['penilaian_kategori']['comm_language_skills']['ringkasan'],
                    
                    "SKOR TOTAL": data['skor_kesesuaian_total'],
                    "REKOMENDASI": data['rekomendasi_akhir']
                }
                all_data_rows.append(row)
            except Exception as e:
                print(f"Gagal memproses data JSON untuk {filename}: {e}")

    # 4. Export ke Excel
    if all_data_rows:
        df = pd.DataFrame(all_data_rows)
        output_file = "laporan_screening_sales_detail.xlsx"
        
        # Simpan ke Excel dengan penyesuaian format sederhana
        df.to_excel(output_file, index=False)
        print(f"\nBerhasil! Laporan detail telah dibuat: {output_file}")
    else:
        print("Gagal mengekstrak data.")

if __name__ == "__main__":
    process_cv_screening()