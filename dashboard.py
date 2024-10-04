# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configurasi untuk tampilan Streamlit
st.set_page_config(page_title="Analisis Peminjaman Sepeda", layout="wide")
st.title("Dashboard Analisis Peminjaman Sepeda")

# Load dataset
day_df = pd.read_csv('c:/Users/Semoga Berkah/Documents/BANGKIT/bike-sharing-dataset/day.csv')
hour_df = pd.read_csv('c:/Users/Semoga Berkah/Documents/BANGKIT/bike-sharing-dataset/hour.csv')

# Format kolom datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan tanggal minimum dan maksimum dari dataset
min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")

# Menambahkan logo perusahaan atau gambar
st.sidebar.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")

# Input rentang waktu
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    value=(min_date_days, max_date_days),  # Mengatur default sebagai tuple
    min_value=min_date_days,
    max_value=max_date_days
)

# Filter data berdasarkan rentang waktu
filtered_day_df = day_df[(day_df["dteday"] >= pd.Timestamp(start_date)) & (day_df["dteday"] <= pd.Timestamp(end_date))]

# Total Jumlah Peminjaman Berdasarkan Rentang Waktu
total_count = filtered_day_df["cnt"].sum()
st.sidebar.metric(label="Total Peminjaman Sepeda", value=total_count)

# Pilihan analisis
option = st.sidebar.selectbox("Pilih Analisis", 
                              ("Pengaruh Kondisi Cuaca", "Tren Peminjaman Sepeda Harian"))

# Menampilkan deskripsi dataset jika checkbox dicentang
if st.sidebar.checkbox("Tampilkan Data"):
    st.write("Data Harian:")
    if not filtered_day_df.empty:  # Memastikan data tidak kosong
        st.write(filtered_day_df.head())
    else:
        st.write("Tidak ada data untuk rentang waktu yang dipilih.")
        
    st.write("Data Jam:")
    st.write(hour_df.head())

# Case 1: Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman
if option == "Pengaruh Kondisi Cuaca":
    st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda")

    # Mengelompokkan data berdasarkan kondisi cuaca untuk menghitung total peminjaman
    weather_data = filtered_day_df.groupby('weathersit').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    # Mengatur label kondisi cuaca
    weather_data['weathersit'] = weather_data['weathersit'].map({
        1: 'Cerah',
        2: 'Kabut',
        3: 'Hujan Ringan/Salju',
        4: 'Hujan Lebat'
    })

    # Membuat plot dengan ukuran lebih kecil dan font yang sesuai
    fig, ax = plt.subplots(figsize=(5, 3))  # Ukuran lebih kecil
    bar_width = 0.25
    x = np.arange(len(weather_data['weathersit']))

    # Menambahkan total peminjaman, kasual, dan terdaftar ke plot
    ax.bar(x - bar_width, weather_data['cnt'], width=bar_width, label='Total Peminjaman', color='skyblue')
    ax.bar(x, weather_data['casual'], width=bar_width, label='Pengguna Kasual', color='orange')
    ax.bar(x + bar_width, weather_data['registered'], width=bar_width, label='Pengguna Terdaftar', color='green')

    # Mengatur label dan judul dengan ukuran font yang lebih kecil
    ax.set_xticks(x)
    ax.set_xticklabels(weather_data['weathersit'], fontsize=8)
    ax.set_title('Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda', fontsize=10)
    ax.set_xlabel('Kondisi Cuaca', fontsize=9)
    ax.set_ylabel('Jumlah Peminjaman', fontsize=9)
    ax.legend(fontsize=7)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Menampilkan kesimpulan
    st.markdown("""
    Kesimpulan:
    - Cuaca cerah memiliki jumlah peminjaman sepeda tertinggi, terutama untuk pengguna kasual.
    - Cuaca buruk seperti hujan atau salju secara signifikan menurunkan jumlah peminjaman.
    - Pengguna terdaftar lebih cenderung tetap meminjam sepeda meskipun kondisi cuaca kurang baik.
    """)

# Case 2: Tren Peminjaman Sepeda Berdasarkan Jam dalam Sehari
elif option == "Tren Peminjaman Sepeda Harian":
    st.subheader("Tren Peminjaman Sepeda Berdasarkan Jam dalam Sehari")

    # Mengubah kolom 'workingday' agar lebih deskriptif
    hour_df['workingday'] = hour_df['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

    # Mengelompokkan data berdasarkan jam dan hari kerja
    hour_avg = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

    # Membuat plot dengan ukuran lebih kecil dan font yang sesuai
    fig, ax = plt.subplots(figsize=(6, 3))  # Ukuran lebih kecil
    sns.lineplot(data=hour_avg, x='hr', y='cnt', hue='workingday', marker='o', ax=ax, palette={"Akhir Pekan": 'orange', "Hari Kerja": 'blue'})
    ax.set_title('Tren Peminjaman Sepeda per Jam (Hari Kerja vs Akhir Pekan)', fontsize=10)
    ax.set_xlabel('Jam dalam Sehari', fontsize=9)
    ax.set_ylabel('Rata-rata Jumlah Peminjaman', fontsize=9)
    ax.legend(title='Tipe Hari', fontsize=7, title_fontsize='8')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Menampilkan kesimpulan
    st.markdown("""
    Kesimpulan:
    - Pada hari kerja, terdapat dua puncak peminjaman: pagi dan sore, yang menunjukkan pola penggunaan untuk komuter.
    - Pada akhir pekan, peminjaman lebih tinggi di tengah hari hingga sore, menunjukkan penggunaan untuk rekreasi.
    - Distribusi ini menunjukkan bahwa waktu dan hari sangat memengaruhi tren peminjaman sepeda.
    """)
