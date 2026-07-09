# TaskCard Line Maintenance PKU

Aplikasi Streamlit untuk membuat (generate) TaskCard penerbangan secara
otomatis dengan mengisi data ke atas template PDF.

## Fitur
- Login dengan password (default: `PKU321`, bisa diganti di `app.py`)
- Pilih template TaskCard dari folder `templates/`
- Form input: Work Order No, A/C Reg, A/C MSN, A/C Effectivity, Operator,
  Place, A/C Type
- Generate PDF otomatis dengan data yang sudah diisi di posisi yang tepat
  (halaman 1 dan seluruh halaman berikutnya)
- Download hasil PDF

## Struktur folder
```
taskcard_app/
├── app.py              # Aplikasi utama Streamlit
├── pdf_filler.py        # Logika overlay data ke PDF
├── field_config.py      # Koordinat posisi tiap field per template
├── requirements.txt
└── templates/
    └── A320-052000-99-2-SJV-IDN.pdf
```

## Menjalankan secara lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```
Lalu buka http://localhost:8501 di browser, masukkan password `PKU321`.

## Deploy ke Streamlit Community Cloud (streamlit.app)
1. Buat repository baru di GitHub, upload seluruh isi folder ini.
2. Buka https://share.streamlit.io/ → New app → pilih repo tersebut,
   file utama `app.py`.
3. Klik Deploy. Selesai — akan dapat URL seperti
   `https://namaapp.streamlit.app`.

## Menambahkan template TaskCard baru
Karena posisi tiap kolom (WORK ORDER NO, A/C REG, dst.) berbeda-beda
tergantung layout template PDF, setiap template baru perlu didaftarkan
koordinatnya di `field_config.py`.

Cara mencari koordinat label pada PDF baru:
```python
import pdfplumber
with pdfplumber.open("templates/NAMA_FILE_BARU.pdf") as pdf:
    page = pdf.pages[0]
    for w in page.extract_words():
        print(round(w['x0'],1), round(w['top'],1), round(w['x1'],1), round(w['bottom'],1), w['text'])
```
Dari situ akan terlihat posisi `x0` (kiri) dan `top`/`bottom` (jarak dari
atas halaman) setiap label. Isikan ke `FIELD_CONFIG` mengikuti pola yang
sudah ada, lalu tempatkan file PDF-nya di folder `templates/`.

## Catatan
- Password disimpan sebagai teks polos di `app.py` (variabel
  `APP_PASSWORD`). Untuk keamanan lebih baik, gunakan
  `st.secrets["APP_PASSWORD"]` dan simpan di file `.streamlit/secrets.toml`
  (jangan di-commit ke repo publik).
- Font yang dipakai: Helvetica-Bold ukuran 8pt. Bisa disesuaikan di
  `pdf_filler.py` (variabel `FONT_NAME`, `FONT_SIZE`).
