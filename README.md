# Proyek Analisis Data E-Commerce (Olist Brazilian E-Commerce Dataset)

## Informasi Peserta
- **Nama:** Noval Berauh
- **Email:** mikelizer123@gmail.com
- **ID Dicoding:** ds506b6y1389

---

## Deskripsi Proyek
Proyek ini menganalisis data transaksi *Brazilian E-Commerce Public Dataset by Olist* untuk menggali *insight* strategis yang berorientasi pada tindakan (*actionable insights*). Fokus analisis meliputi:
1. **Evaluasi Operasional Logistik & Kepuasan Pelanggan (Tahun 2017):** Mengukur dampak keterlambatan pengiriman (*actual delivery > estimated delivery*) terhadap penurunan rata-rata skor ulasan pelanggan (`review_score`) pada 10 kategori produk dengan volume pesanan tertinggi.
2. **Perilaku Pembayaran & Nilai Transaksi Wilayah (Semester 1 2018):** Membandingkan *Gross Merchandise Value* (GMV), *Average Order Value* (AOV), dan rata-rata jumlah cicilan (`payment_installments`) antara metode pembayaran Kartu Kredit (`credit_card`) dan `boleto` di 5 negara bagian (`customer_state`) terbesar.
3. **Analisis Lanjutan (Tanpa Algoritma Machine Learning):**
   - **RFM Analysis (*Recency, Frequency, Monetary*):** Mengidentifikasi pelanggan terbaik berdasarkan waktu transaksi terakhir, frekuensi pemesanan, dan nilai kontribusi pendapatan.
   - **Manual Grouping / Binning:** Mengelompokkan pelanggan ke dalam 5 segmen bisnis (*Champions*, *Loyal Customers*, *Potential Loyalists*, *At Risk*, dan *Lost*) berbasis aturan kuartil skor RFM.
   - **Geospatial Analysis:** Memetakan kepadatan transaksi dan rata-rata hari keterlambatan pengiriman berdasarkan koordinat geografis (`geolocation_lat`, `geolocation_lng`) di wilayah Brasil.

---

## Struktur Direktori
```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

---

## Instruksi Instalasi & Persiapan Lingkungan

### 1. Menggunakan Anaconda / Miniconda (Opsional)
```bash
conda create --name ecommerce-analytics python=3.10 -y
conda activate ecommerce-analytics
```

### 2. Menggunakan Virtual Environment (`venv`) atau Pip Langsung
```bash
python -m venv .venv
# Aktivasi di Windows:
.venv\Scripts\activate
# Aktivasi di macOS/Linux:
source .venv/bin/activate
```

### 3. Instalasi Dependencies
Instal seluruh pustaka yang dibutuhkan melalui `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan Dashboard Streamlit
Jalankan perintah berikut dari direktori utama proyek (*root folder*):
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard interaktif akan terbuka secara otomatis di peramban (*browser*) Anda pada alamat `http://localhost:8501`.

