import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Judul Utama
st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-bottom: 20px;'>🏗️ KALKULATOR & EVALUASI PENAWARAN PROYEK</h3>", unsafe_allow_html=True)

# --- SIDEBAR: ACUAN BIAYA BATCHING PLANT ---
with st.sidebar:
    st.markdown("### ⚙️ Acuan Biaya Batching Plant")
    st.caption("Parameter bulanan / berjalan")
    
    cap_prod = st.number_input("Kapasitas Produksi (a) [m³]", value=7392.0, step=100.0, format="%.2f")
    biaya_cogm = st.number_input("Biaya COGM (b) [Rp/m³]", value=1095193.0, step=1000.0, format="%.2f")
    upah_langsung = st.number_input("Biaya Upah Langsung (c) [Rp/m³]", value=21831.0, step=100.0, format="%.2f")
    bbm_alat = st.number_input("Biaya BBM Alat (d) [Rp/m³]", value=111386.0, step=100.0, format="%.2f")
    fixed_cost = st.number_input("Total Biaya Tetap / Fixed Cost (f) [Rp]", value=668523832.0, step=1000000.0, format="%.2f")

    # Hitungan Parameter Acuan
    e_var = biaya_cogm - upah_langsung - bbm_alat
    g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0

    st.markdown("---")
    st.markdown(f"**Biaya Variabel (e):** `Rp {e_var:,.2f} /m³`")
    st.markdown(f"**Biaya Tetap Satuan (g):** `Rp {g_fixed_satuan:,.2f} /m³`")

# --- HALAMAN UTAMA ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("### 📋 Cek Penawaran Proyek")
    st.caption("Masukkan parameter order/penawaran baru")
    
    harga_jual = st.number_input("Harga Jual (h) [Rp/m³]", value=1300000.0, step=10000.0, format="%.2f")
    rencana_vol = st.number_input("Rencana Volume (i) [m³]", value=1000.0, step=10.0, format="%.2f")
    mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2")
    jarak_proyek = st.number_input("Jarak Proyek dari Batching Plant [Km]", value=20.0, step=1.0)

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

    # Status Kelayakan Sesuai Logika Excel
    if j_margin > 0:
        if n_laba_prop < 0:
            status_layak = "🟡 Layak (Bantu Tutup Biaya Tetap)"
        else:
            status_layak = "🟢 Sangat Layak (Laba Penuh)"
    else:
        status_layak = "🔴 Tidak Layak (Harga Jual < Biaya Var)"

    # Helper function untuk membuat kotak nilai (rectangle merah tipis)
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

st.markdown("---")

# --- BAGIAN BAWAH: REKAPITULASI FINANSIAL AKHIR ---
st.markdown("### 🧮 Rekapitulasi Finansial Akhir")

bep_rupiah = l_bep_vol * harga_jual           
tot_biaya_var = e_var * l_bep_vol             
tot_biaya = tot_biaya_var + fixed_cost        
cek_nol = tot_biaya - bep_rupiah              

render_box("BEP Rupiah (f = BEP Vol * Harga Jual):", f"Rp {bep_rupiah:,.2f}")
render_box("Total Biaya Variabel (g = Biaya Var * BEP Vol):", f"Rp {tot_biaya_var:,.2f}")
render_box("Total Biaya (h = Total Biaya Variabel + Fixed Cost):", f"Rp {tot_biaya:,.2f}")
render_box("Cek Harus 0 (i = f - h):", f"Rp {cek_nol:,.2f}")
