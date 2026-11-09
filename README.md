# 📊 Brazilian E-Commerce Public Analysis Dashboard

Proyek akhir analisis data menggunakan **E-Commerce Public Dataset** dari Olist Store untuk memenuhi kriteria kelulusan kelas **"Belajar Analisis Data dengan Python"** di Dicoding Academy.

---

## 📌 Ringkasan Proyek
Proyek ini melakukan analisis data menyeluruh mulai dari perumusan pertanyaan bisnis (menggunakan kaidah SMART), data wrangling (*gathering, assessing, cleaning*), *Exploratory Data Analysis* (EDA), visualisasi data, hingga pembuatan dashboard interaktif berbasis Streamlit.

### 🎯 Pertanyaan Bisnis yang Dijawab
1. **Operasional Logistik & Kepuasan Pelanggan:** Seberapa besar penurunan rata-rata skor ulasan pelanggan (`review_score`) pada pesanan yang mengalami keterlambatan pengiriman (*actual delivery > estimated delivery*) dibandingkan pengiriman tepat waktu pada 10 kategori produk dengan volume pesanan tertinggi sepanjang tahun 2017?
2. **Perilaku Pembayaran & Nilai Transaksi Wilayah:** Bagaimana perbandingan total nilai transaksi (*Gross Merchandise Value*), rata-rata nilai pesanan (*Average Order Value*), dan rata-rata jumlah cicilan (`payment_installments`) antara metode pembayaran Kartu Kredit (`credit_card`) dan `boleto` di 5 negara bagian (`customer_state`) dengan transaksi tertinggi selama Semester 1 tahun 2018 (Januari – Juni 2018)?

### ⭐ Analisis Lanjutan (Nilai Maksimal / Bintang 5)
* **RFM Analysis (Recency, Frequency, Monetary):** Mengukur nilai pelanggan berdasarkan hari sejak transaksi terakhir (*Recency*), total pesanan unik (*Frequency*), dan total nilai belanja (*Monetary*).
* **Customer Segmentation (Manual Grouping / Binning):** Segmentasi perilaku pelanggan (*Champions, Loyal Customers, Potential Loyalists, At Risk, Lost*) berbasis aturan kuartil skor RFM tanpa algoritma *Machine Learning*.
* **Geospatial Analysis:** Pemetaan spasial kepadatan transaksi dan tingkat keterlambatan pengiriman di seluruh negara bagian Brasil untuk mengevaluasi efisiensi SLA logistik.

---

## 📁 Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py           # Berkas aplikasi Streamlit
│   └── main_data.csv          # Berkas dataset gabungan bersih (< 25 MB)
├── data/                      # Dataset mentah (E-Commerce Public Dataset)
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb             # Jupyter Notebook proses analisis (sudah dieksekusi)
├── README.md                  # Dokumentasi proyek & panduan instalasi
├── requirements.txt           # Daftar library Python yang dibutuhkan
└── url.txt                    # Tautan live dashboard di Streamlit Community Cloud
```

---

## 🚀 Panduan Menjalankan Dashboard Secara Lokal

### 1. Kloning Repository atau Buka Folder Proyek
```bash
git clone https://github.com/MIKELIZER/analisis_data_e-commerce.git
cd analisis_data_e-commerce
```

### 2. Membuat dan Mengaktifkan Virtual Environment (Opsional namun disarankan)
Menggunakan **venv**:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
Atau menggunakan **Conda**:
```bash
conda create --name ecommerce-dashboard python=3.12
conda activate ecommerce-dashboard
```

### 3. Menginstal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi akan secara otomatis terbuka di peramban web pada alamat `http://localhost:8501`.

---

## 🌐 Live Streamlit Cloud
Dashboard ini dapat diakses secara daring pada tautan:
- **Direct Live Link:** [https://aboplkllac2wrlz5uxuk4s.streamlit.app/](https://aboplkllac2wrlz5uxuk4s.streamlit.app/)
- **Author:** Noval Berauh (ID Dicoding: `ds506b6y1389` | Email: `mikelizer123@gmail.com`)
- **Tautan berkas:** [url.txt](url.txt)
