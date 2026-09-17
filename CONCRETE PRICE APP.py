import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk mempercantik tampilan tab dan kontras warna
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 75, 75, 0.08);
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Judul Utama yang Lebih Terang, Kontras, dan Elegan di Layar Gelap
st.markdown("""
    <div style="text-align: center; padding: 10px 0px 20px 0px;">
        <span style="font-size: 1.8rem; vertical-align: middle;">🏗️</span>
        <span style="font-size: 1.5rem; font-weight: 700; color: #F3F4F6; letter-spacing: 0.5px; vertical-align: middle; margin-left: 8px;">
            KALKULATOR & EVALUASI PENAWARAN PROYEK
        </span>
    </div>
""", unsafe_allow_html=True)

# Helper untuk membersihkan input string berformat ke float
def parse_num(val, default=0.0):
    try:
        cleaned = str(val).replace(".", "").replace(",", "")
        return float(cleaned)
    except:
        return default

# --- MEMBUAT NAVIGASI TAB UTAMA ---
tab1, tab2 = st.tabs(["📋 Evaluasi Penawaran Proyek", "⚙️ Parameter & Acuan Batching Plant"])

# --- TAB 2: PARAMETER & ACUAN BATCHING PLANT ---
with tab2:
    st.markdown("#### ⚙️ Pengaturan Parameter Acuan Bulanan")
    st.caption("Ubah parameter acuan dasar batching plant di sini jika ada pembaruan berkala.")
    
    t2_col1, t2_col2 = st.columns(2, gap="medium")
    with t2_col1:
        raw_cap = st.text_input("Kapasitas Produksi [m³] (Kode: a)", value="7.392")
        cap_prod = parse_num(raw_cap, 7392.0)
        st.caption(f"💡 Terbaca: **{cap_prod:,.2f} m³**")

        raw_cogm = st.text_input("Biaya COGM [Rp/m³] (Kode: b)", value="1.095.193")
        biaya_cogm = parse_num(raw_cogm, 1095193.0)
        st.caption(f"💡 Terbaca: **Rp {biaya_cogm:,.2f}**")

        raw_upah = st.text_input("Biaya Upah Langsung [Rp/m³] (Kode: c)", value="21.831")
        upah_langsung = parse_num(raw_upah, 21831.0)
        st.caption(f"💡 Terbaca: **Rp {upah_langsung:,.2f}**")

    with t2_col2:
        raw_bbm = st.text_input("Biaya BBM Alat [Rp/m³] (Kode: d)", value="111.386")
        bbm_alat = parse_num(raw_bbm, 111386.0)
        st.caption(f"💡 Terbaca: **Rp {bbm_alat:,.2f}**")

        raw_fc = st.text_input("Total Biaya Tetap / Fixed Cost [Rp] (Kode: f)", value="668.523.832")
        fixed_cost = parse_num(raw_fc, 668523832.0)
        st.caption(f"💡 Terbaca: **Rp {fixed_cost:,.2f}**")

    # Hitungan Parameter Acuan Sesuai Rumus Excel
    e_var = biaya_cogm - upah_langsung - bbm_alat
    g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0

    st.markdown("---")
    st.markdown("##### Hasil Turunan Parameter Acuan:")
    st.text_input("Biaya Variabel (e = b - c - d) [Rp/m³]", value=f"{e_var:,.2f}", disabled=True)
    st.caption(f"💡 Terbaca: **Rp {e_var:,.2f}** per m³")

    st.text_input("Biaya Tetap Satuan (g = f / a) [Rp/m³]", value=f"{g_fixed_satuan:,.2f}", disabled=True)
    st.caption(f"💡 Terbaca: **Rp {g_fixed_satuan:,.2f}** per m³")

# Hitung nilai acuan untuk digunakan di Tab 1 juga
e_var = biaya_cogm - upah_langsung - bbm_alat
g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0


# --- TAB 1: EVALUASI PENAWARAN PROYEK (MENU UTAMA) ---
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📋 Masukkan Parameter Penawaran")
        st.caption("Input data pesanan atau penawaran proyek baru")
        
        raw_harga = st.text_input("Harga Jual (h) [Rp/m³]", value="1.300.000", key="in_harga")
        harga_jual = parse_num(raw_harga, 1300000.0)
        st.caption(f"💡 Terbaca: **Rp {harga_jual:,.2f}** per m³")

        raw_vol = st.text_input("Rencana Volume (i) [m³]", value="1.000", key="in_vol")
        rencana_vol = parse_num(raw_vol, 1000.0)
        st.caption(f"💡 Terbaca: **{rencana_vol:,.2f} m³**")

        mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2")
        
        raw_jarak = st.text_input("Jarak Proyek dari Batching Plant [Km]", value="20", key="in_jarak")
        jarak_proyek = parse_num(raw_jarak, 20.0)
        st.caption(f"💡 Terbaca: **{jarak_proyek:,.2f} Km**")

    with col2:
        st.markdown("#### 📊 Hasil Evaluasi & Kelayakan")
        
        # Perhitungan Formula Excel 100% Presisi
        j_margin = harga_jual - e_var
        k_proporsional = (fixed_cost / cap_prod) * rencana_vol if cap_prod > 0 else 0
        l_bep_vol = fixed_cost / j_margin if j_margin > 0 else 0
        status_vol = "Kapasitas Tercukupi" if rencana_vol <= cap_prod else "Volume Melebihi Kapasitas"
        m_total_margin = rencana_vol * j_margin
        n_laba_prop = m_total_margin - k_proporsional
        estimasi_laba_bp = m_total_margin - fixed_cost

        # Status Kelayakan
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
