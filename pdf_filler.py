"""
Logika inti: menimpa (overlay) teks data ke atas template PDF TaskCard.
Menggunakan reportlab untuk menggambar teks, lalu digabung ke halaman asli
memakai pypdf.
"""
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

from field_config import FIELD_CONFIG, DEFAULT_CONFIG_KEY

FONT_NAME = "Helvetica-Bold"
FONT_SIZE = 8


def _draw_fields(c, height, fields_cfg, data):
    """Gambar semua field yang ada di fields_cfg pada canvas overlay."""
    c.setFont(FONT_NAME, FONT_SIZE)
    for key, (x, top, bottom) in fields_cfg.items():
        value = data.get(key, "")
        if not value:
            continue
        y = height - bottom  # konversi ke koordinat reportlab (dari bawah)
        c.drawString(x, y, str(value))


def generate_taskcard(template_path: str, data: dict) -> bytes:
    """
    Mengisi template PDF dengan data yang diberikan.

    data yang didukung (semua opsional):
        wo_no, ac_reg, ac_msn, effectivity, operator, place, ac_type

    Mengembalikan bytes PDF hasil generate.
    """
    reader = PdfReader(template_path)
    writer = PdfWriter()

    template_filename = template_path.split("/")[-1]
    config = FIELD_CONFIG.get(template_filename, FIELD_CONFIG[DEFAULT_CONFIG_KEY])
    page_w, page_h = config["page_size"]

    for i, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(w, h))

        if i == 0:
            _draw_fields(c, h, config.get("page1", {}), data)
        else:
            _draw_fields(c, h, config.get("other_pages", {}), data)

        c.save()
        packet.seek(0)

        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)

    # Salin field checkbox / metadata form jika ada, agar tidak hilang
    if reader.get_fields():
        try:
            writer.append_pages_from_reader = None  # no-op guard
        except Exception:
            pass

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()
