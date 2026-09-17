import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Judul Utama
st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-bottom: 15px;'>🏗️ KALKULATOR & EVALUASI PENAWARAN PROYEK</h3>", unsafe_allow_html=True)

# Helper untuk membersihkan input string berformat ke float
def parse_num(val, default=0.0):
    try:
        cleaned = str(val).replace(".", "").replace(",", "")
        return float(cleaned)
    except:
        return default

# --- PANEL ACUAN DI BAGIAN ATAS (BERJAJAR KEBAWAH TANPA KOTAK TERPISAH) ---
with st.expander("📌 Acuan Biaya Batching Plant (Parameter Bulanan)", expanded=True):
    ac1, ac2 = st.columns(2, gap="medium")
    with ac1:
        raw_cap = st.text_input("Kapasitas Produksi [m³] (Kode: a)", value="7.392")
        cap_prod = parse_num(raw_cap, 7392.0)
        st.caption(f"💡 Terbaca: **{cap_prod:,.2f} m³**")

        raw_cogm = st.text_input("Biaya COGM [Rp/m³] (Kode: b)", value="1.095.193")
        biaya_cogm = parse_num(raw_cogm, 1095193.0)
        st.caption(f"💡 Terbaca: **Rp {biaya_cogm:,.2f}**")

        raw_upah = st.text_input("Biaya Upah Langsung [Rp/m³] (Kode: c)", value="21.831")
        upah_langsung = parse_num(raw_upah, 21831.0)
        st.caption(f"💡 Terbaca: **Rp {upah_langsung:,.2f}**")

    with ac2:
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
    st.markdown(f"• **Biaya Variabel (e = b - c - d):** Rp {e_var:,.2f} /m³")
    st.markdown(f"• **Biaya Tetap Satuan (g = f / a):** Rp {g_fixed_satuan:,.2f} /m³")

st.markdown("---")

# --- HALAMAN UTAMA: CEK PENAWARAN & EVALUASI ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("### 📋 Cek Penawaran Proyek")
    st.caption("Masukkan parameter order/penawaran baru")
    
    raw_harga = st.text_input("Harga Jual (h) [Rp/m³]", value="1.300.000")
    harga_jual = parse_num(raw_harga, 1300000.0)
    st.caption(f"💡 Terbaca: **Rp {harga_jual:,.2f}** per m³")

    raw_vol = st.text_input("Rencana Volume (i) [m³]", value="1.000")
    rencana_vol = parse_num(raw_vol, 1000.0)
    st.caption(f"💡 Terbaca: **{rencana_vol:,.2f} m³**")

    mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2")
    
    raw_jarak = st.text_input("Jarak Proyek dari Batching Plant [Km]", value="20")
    jarak_proyek = parse_num(raw_jarak, 20.0)
    st.caption(f"💡 Terbaca: **{jarak_proyek:,.2f} Km**")

with col2:
    st.markdown("### 📊 Hasil Evaluasi & Kelayakan")
    
    # Perhitungan Formula Excel 100% Presisi
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

    def render_box(title, value):
        st.markdown(f"""
        <div style="margin-bottom: 8px;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #d1d5db; margin-bottom: 2px;">{title}</div>
            <div style="
                border: 1.5px solid #ff4b4b; 
                border-radius: 6px; 
                padding: 6px 12px; 
                background-color: rgba(255, 75, 75, 0.04);
                font-size: 1.05rem;
                font-weight: 700;
            ">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    render_box("Margin Kontribusi (j = h - e):", f"Rp {j_margin:,.2f} /m³")
    render_box("Beban Biaya Tetap Proporsional (k = (f/a)*i):", f"Rp {k_proporsional:,.2f}")
    render_box("BEP Volume (l = f / j):", f"{l_bep_vol:,.2f} m³")
    render_box("Status Target Volume Proyek:", status_vol)
    render_box("Total Margin Kontribusi (m = i * j):", f"Rp {m_total_margin:,.2f}")
    render_box("Laba Operasi Proporsional Proyek (n = m - k):", f"Rp {n_laba_prop:,.2f}")
    render_box("Estimasi Laba Operasi Batching Plant (m - f):", f"Rp {estimasi_laba_bp:,.2f}")
    render_box("Status Kelayakan Harga Proyek:", status_layak)
