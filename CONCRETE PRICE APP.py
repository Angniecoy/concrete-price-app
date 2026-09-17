import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOM: MEMPEKATKAN LATAR BELAKANG & KOTAK KONTROL UTAMA ---
st.markdown("""
    <style>
        /* Lapisan gelap latar belakang dibuat sangat pekat (0.93) agar bersih */
        .stApp {
            background-image: linear-gradient(rgba(0, 0, 0, 0.93), rgba(0, 0, 0, 0.93)), 
                              url("https://raw.githubusercontent.com/Angniecoy/concrete-price-app/main/BG%20APP.jpeg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        
        /* Kotak kartu konten utama agar teks dan input sangat mudah dibaca */
        .main-card {
            background-color: rgba(15, 23, 42, 0.92);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.8);
            margin-bottom: 20px;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 75, 75, 0.2);
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEM KEAMANAN (PASSWORD GATEWAY) ---
PASSWORD_BENAR = "2026"  

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col_lock1, col_lock2, col_lock3 = st.columns([1, 1.4, 1])
    with col_lock2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #FFFFFF; margin-bottom: 10px;'>🔒 Autentikasi Masuk</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #D1D5DB; font-size: 0.9rem; margin-bottom: 20px;'>Masukkan password internal untuk mengakses Kalkulator Pasar Retail Pro.</p>", unsafe_allow_html=True)
        
        input_pass = st.text_input("Password", type="password", placeholder="Masukkan password...")
        
        if st.button("Masuk Aplikasi", use_container_width=True):
            if input_pass == PASSWORD_BENAR:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Password salah! Silakan coba lagi.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# KODE UTAMA APLIKASI (HANYA MUNCUL SETELAH LOGIN)
# ==========================================

with st.sidebar:
    st.markdown("### 🔒 Keamanan Akun")
    if st.button("Keluar (Logout)", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("""
    <div style="text-align: center; padding: 10px 0px 20px 0px;">
        <span style="font-size: 1.8rem; vertical-align: middle;">🏗️</span>
        <span style="font-size: 1.5rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.5px; vertical-align: middle; margin-left: 8px; text-shadow: 2px 2px 4px rgba(0,0,0,0.9);">
            KALKULATOR & EVALUASI PENAWARAN PROYEK
        </span>
    </div>
""", unsafe_allow_html=True)

def parse_num(val, default=0.0):
    try:
        cleaned = str(val).replace(".", "").replace(",", "")
        return float(cleaned)
    except:
        return default

tab1, tab2 = st.tabs(["📋 Evaluasi Penawaran Proyek", "⚙️ Parameter & Acuan Batching Plant"])

# --- TAB 2: PARAMETER & ACUAN BATCHING PLANT ---
with tab2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ Pengaturan Parameter Acuan Bulanan")
    st.caption("Ubah parameter acuan dasar batching plant di sini jika ada pembaruan berkala.")
    
    t2_col1, t2_col2 = st.columns(2, gap="medium")
    with t2_col1:
        raw_cap = st.text_input("Kapasitas Produksi [m³] (Kode: a)", value="7.392", key="t2_cap")
        cap_prod = parse_num(raw_cap, 7392.0)
        st.caption(f"💡 Terbaca: **{cap_prod:,.2f} m³**")

        raw_cogm = st.text_input("Biaya COGM [Rp/m³] (Kode: b)", value="1.095.193", key="t2_cogm")
        biaya_cogm = parse_num(raw_cogm, 1095193.0)
        st.caption(f"💡 Terbaca: **Rp {biaya_cogm:,.2f}**")

        raw_upah = st.text_input("Biaya Upah Langsung [Rp/m³] (Kode: c)", value="21.831", key="t2_upah")
        upah_langsung = parse_num(raw_upah, 21831.0)
        st.caption(f"💡 Terbaca: **Rp {upah_langsung:,.2f}**")

    with t2_col2:
        raw_bbm = st.text_input("Biaya BBM Alat [Rp/m³] (Kode: d)", value="111.386", key="t2_bbm")
        bbm_alat = parse_num(raw_bbm, 111386.0)
        st.caption(f"💡 Terbaca: **Rp {bbm_alat:,.2f}**")

        raw_fc = st.text_input("Total Biaya Tetap / Fixed Cost [Rp] (Kode: f)", value="668.523.832", key="t2_fc")
        fixed_cost = parse_num(raw_fc, 668523832.0)
        st.caption(f"💡 Terbaca: **Rp {fixed_cost:,.2f}**")

    e_var = biaya_cogm - upah_langsung - bbm_alat
    g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0

    st.markdown("---")
    st.markdown("##### Hasil Turunan Parameter Acuan:")
    st.text_input("Biaya Variabel (e = b - c - d) [Rp/m³]", value=f"{e_var:,.2f}", disabled=True, key="t2_e")
    st.caption(f"💡 Terbaca: **Rp {e_var:,.2f}** per m³")

    st.text_input("Biaya Tetap Satuan (g = f / a) [Rp/m³]", value=f"{g_fixed_satuan:,.2f}", disabled=True, key="t2_g")
    st.caption(f"💡 Terbaca: **Rp {g_fixed_satuan:,.2f}** per m³")
    st.markdown('</div>', unsafe_allow_html=True)

e_var = biaya_cogm - upah_langsung - bbm_alat
g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0

# --- TAB 1: EVALUASI PENAWARAN PROYEK ---
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Masukkan Parameter Penawaran")
        st.caption("Input data pesanan atau penawaran proyek baru")
        
        raw_harga = st.text_input("Harga Jual (h) [Rp/m³]", value="1.300.000", key="in_harga")
        harga_jual = parse_num(raw_harga, 1300000.0)
        st.caption(f"💡 Terbaca: **Rp {harga_jual:,.2f}** per m³")

        raw_vol = st.text_input("Rencana Volume (i) [m³]", value="1.000", key="in_vol")
        rencana_vol = parse_num(raw_vol, 1000.0)
        st.caption(f"💡 Terbaca: **{rencana_vol:,.2f} m³**")

        mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2", key="in_mutu")
        
        raw_jarak = st.text_input("Jarak Proyek dari Batching Plant [Km]", value="20", key="in_jarak")
        jarak_proyek = parse_num(raw_jarak, 20.0)
        st.caption(f"💡 Terbaca: **{jarak_proyek:,.2f} Km**")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Hasil Evaluasi & Kelayakan")
        
        j_margin = harga_jual - e_var
        k_proporsional = (fixed_cost / cap_prod) * rencana_vol if cap_prod > 0 else 0
        l_bep_vol = fixed_cost / j_margin if j_margin > 0 else 0
        status_vol = "Kapasitas Tercukupi" if rencana_vol <= cap_prod else "Volume Melebihi Kapasitas"
        m_total_margin = rencana_vol * j_margin
        n_laba_prop = m_total_margin - k_proporsional
        estimasi_laba_bp = m_total_margin - fixed_cost

        if j_margin > 0:
            if n_laba_prop < 0:
                status_layak = "🟡 Layak (Bantu Tutup Biaya Tetap)"
            else:
                status_layak = "🟢 Sangat Layak (Laba Penuh)"
        else:
            status_layak = "🔴 Tidak Layak (Harga Jual < Biaya Var)"

        st.text_input("Margin Kontribusi (j = h - e) [Rp/m³]", value=f"{j_margin:,.2f}", disabled=True, key="res_j")
        st.caption(f"💡 Terbaca: **Rp {j_margin:,.2f}** per m³")

        st.text_input("Beban Biaya Tetap Proporsional (k = (f/a)*i) [Rp]", value=f"{k_proporsional:,.2f}", disabled=True, key="res_k")
        st.caption(f"💡 Terbaca: **Rp {k_proporsional:,.2f}**")

        st.text_input("BEP Volume (l = f / j) [m³]", value=f"{l_bep_vol:,.2f}", disabled=True, key="res_l")
        st.caption(f"💡 Terbaca: **{l_bep_vol:,.2f} m³**")

        st.text_input("Status Target Volume Proyek", value=status_vol, disabled=True, key="res_svol")
        st.caption(f"💡 Status: **{status_vol}**")

        st.text_input("Total Margin Kontribusi (m = i * j) [Rp]", value=f"{m_total_margin:,.2f}", disabled=True, key="res_m")
        st.caption(f"💡 Terbaca: **Rp {m_total_margin:,.2f}**")

        st.text_input("Laba Operasi Proporsional Proyek (n = m - k) [Rp]", value=f"{n_laba_prop:,.2f}", disabled=True, key="res_n")
        st.caption(f"💡 Terbaca: **Rp {n_laba_prop:,.2f}**")

        st.text_input("Estimasi Laba Operasi Batching Plant (m - f) [Rp]", value=f"{estimasi_laba_bp:,.2f}", disabled=True, key="res_bp")
        st.caption(f"💡 Terbaca: **Rp {estimasi_laba_bp:,.2f}**")

        st.text_input("Status Kelayakan Harga Proyek", value=status_layak, disabled=True, key="res_layak")
        st.caption(f"💡 Keputusan: **{status_layak}**")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER COPYRIGHT ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #FFFFFF; font-size: 0.85rem; padding: 10px 0px 20px 0px; text-shadow: 1px 1px 2px rgba(0,0,0,0.9);">
        © 2026 PT Waskita Beton Precast Tbk · Kalkulator Pasar Retail Pro v2.1 | Developed By RMQ Division
    </div>
""", unsafe_allow_html=True)
