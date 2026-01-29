# LLM For CV Screening - Sistem Penyaringan CV Berbasis AI

Sistem otomatis untuk menyaring dan menganalisis CV menggunakan teknologi AI generatif (Google Gemini 2.5 Flash). Solusi ini dirancang khusus untuk mempercepat proses rekrutmen dengan memberikan penilaian terstruktur dan rekomendasi berbasis kriteria HR.

## 🎯 Fitur Utama

- **Ekstraksi CV Otomatis**: Mengambil informasi dari file PDF secara otomatis
- **Analisis Berbasis AI**: Menggunakan Google Gemini 2.5 Flash untuk analisis mendalam
- **Penilaian Terstruktur**: Menilai kandidat berdasarkan 4 kategori utama dengan bobot yang dapat disesuaikan
- **Laporan Detail**: Menghasilkan file Excel dengan informasi lengkap dan rekomendasi
- **Retry Mechanism**: Implementasi Exponential Backoff untuk menangani timeout API
- **Multi-File Processing**: Memproses multiple CV sekaligus dalam satu batch

## 📋 Kriteria Penilaian

Sistem mengevaluasi kandidat berdasarkan kriteria posisi Sales Representative dengan penimbangan:

| Kriteria | Bobot | Deskripsi |
|----------|-------|-----------|
| **Pengalaman FMCG** | 30% | Minimal 3 tahun di industri barang konsumsi |
| **Pencapaian Target** | 40% | Bukti pencapaian target di atas 100% |
| **Skill CRM/Teknis** | 15% | Penguasaan Salesforce, Hubspot, atau CRM lain |
| **Komunikasi & Bahasa** | 15% | Negosiasi, komunikasi, dan Bahasa Inggris |

## ⚙️ Instalasi

### Persyaratan Sistem
- Python 3.8 atau lebih tinggi
- pip (Python Package Manager)

### Langkah Instalasi

1. **Clone Repository**
```bash
git clone https://github.com/amathiday/LLM-For-CV-Screening.git
cd LLM-For-CV-Screening
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

Atau install secara manual:
```bash
pip install google-generativeai pandas PyPDF2 openpyxl
```

3. **Konfigurasi API Key**
   - Dapatkan API Key dari [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Set API Key sebagai environment variable:
   
   **Linux/Mac:**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   set GOOGLE_API_KEY=your_api_key_here
   ```
   
   **Windows (PowerShell):**
   ```powershell
   $env:GOOGLE_API_KEY="your_api_key_here"
   ```

## 🚀 Cara Penggunaan

1. **Persiapkan File CV**
   - Tempat semua file CV (format PDF) di folder yang sama dengan script
   - Pastikan setiap file adalah dokumen PDF yang valid

2. **Jalankan Script**
   ```bash
   python CV_Screening_AI.py
   ```

3. **Output**
   - Script akan menghasilkan file Excel: `laporan_screening_sales_detail.xlsx`
   - Laporan berisi:
     - Informasi kandidat (nama, pendidikan, kontak, pengalaman)
     - Skor untuk setiap kategori penilaian (0-100)
     - Ringkasan alasan untuk setiap kategori
     - Skor total kesesuaian
     - Rekomendasi akhir (Lanjut / Cadangan / Tolak)

## 📊 Output File Excel

File laporan mencakup kolom berikut:

```
- File Source: Nama file CV sumber
- Nama Kandidat: Nama dari CV
- Pendidikan: Riwayat pendidikan
- Kontak: Informasi kontak
- Total Exp (Tahun): Total pengalaman kerja
- Ringkasan Profil: Ringkasan profil kandidat
- Skor FMCG: Skor untuk pengalaman FMCG (0-100)
- Alasan FMCG: Penjelasan penilaian FMCG
- Skor Sales Record: Skor untuk pencapaian target (0-100)
- Alasan Sales Record: Penjelasan penilaian sales record
- Skor CRM/Tech: Skor untuk skill teknis (0-100)
- Alasan CRM/Tech: Penjelasan penilaian CRM/Tech
- Skor Comm/English: Skor untuk komunikasi & bahasa (0-100)
- Alasan Comm/English: Penjelasan penilaian komunikasi
- SKOR TOTAL: Total skor kesesuaian (0-100)
- REKOMENDASI: Rekomendasi akhir (Lanjut / Cadangan / Tolak)
```

