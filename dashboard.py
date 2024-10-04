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
day_df = pd.read_csv('c:/Users/Semoga Berkah/Documents/BANGKIT/day.csv')
hour_df = pd.read_csv('c:/Users/Semoga Berkah/Documents/BANGKIT/hour.csv')

# Format kolom datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
option = st.sidebar.selectbox("Pilih Analisis", 
                              ("Pengaruh Kondisi Cuaca", "Tren Peminjaman Sepeda Harian"))

# Menampilkan deskripsi dataset
if st.sidebar.checkbox("Tampilkan Data"):
    st.write("Data Harian:")
    st.write(day_df.head())
    st.write("Data Jam:")
    st.write(hour_df.head())

# Case 1: Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman
if option == "Pengaruh Kondisi Cuaca":
    st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda")

    # Mengelompokkan data berdasarkan kondisi cuaca untuk menghitung total peminjaman
    weather_data = day_df.groupby('weathersit').agg({
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

    # Membuat plot
    fig, ax = plt.subplots(figsize=(8, 4))
    bar_width = 0.35
    x = np.arange(len(weather_data['weathersit']))

    # Menambahkan total peminjaman, kasual, dan terdaftar ke plot
    ax.bar(x - bar_width, weather_data['cnt'], width=bar_width, label='Total Peminjaman', color='skyblue')
    ax.bar(x, weather_data['casual'], width=bar_width, label='Pengguna Kasual', color='orange')
    ax.bar(x + bar_width, weather_data['registered'], width=bar_width, label='Pengguna Terdaftar', color='green')

    # Mengatur label dan judul
    ax.set_xticks(x)
    ax.set_xticklabels(weather_data['weathersit'])
    ax.set_title('Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Peminjaman')
    ax.legend()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Menampilkan kesimpulan
    st.markdown("""
    **Kesimpulan**:
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

    # Membuat plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=hour_avg, x='hr', y='cnt', hue='workingday', marker='o', ax=ax, palette={"Akhir Pekan": 'orange', "Hari Kerja": 'blue'})
    ax.set_title('Tren Peminjaman Sepeda per Jam (Hari Kerja vs Akhir Pekan)')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.legend(title='Tipe Hari')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Menampilkan kesimpulan
    st.markdown("""
    **Kesimpulan**:
    - Pada hari kerja, terdapat dua puncak peminjaman: pagi dan sore, yang menunjukkan pola penggunaan untuk komuter.
    - Pada akhir pekan, peminjaman lebih tinggi di tengah hari hingga sore, menunjukkan penggunaan untuk rekreasi.
    - Distribusi ini menunjukkan bahwa waktu dan hari sangat memengaruhi tren peminjaman sepeda.
    """)

