import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Pasar Retail Pro",
    page_icon="🏗️",
    layout="wide"
)

# Custom Style agar tampilan rapi dan proporsional
st.markdown("""
<style>
    .main-title {
        font-size: 26px;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ KALKULATOR & EVALUASI PENAWARAN PROYEK</div>', unsafe_allow_html=True)

# Layout 2 Kolom Utama (Kiri: Input Acuan & Proyek, Kanan: Evaluasi & Rekap)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 1. Acuan Biaya Batching Plant")
    st.caption("Update berkala / parameter bulanan")
    
    cap_prod = st.number_input("Kapasitas Produksi (a) [m³]", value=7392.0, step=100.0, format="%.2f")
    biaya_cogm = st.number_input("Biaya COGM (b) [Rp/m³]", value=1095193.0, step=1000.0, format="%.2f")
    upah_langsung = st.number_input("Biaya Upah Langsung (c) [Rp/m³]", value=21831.0, step=100.0, format="%.2f")
    bbm_alat = st.number_input("Biaya BBM Alat (d) [Rp/m³]", value=111386.0, step=100.0, format="%.2f")
    fixed_cost = st.number_input("Total Biaya Tetap / Fixed Cost (f) [Rp]", value=668523832.0, step=1000000.0, format="%.2f")

    # Hitungan Otomatis Parameter Acuan
    e_var = biaya_cogm - upah_langsung - bbm_alat
    g_fixed_satuan = fixed_cost / cap_prod if cap_prod > 0 else 0

    st.success(f"**Biaya Variabel (e = b - c - d):** Rp {e_var:,.2f} /m³")
    st.info(f"**Biaya Tetap Satuan (g = f / a):** Rp {g_fixed_satuan:,.2f} /m³")

    st.markdown("---")
    st.markdown("### 2. Kalkulator Cek Penawaran Proyek")
    st.caption("Diisi saat ada order masuk")

    harga_jual = st.number_input("Harga Jual (h) [Rp/m³]", value=1300000.0, step=10000.0, format="%.2f")
    rencana_vol = st.number_input("Rencana Volume (i) [m³]", value=1000.0, step=10.0, format="%.2f")
    mutu_beton = st.text_input("Mutu Beton Rencana", value="K250 Slump 12 ± 2")
    jarak_proyek = st.number_input("Jarak Proyek dari Batching Plant [Km]", value=20.0, step=1.0)

with col2:
    st.markdown("### 3. Hasil Evaluasi & Kelayakan Proyek")
    
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

    # Kartu Metrik
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Margin Kontribusi (j)", f"Rp {j_margin:,.2f}")
    m_col2.metric("Beban Tetap Proporsional (k)", f"Rp {k_proporsional:,.2f}")

    m_col3, m_col4 = st.columns(2)
    m_col3.metric("BEP Volume (l)", f"{l_bep_vol:,.2f} m³")
    m_col4.metric("Status Target Volume", status_vol)

    m_col5, m_col6 = st.columns(2)
    m_col5.metric("Total Margin Kontribusi (m)", f"Rp {m_total_margin:,.2f}")
    m_col6.metric("Laba Proporsional Proyek (n)", f"Rp {n_laba_prop:,.2f}")

    st.metric("Estimasi Laba Operasi BP (m - f)", f"Rp {estimasi_laba_bp:,.2f}")
    
    st.subheader(f"Status: {status_layak}")

    st.markdown("---")
    st.markdown("### 4. Rekapitulasi Finansial Akhir")
    
    # Formula Sel Excel Bagian Bawah
    bep_rupiah = l_bep_vol * harga_jual           # D25: D18 * D12
    tot_biaya_var = e_var * l_bep_vol             # D26: D8 * D18
    tot_biaya = tot_biaya_var + fixed_cost        # D27: D26 + D7
    cek_nol = tot_biaya - bep_rupiah              # D28: D27 - D25

    rekap_col1, rekap_col2 = st.columns(2)
    with rekap_col1:
        st.write(f"**BEP Rupiah:**")
        st.write(f"**Total Biaya Variabel:**")
        st.write(f"**Total Biaya:**")
        st.write(f"**Cek Harus 0:**")
    with rekap_col2:
        st.write(f"Rp {bep_rupiah:,.2f}")
        st.write(f"Rp {tot_biaya_var:,.2f}")
        st.write(f"Rp {tot_biaya:,.2f}")
        st.write(f"Rp {cek_nol:,.2f}")
