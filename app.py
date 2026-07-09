import os
import glob
import datetime
import streamlit as st

from pdf_filler import generate_taskcard

# --------------------------------------------------------------------------
# KONFIGURASI DASAR
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="TaskCard Line Maintenance PKU",
    page_icon="🛩️",
    layout="centered",
)

APP_PASSWORD = "PKU321"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

OPERATOR_OPTIONS = ["LION AIR", "BATIK AIR", "WINGS AIR", "SUPER AIR JET", "THAI LION AIR"]
AC_TYPE_OPTIONS = ["B737-800 NG", "B737 MAX 8", "A320", "A320 NEO", "A330"]


# --------------------------------------------------------------------------
# STYLING (meniru gaya tampilan referensi)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        color: #E30613;
        font-weight: 800;
        text-align: center;
        font-size: 2.1rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 0.95rem;
        margin-bottom: 1.6rem;
    }
    .section-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# GERBANG PASSWORD
# --------------------------------------------------------------------------
def check_password() -> bool:
    if st.session_state.get("authenticated", False):
        return True

    st.markdown("<div class='main-title'>🔒 TASKCARD LINE MAINTENANCE PKU</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Masukkan password untuk mengakses aplikasi</div>", unsafe_allow_html=True)

    with st.form("login_form"):
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Masuk")

    if submitted:
        if pwd == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Password salah. Silakan coba lagi.")

    return False


if not check_password():
    st.stop()


# --------------------------------------------------------------------------
# HALAMAN UTAMA (setelah login)
# --------------------------------------------------------------------------
st.markdown("<div class='main-title'>TASKCARD LINE MAINTENANCE PKU</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>TASKCARD DAILY CHECK, PRE-FLIGHT CHECK, WEEKLY CHECK AIRBUS A320 AND BOEING 737</div>",
    unsafe_allow_html=True,
)

# --- Pilih TaskCard ---
template_files = sorted(glob.glob(os.path.join(TEMPLATES_DIR, "*.pdf")))
template_names = [os.path.basename(f) for f in template_files]

if not template_names:
    st.warning("Belum ada template TaskCard di folder `templates/`. Tambahkan file PDF terlebih dahulu.")
    st.stop()

st.markdown("📄 **Choose TaskCard**")
selected_template = st.selectbox(
    "Choose TaskCard", template_names, label_visibility="collapsed"
)
template_path = os.path.join(TEMPLATES_DIR, selected_template)

st.markdown("---")

# --- Form input data ---
with st.container(border=True):
    st.markdown("<div class='section-title'>MASUKAN DATA DENGAN BENAR</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        wo_no = st.text_input("WORK ORDER NO.")
        ac_reg = st.text_input("A/C REG.")
        ac_msn = st.text_input("A/C MSN.")
        ac_type = st.selectbox("A/C TYPE", AC_TYPE_OPTIONS)
    with col2:
        effectivity = st.text_input("A/C Effectivity")
        operator = st.selectbox("OPERATOR", OPERATOR_OPTIONS)
        place = st.text_input("PLACE")

    generate_clicked = st.button("Generate TaskCard", type="primary")

# --------------------------------------------------------------------------
# PROSES GENERATE
# --------------------------------------------------------------------------
if generate_clicked:
    missing = []
    if not wo_no:
        missing.append("WORK ORDER NO.")
    if not ac_reg:
        missing.append("A/C REG.")
    if not ac_msn:
        missing.append("A/C MSN.")
    if not effectivity:
        missing.append("A/C Effectivity")
    if not place:
        missing.append("PLACE")

    if missing:
        st.error("Mohon lengkapi data berikut: " + ", ".join(missing))
    else:
        data = {
            "wo_no": wo_no.strip(),
            "ac_reg": ac_reg.strip().upper(),
            "ac_msn": ac_msn.strip(),
            "effectivity": effectivity.strip(),
            "operator": operator,
            "place": place.strip().upper(),
            "ac_type": ac_type,
        }

        with st.spinner("Sedang membuat TaskCard..."):
            pdf_bytes = generate_taskcard(template_path, data)

        st.success("TaskCard berhasil dibuat!")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = f"TC_{ac_reg.strip().upper()}_{wo_no.strip()}_{timestamp}.pdf"

        st.download_button(
            label="⬇️ Download TaskCard",
            data=pdf_bytes,
            file_name=out_name,
            mime="application/pdf",
        )
