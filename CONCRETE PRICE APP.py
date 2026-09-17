import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ToolsPasarRetailModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Pasar Retail Pro (Sesuai Excel)")
        self.root.geometry("950x900")
        
        self.style = ttk.Style(theme="flatly")

        # --- KANVAS UTAMA & SCROLLBAR RESPONSIF ---
        self.main_canvas = tk.Canvas(self.root, bg="#f4f6f9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.main_canvas, padding=20)
        
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.bind('<Configure>', self.on_canvas_configure)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.root.bind_all("<MouseWheel>", lambda event: self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.create_widgets()
        self.hitung_otomatis()

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def create_widgets(self):
        # Header Judul Utama
        title_lbl = ttk.Label(
            self.scrollable_frame, text="KALKULATOR & EVALUASI PENAWARAN PROYEK (EXCEL SYNC)", 
            font=("Segoe UI", 16, "bold"), bootstyle="primary"
        )
        title_lbl.pack(pady=(5, 15), anchor="center")

        # 1. FRAME ACUAN BIAYA BATCHING PLANT
        frame_bp = ttk.LabelFrame(self.scrollable_frame, text=" 1. Acuan Biaya Batching Plant (Update berkala/bulanan) ", padding=12, bootstyle="info")
        frame_bp.pack(fill=X, pady=6)
        frame_bp.columnconfigure(1, weight=1)

        self.entries_bp = {}
        bp_data = [
            ("Kapasitas Produksi", "7392", "m³", "a"),
            ("Biaya COGM", "1095193", "Rp/m³", "b"),
            ("Biaya Upah Langsung", "21831", "Rp/m³", "c"),
            ("Biaya BBM Alat", "111386", "Rp/m³", "d"),
            ("Total biaya tetap (fixed cost)", "668523832", "Rp", "f")
        ]

        for i, (label_text, default_val, unit, kode) in enumerate(bp_data):
            ttk.Label(frame_bp, text=f"{label_text} ({unit}) [{kode}]", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=6)
            ent = ttk.Entry(frame_bp, font=("Segoe UI", 10))
            ent.insert(0, default_val)
            ent.grid(row=i, column=1, sticky="ew", padx=5, pady=6)
            ent.bind("<KeyRelease>", lambda event: self.hitung_otomatis())
            self.entries_bp[label_text] = ent

        # Biaya Variabel & Biaya Tetap di Bagian Acuan
        frame_acuan_out = ttk.Frame(self.scrollable_frame, padding=5)
        frame_acuan_out.pack(fill=X, pady=4)
        frame_acuan_out.columnconfigure(1, weight=1)

        ttk.Label(frame_acuan_out, text="Biaya variabel (variable cost) [e = b - c - d] (Rp/m³):", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.lbl_biaya_variabel = ttk.Label(frame_acuan_out, text="-", font=("Segoe UI", 10, "bold"), anchor="e", relief="sunken", padding=4, bootstyle="inverse-info")
        self.lbl_biaya_variabel.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(frame_acuan_out, text="Biaya tetap (fixed cost) [g = f / a] (Rp/m³):", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.lbl_biaya_tetap_satuan = ttk.Label(frame_acuan_out, text="-", font=("Segoe UI", 10, "bold"), anchor="e", relief="sunken", padding=4, bootstyle="inverse-info")
        self.lbl_biaya_tetap_satuan.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        ttk.Separator(self.scrollable_frame, orient=HORIZONTAL).pack(fill=X, pady=10)

        # 2. FRAME KALKULATOR CEK PENAWARAN PROYEK (INPUT ORANYE)
        frame_proyek = ttk.LabelFrame(self.scrollable_frame, text=" 2. Kalkulator Cek Penawaran Proyek (Diisi saat ada order) ", padding=12, bootstyle="warning")
        frame_proyek.pack(fill=X, pady=6)
        frame_proyek.columnconfigure(1, weight=1)

        self.entries_proyek = {}
        proyek_data = [
            ("Harga Jual", "1300000", "Rp/m³", "h"),
            ("Rencana Volume", "1000", "m³", "i"),
            ("Mutu Beton Rencana", "K250 Slump 12 ± 2", "Text", ""),
            ("Jarak Proyek dari Batching Plant", "20", "Km", "")
        ]

        for i, (label_text, default_val, unit, kode) in enumerate(proyek_data):
            display_txt = f"{label_text} ({unit})" + (f" [{kode}]" if kode else "")
            ttk.Label(frame_proyek, text=display_txt, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=6)
            
            ent = ttk.Entry(frame_proyek, font=("Segoe UI", 10))
            ent.insert(0, default_val)
            if "Mutu" not in label_text:
                ent.bind("<KeyRelease>", lambda event: self.hitung_otomatis())
            
            ent.grid(row=i, column=1, sticky="ew", padx=5, pady=6)
            self.entries_proyek[label_text] = ent

        # 3. FRAME HASIL EVALUASI KELAYAKAN
        frame_hasil = ttk.LabelFrame(self.scrollable_frame, text=" 3. Hasil Evaluasi & Kelayakan Proyek ", padding=12, bootstyle="success")
        frame_hasil.pack(fill=X, pady=10)
        frame_hasil.columnconfigure(1, weight=1)

        self.labels_hasil = {}
        hasil_items = [
            ("Margin kontribusi [j = h - e]", "Rp/m³"),
            ("Beban Biaya Tetap Proporsional [k = (f / a) * i]", "Rp"),
            ("BEP Volume [l = f / j]", "m³"),
            ("Status Target Volume Proyek", "Text"),
            ("Total Margin kontribusi [m = i * j]", "Rp"),
            ("Laba Operasi Proporsional Proyek [n = m - k]", "Rp"),
            ("Estimasi Laba Operasi Batching Plant [m = l - a]", "Rp"),
            ("Status Kelayakan Harga Proyek", "Text")
        ]

        for i, (item, unit) in enumerate(hasil_items):
            ttk.Label(frame_hasil, text=f"{item} ({unit}):", font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            val_lbl = ttk.Label(frame_hasil, text="-", font=("Segoe UI", 10, "bold"), anchor="e", relief="flat", padding=(6, 3), bootstyle="inverse-secondary")
            val_lbl.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.labels_hasil[item] = val_lbl

        # 4. FRAME REKAPITULASI FINANSIAL AKHIR (SESUAI RUMUS EXCEL)
        frame_bawah = ttk.LabelFrame(self.scrollable_frame, text=" 4. Rekapitulasi Finansial Akhir ", padding=12, bootstyle="dark")
        frame_bawah.pack(fill=X, pady=10)
        frame_bawah.columnconfigure(1, weight=1)

        self.labels_bawah = {}
        bawah_items = [
            ("BEP Rupiah [f = e * c -> BEP Vol * Harga Jual]", "Rp"),
            ("Total biaya variabel (variable cost) [g = b * e -> Biaya Var * BEP Vol]", "Rp"),
            ("Total biaya [h = a + g -> Total Biaya Variabel + Fixed Cost]", "Rp"),
            ("Cek harus 0 [i = f - h]", "Rp")
        ]

        for i, (item, unit) in enumerate(bawah_items):
            ttk.Label(frame_bawah, text=f"{item} ({unit}):", font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            val_lbl = ttk.Label(frame_bawah, text="-", font=("Segoe UI", 10, "bold"), anchor="e", relief="flat", padding=(6, 3), bootstyle="inverse-light")
            val_lbl.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.labels_bawah[item] = val_lbl

        # Tombol Aksi di Bagian Bawah
        action_frame = ttk.Frame(self.scrollable_frame, padding=10)
        action_frame.pack(fill=X)
        ttk.Button(action_frame, text="Refresh Hitungan", bootstyle="primary-outline", command=self.hitung_otomatis).pack(fill=X, pady=5)

    def hitung_otomatis(self):
        try:
            a = float(self.entries_bp["Kapasitas Produksi"].get().replace(",", "").replace(" ", ""))
            b = float(self.entries_bp["Biaya COGM"].get().replace(",", "").replace(" ", ""))
            c = float(self.entries_bp["Biaya Upah Langsung"].get().replace(",", "").replace(" ", ""))
            d = float(self.entries_bp["Biaya BBM Alat"].get().replace(",", "").replace(" ", ""))
            f_fixed = float(self.entries_bp["Total biaya tetap (fixed cost)"].get().replace(",", "").replace(" ", ""))

            h_jual = float(self.entries_proyek["Harga Jual"].get().replace(",", "").replace(" ", ""))
            i_vol = float(self.entries_proyek["Rencana Volume"].get().replace(",", "").replace(" ", ""))

            # Rumus Dasar Sesuai Excel
            e_var = b - c - d
            g_fixed_satuan = f_fixed / a if a > 0 else 0
            
            j_margin = h_jual - e_var
            k_proporsional = (f_fixed / a) * i_vol if a > 0 else 0  
            l_bep_vol = f_fixed / j_margin if j_margin > 0 else 0
            
            status_vol = "Kapasitas Tercukupi" if i_vol <= a else "Volume Melebihi Kapasitas"
            m_total_margin = i_vol * j_margin
            n_laba_prop = m_total_margin - k_proporsional
            estimasi_laba_bp = m_total_margin - f_fixed

            # Status Kelayakan
            if j_margin > 0:
                if n_laba_prop < 0:
                    status_layak = "🟡 Layak (Bantu Tutup Biaya Tetap)"
                    color_status = "warning"
                else:
                    status_layak = "🟢 Sangat Layak (Laba Penuh)"
                    color_status = "success"
            else:
                status_layak = "🔴 Tidak Layak (Harga Jual < Biaya Var)"
                color_status = "danger"

            # Rekapitulasi Akhir Sesuai Formula Sel Excel:
            # D25 (BEP Rupiah) = D18 * D12 (BEP Volume * Harga Jual)
            bep_rupiah = l_bep_vol * h_jual  
            
            # D26 (Total Biaya Variabel) = D8 * D18 (Biaya Variabel per m3 * BEP Volume)
            tot_biaya_var = e_var * l_bep_vol 
            
            # D27 (Total Biaya) = D26 + D7 (Total Biaya Variabel + Total Biaya Tetap)
            tot_biaya = tot_biaya_var + f_fixed 
            
            # D28 (Cek harus 0) = D27 - D25 (Total Biaya - BEP Rupiah)
            cek_nol = tot_biaya - bep_rupiah

            # Update Label Acuan
            self.lbl_biaya_variabel.config(text=f"{e_var:,.2f}")
            self.lbl_biaya_tetap_satuan.config(text=f"{g_fixed_satuan:,.2f}")

            # Update Label Evaluasi Proyek
            self.labels_hasil["Margin kontribusi [j = h - e]"].config(text=f"{j_margin:,.2f}")
            self.labels_hasil["Beban Biaya Tetap Proporsional [k = (f / a) * i]"].config(text=f"{k_proporsional:,.2f}")
            self.labels_hasil["BEP Volume [l = f / j]"].config(text=f"{l_bep_vol:,.2f}")
            self.labels_hasil["Status Target Volume Proyek"].config(text=status_vol)
            self.labels_hasil["Total Margin kontribusi [m = i * j]"].config(text=f"{m_total_margin:,.2f}")
            self.labels_hasil["Laba Operasi Proporsional Proyek [n = m - k]"].config(text=f"{n_laba_prop:,.2f}")
            self.labels_hasil["Estimasi Laba Operasi Batching Plant [m = l - a]"].config(text=f"{estimasi_laba_bp:,.2f}")
            
            lbl_status = self.labels_hasil["Status Kelayakan Harga Proyek"]
            lbl_status.config(text=status_layak, bootstyle=f"inverse-{color_status}")

            # Update Label Rekapitulasi Akhir (Sesuai Excel)
            self.labels_bawah["BEP Rupiah [f = e * c -> BEP Vol * Harga Jual]"].config(text=f"{bep_rupiah:,.2f}")
            self.labels_bawah["Total biaya variabel (variable cost) [g = b * e -> Biaya Var * BEP Vol]"].config(text=f"{tot_biaya_var:,.2f}")
            self.labels_bawah["Total biaya [h = a + g -> Total Biaya Variabel + Fixed Cost]"].config(text=f"{tot_biaya:,.2f}")
            self.labels_bawah["Cek harus 0 [i = f - h]"].config(text=f"{cek_nol:,.2f}")

        except ValueError:
            pass

if __name__ == "__main__":
    root = ttk.Window()
    app = ToolsPasarRetailModernApp(root)
    root.mainloop()