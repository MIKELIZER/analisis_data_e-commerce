# Product Requirements Document (PRD): Proyek Analisis Data E-Commerce (Target: Bintang 5)

## 1. Identitas Peserta (Wajib Ditulis di Sel Pertama `notebook.ipynb`)
Buat sel Markdown paling atas di `notebook.ipynb` dengan format persis seperti ini:
- **Nama:** Noval Berauh
- **Email:** mikelizer123@gmail.com
- **ID Dicoding:** ds506b6y1389

## 2. Struktur Direktori Target
Pastikan struktur folder proyek mengikuti standar berikut:
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

## 3. Aturan Kritis Penilaian Bintang 5 (Wajib Dipatuhi AI Agent)
1. **DILARANG menggunakan algoritma Machine Learning** (seperti K-Means / Scikit-Learn). Untuk analisis lanjutan, wajib gunakan kombinasi **RFM Analysis**, **Manual Grouping / Binning** (`pd.cut` atau aturan kuartil), dan **Geospatial Analysis**.
2. **Wajib ada sel Markdown `**Insight:**` berisi angka konkret** (bukan placeholder) di akhir SETIAP tahapan pada `notebook.ipynb`:
   - Gathering Data
   - Assessing Data
   - Cleaning Data
   - Exploratory Data Analysis (EDA)
   - Visualization & Explanatory Analysis
   - Analisis Lanjutan (Advanced Analysis)
3. **Prinsip Desain & Integritas Visualisasi**:
   - Gunakan `seaborn` dan `matplotlib`.
   - Terapkan *color highlighting*: Beri warna kontras utama (`#1f77b4` atau `#e63946` untuk metrik negatif seperti keterlambatan) pada bar tertinggi/utama, dan warna abu-abu muda (`#d3d3d3`) pada bar lainnya.
   - Hapus border atas dan kanan (`sns.despine()`), tambahkan label nilai pada bar (`ax.bar_label()`), serta pastikan judul dan label sumbu X/Y jelas dan tidak bertumpuk.
4. **Optimasi Ukuran `dashboard/main_data.csv`**:
   - Jangan melakukan raw merge pada `geolocation_dataset.csv` (1 juta baris).
   - Lakukan agregasi `groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].median().reset_index()` terlebih dahulu, lalu gabungkan ke data utama yang sudah difilter (`order_status == 'delivered'`) agar ukuran `dashboard/main_data.csv` ramping (< 25 MB) dan tidak memicu Memory Limit di Streamlit Cloud.
5. **Eksekusi Notebook Otomatis**:
   - Setelah menyusun `notebook.ipynb`, jalankan notebook tersebut (misalnya dengan `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb`) agar seluruh output tabel, grafik, dan file `dashboard/main_data.csv` benar-benar terbentuk dan tersimpan di dalam `.ipynb`.

## 4. Pertanyaan Bisnis (Metode SMART)
Tuliskan kedua pertanyaan bisnis ini beserta penjabaran eksplisit elemen **S-M-A-R-T** (Specific, Measurable, Action-Oriented, Relevant, Time-bound) di sel Markdown `notebook.ipynb`:

- **Pertanyaan 1 (Operasional Logistik & Kepuasan Pelanggan):**
  "Seberapa besar penurunan rata-rata skor ulasan pelanggan (`review_score`) pada pesanan yang mengalami keterlambatan pengiriman (*actual delivery > estimated delivery*) dibandingkan pengiriman tepat waktu pada 10 kategori produk dengan volume pesanan tertinggi sepanjang tahun 2017?"
  - *Specific*: Fokus pada selisih `review_score` antara pesanan terlambat vs tepat waktu di 10 kategori produk teratas.
  - *Measurable*: Diukur menggunakan rata-rata skor ulasan (skala 1-5) dan persentase keterlambatan pengiriman.
  - *Action-Oriented*: Memberikan dasar keputusan bagi tim operasional/logistik untuk mengevaluasi SLA kurir pada kategori produk yang paling terdampak.
  - *Relevant*: Kepuasan pelanggan dan ketepatan waktu pengiriman adalah faktor kunci retensi di platform e-commerce.
  - *Time-bound*: Dibatasi secara spesifik pada transaksi sepanjang tahun 2017 (1 Januari 2017 – 31 Desember 2017).