## 🔧 Kustomisasi

### Mengubah Kriteria Penilaian

Modifikasi variabel `hr_requirements` di dalam fungsi `process_cv_screening()`:

```python
hr_requirements = """
Posisi: [Posisi yang Anda inginkan]
Kriteria Utama Penilaian:
1. [Kriteria 1] (Bobot: X%): Deskripsi
2. [Kriteria 2] (Bobot: X%): Deskripsi
...
"""
```

### Mengubah Model AI

Ubah parameter `model_name` di dalam fungsi `call_gemini_with_retry()`:

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Atau model lain yang tersedia
    system_instruction=system_instruction
)
```

## 📝 Struktur Project

```
LLM-For-CV-Screening/
├── CV_Screening_AI.py          # Script utama
├── README.md                   # Dokumentasi ini
├── requirements.txt            # Dependencies
└── [CV Files]                  # Folder untuk file CV (PDF)
    ├── CV_Kandidat_1.pdf
    ├── CV_Kandidat_2.pdf
    └── ...
```

## ⚠️ Pembatasan & Catatan Penting

1. **Format File**: Hanya mendukung file PDF. Pastikan PDF dapat diekstrak teksnya
2. **API Quota**: Google Gemini API memiliki batas penggunaan gratis. Periksa quota di [Google AI Studio](https://aistudio.google.com/)
3. **Timeout Handling**: Script menggunakan exponential backoff untuk menangani timeout (max 5 kali percobaan)
4. **Ukuran File**: Untuk CV dengan ukuran sangat besar, proses ekstraksi mungkin lebih lambat

## 🐛 Troubleshooting

### Error: "API Key tidak ditemukan"
- Pastikan sudah set environment variable `GOOGLE_API_KEY`
- Restart terminal setelah set environment variable

### Error: "Gagal membaca file PDF"
- Verifikasi file PDF tidak corrupt
- Pastikan PDF dapat diekstrak teks (bukan scanned image tanpa OCR)

### Error: "Quota Exceeded"
- Tunggu beberapa jam atau tingkatkan limit API key di Google AI Studio
- Batasi jumlah CV yang diproses sekaligus

### Error: JSON Parse Error
- Mungkin response AI tidak valid JSON
- Coba jalankan ulang script, karena mungkin adalah issue temporary

## 📚 Library yang Digunakan

| Library | Versi | Fungsi |
|---------|-------|--------|
| google-generativeai | Latest | AI API Integration |
| pandas | Latest | Data Processing |
| PyPDF2 | Latest | PDF Text Extraction |
| openpyxl | Latest | Excel File Creation |

## 🔐 Keamanan

- **API Key**: Jangan commit API key ke repository. Gunakan environment variable
- **Sensitive Data**: Pastikan file laporan disimpan di lokasi yang aman
- **Akses File**: Batasi akses ke folder yang berisi CV

## 📞 Support & Kontribusi

Untuk masalah atau saran, silakan buat issue di [GitHub Issues](https://github.com/amathiday/LLM-For-CV-Screening/issues).

## 📄 Lisensi

Project ini menggunakan lisensi MIT. Lihat file LICENSE untuk detail lebih lanjut.

## 🎓 Disclaimer

Sistem ini dirancang sebagai alat bantu dalam proses rekrutmen. Rekomendasi dari sistem harus dipertimbangkan bersama dengan wawancara dan evaluasi manual untuk keputusan rekrutmen final.

---

**Dibuat dengan ❤️ untuk mempermudah proses rekrutmen**