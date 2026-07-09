"""
Konfigurasi koordinat (x, y_dari_atas, y_bottom) untuk tiap field pada tiap
template TaskCard. Koordinat diambil langsung dari hasil analisa PDF asli
(pdfplumber word positions), jadi hasilnya presisi menempel pada kolom yang
sudah tercetak di form.

Cara menambah template baru:
1. Taruh file PDF baru di folder templates/
2. Cari koordinat label memakai pdfplumber (lihat catatan di README.md)
3. Tambahkan entry baru di FIELD_CONFIG mengikuti pola yang sama.

Struktur:
    "nama_file.pdf": {
        "page1": { "field_key": (x, top, bottom), ... },   # khusus halaman 1
        "other_pages": { "field_key": (x, top, bottom), ... },  # halaman 2 dst (berulang sama)
    }

x, top, bottom dalam satuan PDF point, top/bottom dihitung dari SISI ATAS
halaman (seperti pdfplumber). Fungsi generator akan otomatis mengonversi ke
koordinat reportlab (dari bawah).
"""

FIELD_CONFIG = {
    "A320-052000-99-2-SJV-IDN.pdf": {
        "page_size": (595.44, 842.40),
        "page1": {
            "ac_type":     (43.6, 101.9, 109.9),
            "effectivity": (110.2, 101.9, 109.9),
            "wo_no":       (463.3, 101.9, 109.9),
            "ac_reg":      (44.2, 132.5, 140.5),
            "ac_msn":      (111.4, 132.5, 140.5),
            "operator":    (39.7, 198.9, 206.9),
            "place":       (115.8, 198.9, 206.9),
        },
        "other_pages": {
            "wo_no":       (41.2, 101.9, 110.9),
            "ac_reg":      (143.0, 101.9, 110.9),
            "ac_msn":      (196.7, 101.9, 110.9),
            "effectivity": (253.7, 101.9, 110.9),
            "operator":    (353.4, 101.9, 110.9),
        },
    },
}

# Jika ada template baru yang belum terdaftar, konfigurasi ini dipakai
# sebagai fallback (sama dengan template pertama) supaya app tidak error.
DEFAULT_CONFIG_KEY = "A320-052000-99-2-SJV-IDN.pdf"
