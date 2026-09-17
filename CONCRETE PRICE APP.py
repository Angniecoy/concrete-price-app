import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide"
)

# Judul Utama
st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-bottom: 25px;'>🏗️ KALKULATOR & EVALUASI PENAWARAN PROYEK</h2>", unsafe_allow_html=True)

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

# --- HALAMAN UTAMA: 2 KOLOM (INPUT PROYEK & HASIL EVALUASI) ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📋 2. Cek Penawaran Proyek")
    st.caption("Masukkan parameter order/penawaran baru")
    
    harga_jual = st.number_input("Harga Jual (h) [Rp/m³]", value=1300000.0, step=10000.0, format="%.2f")
    rencana_vol = st.number_input("Rencana Volume (i) [m³]", value=1000.0, step=10.0, format="%.2f")
    mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2")
    jarak_proyek = st.number_input("Jarak Proyek dari Batching Plant [Km]", value=20.0, step=1.0)

with col2:
    st.markdown("### 📊 3. Hasil Evaluasi & Kelayakan Proyek")
    
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

    # Tampilan Hasil Ringkas & Rapi
    st.markdown(f"""
    - **Margin Kontribusi (j = h - e):** `Rp {j_margin:,.2f} /m³`
    - **Beban Tetap Proporsional (k):** `Rp {k_proporsional:,.2f}`
    - **BEP Volume (l = f / j):** `{l_bep_vol:,.2f} m³`
    - **Status Target Volume:** `{status_vol}`
    - **Total Margin Kontribusi (m):** `Rp {m_total_margin:,.2f}`
    - **Laba Operasi Proporsional (n):** `Rp {n_laba_prop:,.2f}`
    - **Estimasi Laba Operasi BP:** `Rp {estimasi_laba_bp:,.2f}`
    """)

    st.markdown(f"#### Status: {status_layak}")

st.markdown("---")

# --- BAGIAN BAWAH: REKAPITULASI FINANSIAL AKHIR ---
st.markdown("### 🧮 4. Rekapitulasi Finansial Akhir")

bep_rupiah = l_bep_vol * harga_jual           
tot_biaya_var = e_var * l_bep_vol             
tot_biaya = tot_biaya_var + fixed_cost        
cek_nol = tot_biaya - bep_rupiah              

rcol1, rcol2, rcol3, rcol4 = st.columns(4)
rcol1.metric("BEP Rupiah", f"Rp {bep_rupiah:,.0f}")
rcol2.metric("Total Biaya Variabel", f"Rp {tot_biaya_var:,.0f}")
rcol3.metric("Total Biaya", f"Rp {tot_biaya:,.0f}")
rcol4.metric("Cek Harus 0", f"Rp {cek_nol:,.2f}")