- **Pertanyaan 2 (Perilaku Pembayaran & Nilai Transaksi Wilayah):**
  "Bagaimana perbandingan total nilai transaksi (*Gross Merchandise Value*), rata-rata nilai pesanan (*Average Order Value*), dan rata-rata jumlah cicilan (`payment_installments`) antara metode pembayaran Kartu Kredit (`credit_card`) dan `boleto` di 5 negara bagian (`customer_state`) dengan transaksi tertinggi selama Semester 1 tahun 2018 (Januari – Juni 2018)?"
  - *Specific*: Membandingkan metode pembayaran `credit_card` dan `boleto` di 5 negara bagian terbesar.
  - *Measurable*: Diukur melalui total `payment_value` (BRL), AOV (BRL), dan rata-rata `payment_installments`.
  - *Action-Oriented*: Mengarahkan tim *marketing* dan *partnership* perbankan dalam merancang promo cicilan kartu kredit atau diskon *checkout* boleto di wilayah terkait.
  - *Relevant*: Optimasi metode pembayaran berdampak langsung pada *conversion rate* dan peningkatan ukuran keranjang belanja (*basket size*).
  - *Time-bound*: Dibatasi pada periode Semester 1 tahun 2018 (1 Januari 2018 – 30 Juni 2018).

## 5. Spesifikasi Teknis `notebook.ipynb`
Ikuti kerangka templat resmi secara berurutan:
1. **Header Identitas & Menentukan Pertanyaan Bisnis** (lengkap dengan penjabaran SMART).
2. **Import Semua Packages/Library yang Digunakan** (`pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`, `folium` / `datetime`).
3. **Data Wrangling**:
   - *Gathering Data*: Muat ke-9 CSV dari folder `data/` dan tampilkan `.head()` masing-masing beserta Markdown `**Insight:**`.
   - *Assessing Data*: Periksa `.info()`, `.isna().sum()`, `.duplicated().sum()`, dan `.describe()`. Rangkum minimal 3 masalah kualitas data di Markdown `**Insight:**`:
     1. *Duplicate data*: Terdapat 261.831 baris duplikat pada `geolocation_dataset.csv`.
     2. *Missing values*: Terdapat 2.965 missing values pada `order_delivered_customer_date` di `orders_dataset`, 610 missing values pada `product_category_name` di `products_dataset`, dan missing comments pada `order_reviews_dataset`.
     3. *Inaccurate data types*: Kolom tanggal (`order_purchase_timestamp`, `order_delivered_customer_date`, `order_estimated_delivery_date`) pada `orders_dataset` masih bertipe `object` (string).
   - *Cleaning Data*:
     - Drop duplikat pada `geolocation` dan agregasikan `lat`/`lng` menggunakan median per `zip_code_prefix`.
     - Konversi seluruh kolom timestamp di `orders` menjadi `datetime`.
     - Isi missing `product_category_name` dengan `'unknown'` dan gabungkan dengan `product_category_name_translation`.
     - Hitung `delivery_delay_days = (order_delivered_customer_date - order_estimated_delivery_date).dt.days` dan buat kolom kategorikal `delivery_status` (`'Late'` jika `delivery_delay_days > 0`, selain itu `'On Time'`).
     - Gabungkan tabel utama (`orders`, `order_items`, `order_payments`, `order_reviews`, `products`, `customers`, dan koordinat `geolocation`) serta simpan hasilnya ke `dashboard/main_data.csv`. Tulis Markdown `**Insight:**`.
4. **Exploratory Data Analysis (EDA)**:
   - Eksplorasi distribusi status pesanan, demografi pelanggan per negara bagian (`customer_state`), statistik `delivery_delay_days`, tabel pivot Pertanyaan 1 (10 kategori teratas di 2017: `On Time` vs `Late` beserta rata-rata `review_score`), dan tabel agregasi Pertanyaan 2 (Semester 1 2018: `credit_card` vs `boleto` di 5 state teratas). Akhiri dengan Markdown `**Insight:**` yang memuat angka hasil agregasi.
