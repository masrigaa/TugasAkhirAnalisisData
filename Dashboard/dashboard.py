import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

base_path = Path(__file__).parent

day_df = pd.read_csv(base_path / "day.csv")
wind_df = pd.read_csv(base_path / "windspd.csv")

st.title('Analisis Penyewaan Sepeda')
# sidebar
with st.sidebar:
    st.sidebar.title('Tentang :')
    st.sidebar.write("""
    **Nama**: Aslamul Fikri Alfirdausi  
    **Universitas**: Universitas Jenderal Achmad Yani  
    **Jurusan**: Informatika
    """)

# informasi data perbulan berdasar bulan
mounth_df = day_df.groupby(by=["mnth","yr"]).agg({
    "instant": "nunique",
    "cnt": "sum"
}).reset_index()

# Data PerTahun
year_df = day_df.groupby(by="yr").agg({
    "instant": "nunique",
    "cnt": "sum"
}).reset_index()

st.subheader('Jumlah Penyewa Sepeda Perbulan Dari 2011-2012')
year_2011 = year_df[year_df['yr'] == 0]['cnt'].sum()
year_2012 = year_df[year_df['yr'] == 1]['cnt'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Sewa Tahun 2011 :", value=year_2011)
with col2: 
    st.metric("Total Sewa Tahun 2012 :", value=year_2012)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='mnth', y='cnt',hue='yr', data=mounth_df, palette='Blues', ax=ax)
ax.set_title('Jumlah Penyewa Sepeda Per 2011-2012', fontsize=15)
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewa')
ax.set_xticks(range(12))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
st.pyplot(fig)

st.subheader("Total Penggunaan Berdasar bulan dan Hari Yg paling Sibuk")
col1, col2 = st.columns(2)

with col1 :
    monthly = day_df.groupby(by="mnth").agg({
        "instant": "nunique",
        "cnt": "sum"
    }).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='mnth', y='cnt', data=monthly, palette='Blues', ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda per Bulan")
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
    st.pyplot(fig)

with col2 :
    weekly = day_df.groupby(by="weekday").agg({
        "instant": "nunique",
        "cnt": "sum"
    }).reset_index()
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=weekly.index, y="cnt", data=weekly, palette=colors, ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda Berdasar Hari", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_xticks(ticks=range(7), labels=["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"], rotation=45)
    st.pyplot(fig)

st.subheader("Pengaruh Cuaca Terhadap Penyewaan sepeda")
weather = day_df.groupby(by="weathersit").agg({
    "instant": "nunique",
    "cnt": "sum"
})
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=weather.index, y="cnt", data=weather, palette=colors)
ax.set_title("Penyewa Sepeda Bergantung Cuaca", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Penyewa")
ax.set_xlabel(None)
ax.set_xticks(ticks=range(4), labels=["Clear", "Mist", "Light Snow", "Heavy Rain"], rotation=45)
st.pyplot(fig)

st.subheader("Pengaruh Kecepatan Angin Terhadap Penyewaan sepeda")
day_df["windspd_group"] = day_df.windspeed.apply(lambda x: "Low" if x <= 0.2 else ("Moderate" if x <= 1.0 else "High"))
windspd = day_df.groupby(by="windspd_group").agg({
    "instant": "nunique",
    "cnt": "sum"
})
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=windspd.index, y="cnt", data=windspd, palette=colors)
ax.set_title("Penyewa Sepeda Bergantung Kecepatan Angin", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Penyewa")
ax.set_xlabel(None)
ax.set_xticks(ticks=range(3), labels=["low", "Moderate", "High"], rotation=45)
st.pyplot(fig)

st.title("Kesimpulan Analisis :")
st.subheader("Bagaimana pola penggunaan sepeda selama satu tahun, dan hari apa yang paling sibuk untuk penggunaan sepeda?")
st.write("pola penyewaan sepeda bervariasi. Bulan-bulan di musim dingin penggunaan sepeda cenderung menurun,hari kerja cenderung lebih sibuk untuk penggunaan sepeda dibandingkan akhir pekan, dengan puncak penyewaan terjadi pada hari jumat")

st.subheader("Bagaimana pengaruh kondisi cuaca dan kecepatan angin terhadap jumlah penyewaan sepeda?")
st.write("cuaca yang baik dan angin yang tidak terlalu kencang memiliki dampak positif pada jumlah penyewaan sepeda.")
