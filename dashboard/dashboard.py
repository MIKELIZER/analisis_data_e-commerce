import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import folium
from streamlit_folium import st_folium

# Set Page Configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Set Seaborn Style
sns.set_theme(style="whitegrid")


@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_data.csv")
    df = pd.read_csv(data_path)
    date_cols = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


df_raw = load_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("🛒 Olist E-Commerce Analytics")
    st.markdown("**Noval Berauh | ID: ds506b6y1389**")
    st.caption("Email: mikelizer123@gmail.com")
    st.divider()

    st.subheader("Filter Data Interaktif")

    min_date = df_raw["order_purchase_timestamp"].min().date()
    max_date = df_raw["order_purchase_timestamp"].max().date()

    date_range = st.date_input(
        label="Rentang Tanggal Pembelian",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Handle single date selection safely without error
    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            start_date, end_date = date_range[0], date_range[1]
        elif len(date_range) == 1:
            start_date, end_date = date_range[0], date_range[0]
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date, end_date = date_range, date_range

    all_states = sorted(df_raw["customer_state"].dropna().unique().tolist())
    selected_states = st.multiselect(
        label="Pilih Negara Bagian (Customer State)",
        options=all_states,
        default=all_states
    )

    if not selected_states:
        selected_states = all_states

    st.divider()
    st.markdown(
        "**Tentang Dashboard:**\n"
        "Dashboard ini menyajikan evaluasi performa pengiriman logistik, perilaku pembayaran wilayah, "
        "serta segmentasi pelanggan (RFM, Manual Grouping, & Geospatial Analysis)."
    )

# Filter Main Dataframe
filtered_df = df_raw[
    (df_raw["order_purchase_timestamp"].dt.date >= start_date)
    & (df_raw["order_purchase_timestamp"].dt.date <= end_date)
    & (df_raw["customer_state"].isin(selected_states))
].copy()

# Deduplicate at order level for accurate order-level metrics
order_level_df = filtered_df.drop_duplicates(subset=["order_id"]).copy()

# ==================== HEADER & KPI METRICS ====================
st.title("📊 E-Commerce Executive Analytics Dashboard")
st.markdown(
    f"Menampilkan data transaksi periode **{start_date.strftime('%d %b %Y')}** hingga "
    f"**{end_date.strftime('%d %b %Y')}** pada **{len(selected_states)}** negara bagian."
)

total_orders = order_level_df["order_id"].nunique()
total_revenue = order_level_df["payment_value"].sum()
if len(order_level_df) > 0:
    ontime_rate = (order_level_df["delivery_status"] == "On Time").mean() * 100
    avg_review = order_level_df["review_score"].mean()
else:
    ontime_rate = 0.0
    avg_review = 0.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Total Orders", f"{total_orders:,}")
with kpi2:
    revenue_formatted = format_currency(total_revenue, "BRL", locale="pt_BR")
    st.metric("Total Revenue (BRL)", revenue_formatted)
with kpi3:
    st.metric("On-Time Delivery Rate", f"{ontime_rate:.2f}%")
with kpi4:
    st.metric("Average Review Score", f"{avg_review:.2f} / 5.00")

st.divider()

# ==================== BAGIAN 1: PERTANYAAN BISNIS 1 ====================
st.header("1. Analisis Keterlambatan Pengiriman & Kepuasan Pelanggan")
st.markdown(
    "**Fokus Evaluasi:** Dampak keterlambatan pengiriman (*Late* vs *On Time*) terhadap rata-rata "
    "skor ulasan pelanggan (`review_score`) pada 10 kategori produk dengan volume pesanan tertinggi."
)

toggle_2017 = st.checkbox(
    "Fokus khusus tahun 2017 (Sesuai Pertanyaan Bisnis 1 SMART)",
    value=False
)

q1_source = filtered_df[filtered_df["order_purchase_timestamp"].dt.year == 2017] if toggle_2017 else filtered_df

if len(q1_source) == 0:
    st.warning("Tidak ada data transaksi pada filter yang dipilih.")
else:
    top10_cats = (
        q1_source.groupby("product_category_name_english")["order_id"]
        .nunique()
        .nlargest(10)
        .index.tolist()
    )
    q1_top10 = q1_source[q1_source["product_category_name_english"].isin(top10_cats)].copy()
    q1_top10_orders = q1_top10.drop_duplicates(subset=["order_id", "product_category_name_english"])

    col_q1_left, col_q1_right = st.columns(2)

    with col_q1_left:
        st.subheader("Perbandingan Skor Ulasan: On Time vs Late")
        pivot_review = (
            q1_top10_orders.groupby(["product_category_name_english", "delivery_status"])["review_score"]
            .mean()
            .unstack()
            .reindex(top10_cats)
        )

        fig1, ax1 = plt.subplots(figsize=(9, 6))
        y_pos = np.arange(len(pivot_review.index))
        bar_height = 0.38

        ontime_vals = pivot_review["On Time"].fillna(0) if "On Time" in pivot_review.columns else np.zeros(len(y_pos))
        late_vals = pivot_review["Late"].fillna(0) if "Late" in pivot_review.columns else np.zeros(len(y_pos))

        bars_ontime = ax1.barh(
            y_pos - bar_height / 2,
            ontime_vals,
            height=bar_height,
            label="On Time",
            color="#1f77b4"
        )
        bars_late = ax1.barh(
            y_pos + bar_height / 2,
            late_vals,
            height=bar_height,
            label="Late",
            color="#e63946"
        )

        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(pivot_review.index, fontsize=10)
        ax1.invert_yaxis()
        ax1.set_xlim(0, 5.3)
        ax1.set_xlabel("Rata-Rata Review Score (Skala 1-5)", fontsize=10)
        ax1.set_title("Rata-Rata Review Score per Kategori (On Time vs Late)", fontsize=12, fontweight="bold")
        ax1.bar_label(bars_ontime, fmt="%.2f", padding=3, fontsize=8)
        ax1.bar_label(bars_late, fmt="%.2f", padding=3, fontsize=8)
        ax1.legend(loc="lower right")
        sns.despine(top=True, right=True, ax=ax1)
        plt.tight_layout()
        st.pyplot(fig1)

    with col_q1_right:
        st.subheader("Persentase Keterlambatan per Kategori Produk")
        delay_rate_df = (
            q1_top10_orders.groupby("product_category_name_english")
            .apply(lambda g: (g["delivery_status"] == "Late").mean() * 100, include_groups=False)
            .reindex(top10_cats)
            .sort_values(ascending=False)
        )

        fig2, ax2 = plt.subplots(figsize=(9, 6))
        colors_delay = ["#e63946" if i == 0 else "#d3d3d3" for i in range(len(delay_rate_df))]
        bars_delay = ax2.barh(
            delay_rate_df.index,
            delay_rate_df.values,
            color=colors_delay
        )
        ax2.invert_yaxis()
        ax2.set_xlim(0, max(delay_rate_df.values.max() * 1.18, 10))
        ax2.set_xlabel("Persentase Pengiriman Terlambat (%)", fontsize=10)
        ax2.set_title("Tingkat Keterlambatan Pengiriman pada 10 Kategori Teratas", fontsize=12, fontweight="bold")
        ax2.bar_label(bars_delay, fmt="%.2f%%", padding=3, fontsize=9)
        sns.despine(top=True, right=True, ax=ax2)
        plt.tight_layout()
        st.pyplot(fig2)

st.divider()

# ==================== BAGIAN 2: PERTANYAAN BISNIS 2 ====================
st.header("2. Analisis Metode Pembayaran & Wilayah (Credit Card vs Boleto)")
st.markdown(
    "**Fokus Evaluasi:** Perbandingan *Gross Merchandise Value* (GMV), *Average Order Value* (AOV), "
    "dan rata-rata jumlah cicilan (`payment_installments`) antara metode pembayaran `credit_card` dan `boleto` "
    "di 5 negara bagian dengan transaksi tertinggi."
)

toggle_h1_2018 = st.checkbox(
    "Fokus khusus Semester 1 Tahun 2018 (Jan - Jun 2018, Sesuai Pertanyaan Bisnis 2 SMART)",
    value=False
)

if toggle_h1_2018:
    q2_source = filtered_df[
        (filtered_df["order_purchase_timestamp"] >= "2018-01-01")
        & (filtered_df["order_purchase_timestamp"] <= "2018-06-30 23:59:59")
    ]
else:
    q2_source = filtered_df

q2_orders = q2_source.drop_duplicates(subset=["order_id"]).copy()
q2_orders = q2_orders[q2_orders["payment_type"].isin(["credit_card", "boleto"])]

if len(q2_orders) == 0:
    st.warning("Tidak ada transaksi Credit Card / Boleto pada rentang filter ini.")
else:
    top5_states = (
        q2_orders.groupby("customer_state")["payment_value"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )
    q2_top5 = q2_orders[q2_orders["customer_state"].isin(top5_states)].copy()

    q2_summary = (
        q2_top5.groupby(["customer_state", "payment_type"])
        .agg(
            total_gmv=("payment_value", "sum"),
            aov=("payment_value", "mean"),
            avg_installments=("payment_installments", "mean"),
            total_orders=("order_id", "nunique")
        )
        .reset_index()
    )

    col_q2_1, col_q2_2, col_q2_3 = st.columns(3)

    with col_q2_1:
        st.subheader("Total GMV (BRL)")
        pivot_gmv = (
            q2_summary.pivot(index="customer_state", columns="payment_type", values="total_gmv")
            .reindex(top5_states)
            .fillna(0)
        )
        fig3, ax3 = plt.subplots(figsize=(6, 5))
        x = np.arange(len(pivot_gmv.index))
        w = 0.36
        cc_gmv = pivot_gmv["credit_card"] / 1e3 if "credit_card" in pivot_gmv.columns else np.zeros(len(x))
        bl_gmv = pivot_gmv["boleto"] / 1e3 if "boleto" in pivot_gmv.columns else np.zeros(len(x))

        b1 = ax3.bar(x - w / 2, cc_gmv, width=w, label="Credit Card", color="#1f77b4")
        b2 = ax3.bar(x + w / 2, bl_gmv, width=w, label="Boleto", color="#d3d3d3")
        ax3.set_xticks(x)
        ax3.set_xticklabels(pivot_gmv.index)
        ax3.set_ylabel("Total GMV (Ribu BRL)")
        ax3.set_title("Total GMV (Ribu BRL) per Negara Bagian", fontsize=11, fontweight="bold")
        ax3.bar_label(b1, fmt="%.1fK", padding=2, fontsize=8)
        ax3.bar_label(b2, fmt="%.1fK", padding=2, fontsize=8)
        ax3.legend()
        sns.despine(top=True, right=True, ax=ax3)
        plt.tight_layout()
        st.pyplot(fig3)

    with col_q2_2:
        st.subheader("Average Order Value (BRL)")
        pivot_aov = (
            q2_summary.pivot(index="customer_state", columns="payment_type", values="aov")
            .reindex(top5_states)
            .fillna(0)
        )
        fig4, ax4 = plt.subplots(figsize=(6, 5))
        x = np.arange(len(pivot_aov.index))
        cc_aov = pivot_aov["credit_card"] if "credit_card" in pivot_aov.columns else np.zeros(len(x))
        bl_aov = pivot_aov["boleto"] if "boleto" in pivot_aov.columns else np.zeros(len(x))

        b3 = ax4.bar(x - w / 2, cc_aov, width=w, label="Credit Card", color="#1f77b4")
        b4 = ax4.bar(x + w / 2, bl_aov, width=w, label="Boleto", color="#d3d3d3")
        ax4.set_xticks(x)
        ax4.set_xticklabels(pivot_aov.index)
        ax4.set_ylabel("AOV (BRL)")
        ax4.set_title("Rata-Rata Nilai Pesanan (AOV)", fontsize=11, fontweight="bold")
        ax4.bar_label(b3, fmt="%.1f", padding=2, fontsize=8)
        ax4.bar_label(b4, fmt="%.1f", padding=2, fontsize=8)
        ax4.legend()
        sns.despine(top=True, right=True, ax=ax4)
        plt.tight_layout()
        st.pyplot(fig4)

    with col_q2_3:
        st.subheader("Rata-Rata Jumlah Cicilan")
        cc_inst = (
            q2_summary[q2_summary["payment_type"] == "credit_card"]
            .set_index("customer_state")["avg_installments"]
            .reindex(top5_states)
            .fillna(0)
        )
        fig5, ax5 = plt.subplots(figsize=(6, 5))
        max_idx = cc_inst.values.argmax() if len(cc_inst) > 0 else 0
        inst_colors = ["#1f77b4" if i == max_idx else "#d3d3d3" for i in range(len(cc_inst))]
        b5 = ax5.bar(cc_inst.index, cc_inst.values, color=inst_colors)
        ax5.set_ylabel("Rata-Rata Tenor Cicilan (Kali)")
        ax5.set_title("Rata-Rata Cicilan Kartu Kredit per State", fontsize=11, fontweight="bold")
        ax5.bar_label(b5, fmt="%.2fx", padding=2, fontsize=9)
        sns.despine(top=True, right=True, ax=ax5)
        plt.tight_layout()
        st.pyplot(fig5)

st.divider()

# ==================== BAGIAN 3: ANALISIS LANJUTAN ====================
st.header("3. Analisis Lanjutan (RFM, Segmentasi Pelanggan, & Geospasial)")

tab_rfm, tab_seg, tab_geo = st.tabs([
    "📈 RFM Analysis",
    "🎯 Customer Segmentation (Manual Grouping)",
    "🗺️ Peta Geospasial Brasil"
])

# Compute RFM on order_level_df
if len(order_level_df) > 0:
    reference_date = order_level_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm_df = (
        order_level_df.groupby("customer_unique_id")
        .agg(
            Recency=("order_purchase_timestamp", lambda x: (reference_date - x.max()).days),
            Frequency=("order_id", "nunique"),
            Monetary=("payment_value", "sum")
        )
        .reset_index()
    )
    rfm_df["short_id"] = rfm_df["customer_unique_id"].str[:8]

    # Manual Grouping / Binning using quartiles & rules
    r_quartiles = rfm_df["Recency"].quantile([0.25, 0.50, 0.75]).to_dict()
    m_quartiles = rfm_df["Monetary"].quantile([0.25, 0.50, 0.75]).to_dict()

    def r_score_func(x):
        if x <= r_quartiles[0.25]:
            return 4
        elif x <= r_quartiles[0.50]:
            return 3
        elif x <= r_quartiles[0.75]:
            return 2
        return 1

    def f_score_func(x):
        if x >= 3:
            return 4
        elif x == 2:
            return 3
        return 2

    def m_score_func(x):
        if x >= m_quartiles[0.75]:
            return 4
        elif x >= m_quartiles[0.50]:
            return 3
        elif x >= m_quartiles[0.25]:
            return 2
        return 1

    rfm_df["R_Score"] = rfm_df["Recency"].apply(r_score_func)
    rfm_df["F_Score"] = rfm_df["Frequency"].apply(f_score_func)
    rfm_df["M_Score"] = rfm_df["Monetary"].apply(m_score_func)
    rfm_df["RFM_Total"] = rfm_df["R_Score"] + rfm_df["F_Score"] + rfm_df["M_Score"]

    def assign_segment(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
        if r >= 3 and (f >= 3 or m == 4):
            return "Champions"
        elif r >= 3 and m >= 3:
            return "Loyal Customers"
        elif r >= 3 and m <= 2:
            return "Potential Loyalists"
        elif r == 2:
            return "At Risk"
        else:
            return "Lost"

    rfm_df["Segment"] = rfm_df.apply(assign_segment, axis=1)

    with tab_rfm:
        st.subheader("Top 5 Pelanggan Berdasarkan Recency, Frequency, dan Monetary")
        c_r, c_f, c_m = st.columns(3)
        with c_r:
            st.metric("Rata-Rata Recency (Hari)", f"{rfm_df['Recency'].mean():.1f}")
        with c_f:
            st.metric("Rata-Rata Frequency (Order)", f"{rfm_df['Frequency'].mean():.2f}")
        with c_m:
            st.metric("Rata-Rata Monetary (BRL)", f"R$ {rfm_df['Monetary'].mean():.2f}")

        fig_rfm, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Top 5 Recency (lowest days)
        top_r = rfm_df.nsmallest(5, "Recency")
        colors_r = ["#1f77b4" if i == 0 else "#d3d3d3" for i in range(len(top_r))]
        b_r = axes[0].bar(top_r["short_id"], top_r["Recency"], color=colors_r)
        axes[0].set_title("By Recency (Hari Terkecil)", fontweight="bold")
        axes[0].set_ylabel("Recency (Hari)")
        axes[0].bar_label(b_r, fmt="%d", padding=2)
        sns.despine(top=True, right=True, ax=axes[0])

        # Top 5 Frequency
        top_f = rfm_df.nlargest(5, "Frequency")
        colors_f = ["#1f77b4" if i == 0 else "#d3d3d3" for i in range(len(top_f))]
        b_f = axes[1].bar(top_f["short_id"], top_f["Frequency"], color=colors_f)
        axes[1].set_title("By Frequency (Pesanan Terbanyak)", fontweight="bold")
        axes[1].set_ylabel("Frequency (Jumlah Order)")
        axes[1].bar_label(b_f, fmt="%d", padding=2)
        sns.despine(top=True, right=True, ax=axes[1])

        # Top 5 Monetary
        top_m = rfm_df.nlargest(5, "Monetary")
        colors_m = ["#1f77b4" if i == 0 else "#d3d3d3" for i in range(len(top_m))]
        b_m = axes[2].bar(top_m["short_id"], top_m["Monetary"], color=colors_m)
        axes[2].set_title("By Monetary (Total Belanja BRL)", fontweight="bold")
        axes[2].set_ylabel("Monetary (BRL)")
        axes[2].bar_label(b_m, fmt="%.0f", padding=2)
        sns.despine(top=True, right=True, ax=axes[2])

        plt.tight_layout()
        st.pyplot(fig_rfm)

    with tab_seg:
        st.subheader("Distribusi Segmen Pelanggan (Manual Grouping / Binning)")
        seg_counts = rfm_df["Segment"].value_counts()
        fig_seg, ax_seg = plt.subplots(figsize=(10, 5))
        colors_seg = ["#1f77b4" if i == 0 else "#d3d3d3" for i in range(len(seg_counts))]
        bars_seg = ax_seg.barh(seg_counts.index, seg_counts.values, color=colors_seg)
        ax_seg.invert_yaxis()
        ax_seg.set_xlabel("Jumlah Pelanggan Unik")
        ax_seg.set_title("Distribusi Segmen Pelanggan Berdasarkan Aturan Kuartil RFM", fontweight="bold")
        ax_seg.bar_label(bars_seg, fmt="%d", padding=4)
        ax_seg.set_xlim(0, seg_counts.values.max() * 1.15)
        sns.despine(top=True, right=True, ax=ax_seg)
        plt.tight_layout()
        st.pyplot(fig_seg)

        seg_table = (
            rfm_df.groupby("Segment")
            .agg(
                Jumlah_Pelanggan=("customer_unique_id", "count"),
                Rata_Recency_Hari=("Recency", "mean"),
                Rata_Frequency=("Frequency", "mean"),
                Rata_Monetary_BRL=("Monetary", "mean")
            )
            .reset_index()
        )
        seg_table["Persentase (%)"] = (seg_table["Jumlah_Pelanggan"] / len(rfm_df) * 100).round(2)
        st.dataframe(seg_table)

    with tab_geo:
        st.subheader("Kepadatan Transaksi & Rata-Rata Keterlambatan per Negara Bagian di Brasil")
        geo_state = (
            order_level_df.dropna(subset=["geolocation_lat", "geolocation_lng"])
            .groupby("customer_state")
            .agg(
                lat=("geolocation_lat", "median"),
                lng=("geolocation_lng", "median"),
                total_orders=("order_id", "nunique"),
                late_rate=("delivery_status", lambda s: (s == "Late").mean() * 100),
                avg_delay=("delivery_delay_days", "mean")
            )
            .reset_index()
        )

        m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="OpenStreetMap")
        for _, row in geo_state.iterrows():
            color = "#e63946" if row["late_rate"] > 10 else "#1f77b4"
            radius = max(float(np.sqrt(row["total_orders"]) / 8), 5.0)
            popup_html = (
                f"<b>State: {row['customer_state']}</b><br>"
                f"Total Orders: {int(row['total_orders']):,}<br>"
                f"Late Delivery Rate: {row['late_rate']:.2f}%<br>"
                f"Avg Delay Days: {row['avg_delay']:.2f} hari"
            )
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=folium.Popup(popup_html, max_width=250)
            ).add_to(m)

        st_folium(m, width=1000, height=500)
else:
    st.warning("Tidak ada data untuk dianalisis.")