5. **Visualization & Explanatory Analysis**:
   - *Visualisasi Pertanyaan 1*: Buat 2 grafik pendukung (misal: *Grouped Horizontal Bar Chart* perbandingan rata-rata `review_score` antara pengiriman `On Time` vs `Late` pada 10 kategori produk teratas di 2017, serta grafik persentase keterlambatan per kategori).
   - *Visualisasi Pertanyaan 2*: Buat visualisasi perbandingan Total GMV, AOV, dan rata-rata cicilan antara `credit_card` dan `boleto` di 5 negara bagian tertinggi selama Semester 1 2018.
   - Tulis Markdown `**Insight:**` yang tajam di bawah setiap visualisasi.
6. **Analisis Lanjutan (Advanced Analysis - Tanpa Machine Learning)**:
   - Tulis penjelasan tujuan masing-masing metode di sel Markdown sebelum kodenya.
   - *RFM Analysis*: Hitung `Recency` (hari sejak transaksi terakhir pelanggan terhadap tanggal maksimum dataset), `Frequency` (jumlah `order_id` unik per `customer_unique_id`), dan `Monetary` (total `payment_value` per `customer_unique_id`). Visualisasikan Top 5 pelanggan untuk Recency, Frequency, dan Monetary dalam 3 *subplot* berdampingan.
   - *Clustering via Manual Grouping / Binning*: Kelompokkan pelanggan berdasarkan skor RFM menjadi segmen bisnis (`Champions`, `Loyal Customers`, `Potential Loyalists`, `At Risk`, `Lost`) menggunakan aturan persentil/kuartil tanpa algoritma ML, lalu buat *Horizontal Bar Chart* distribusi segmen pelanggan.
   - *Geospatial Analysis*: Buat visualisasi kepadatan transaksi dan rata-rata keterlambatan pengiriman berdasarkan koordinat geografis (`geolocation_lat`, `geolocation_lng`) di wilayah Brasil.
   - Tutup dengan Markdown `**Insight:**`.
7. **Conclusion & Recommendation**:
   - *Conclusion*: Minimal 2 paragraf kesimpulan yang menjawab secara spesifik Pertanyaan Bisnis 1 dan Pertanyaan Bisnis 2 lengkap dengan metrik/angkanya.
   - *Recommendation*: Minimal 3 *Action Items* konkret yang dapat dieksekusi oleh bisnis berdasarkan hasil analisis.

## 6. Spesifikasi Teknis `dashboard/dashboard.py`
- Baca file `main_data.csv` menggunakan path dinamis:
  `os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_data.csv")`
- Gunakan `st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")`.
- **Sidebar**: Tampilkan identitas (`Noval Berauh | ID: ds506b6y1389`), filter rentang tanggal (`st.date_input`), dan filter `customer_state` (`st.multiselect`). Pastikan dashboard tidak error jika pengguna baru memilih 1 tanggal pada `st.date_input`.
- **Main Content**:
  1. Baris KPI utama menggunakan `st.metric` (Total Orders, Total Revenue BRL, On-Time Delivery Rate %, Average Review Score).
  2. Bagian 1: Analisis Keterlambatan Pengiriman & Kepuasan Pelanggan (Visualisasi Pertanyaan 1).
  3. Bagian 2: Analisis Metode Pembayaran & Wilayah (Visualisasi Pertanyaan 2).
  4. Bagian 3: Analisis Lanjutan (Tab untuk RFM Analysis, Customer Segmentation Manual Grouping, dan Peta Geospasial).

## 7. Spesifikasi `requirements.txt` & `README.md`
- `requirements.txt`: Hanya tulis library yang dipakai (`pandas`, `numpy`, `matplotlib`, `seaborn`, `streamlit`, `babel`, `folium`, `streamlit-folium`) tanpa library bawaan OS lokal.
- `README.md`: Buat panduan profesional berisi deskripsi proyek, struktur folder, instruksi instalasi dependencies (`pip install -r requirements.txt`), dan perintah menjalankan dashboard (`streamlit run dashboard/dashboard.py`).