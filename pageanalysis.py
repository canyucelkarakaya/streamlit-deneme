

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Birleştirilmiş veriyi oku
merged_df = pd.read_excel("merged_business_report.xlsx")

# Region sütunundaki değerleri say
region_counts = merged_df["Region"].value_counts()

# Streamlit ile grafiği çizme
st.title("Bölgelerin Dağılımı")
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# İlk pasta grafiği
ax[0].pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=140)
ax[0].set_title("Bölgelerin Dağılımı")
ax[0].axis('equal')  # Daire şeklinde görüntüleme

# İkinci pasta grafiği (sayısal değerleri gösteren)
ax[1].pie(region_counts, labels=region_counts.index, autopct=lambda p: '{:.0f}'.format(p * sum(region_counts) / 100), startangle=140)
ax[1].set_title("Bölgelerin Dağılımı (Sayılar)")
ax[1].axis('equal')  # Daire şeklinde görüntüleme

st.pyplot(fig)

# Bölgeleri ve toplam sayfa görüntülemelerini grupla
region_page_views = merged_df.groupby("Region")["Page Views - Total"].sum()

# Her bölgedeki tekrar sayılarını hesapla
region_counts = merged_df["Region"].value_counts()

# B2B sayfa görüntülemelerini topla
b2b_page_views = merged_df.groupby("Region")["Page Views - Total - B2B"].sum()

# Streamlit uygulamasını başlatın
st.title("Bölgelerin Analizi")

# Bir figür oluşturun
fig, ax = plt.subplots(figsize=(12, 6))

# Çubuk grafikteki sayıları üzerine ekleme
ax.bar(region_page_views.index, region_page_views, label='Toplam Sayfa Görüntülemeleri')
ax.bar(b2b_page_views.index, b2b_page_views, label='Toplam Sayfa Görüntülemeleri - B2B', alpha=0.7)
ax.set_title("Bölgelerin Toplam Sayfa Görüntülemeleri")
ax.set_xlabel("Bölge")
ax.set_ylabel("Toplam Sayfa Görüntülemeleri")
ax.set_xticklabels(region_page_views.index, rotation=45)

# Çubuk grafikteki sayıları üzerine ekleme
for i, val in enumerate(region_page_views):
    ax.text(i, val, str(val), ha='center', va='bottom', fontsize=10)

# Çubuk grafikteki B2B sayıları üzerine ekleme
for i, val in enumerate(b2b_page_views):
    ax.text(i, val, str(val), ha='center', va='top', fontsize=10)

# Sayıları görselleştirmek için ikinci bir eksen oluşturma
ax2 = ax.twinx()
ax2.plot(region_counts.index, region_counts.values, color='r', marker='o', label='Ürün Sayıları')
ax2.set_ylabel("Ürün Sayıları")

# Çizgi grafikteki sayıları üzerine ekleme
for i, txt in enumerate(region_counts.values):
    ax2.annotate(txt, (region_counts.index[i], region_counts.values[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Grafikleri gösterme
ax.legend(loc='upper right')
ax2.legend(loc='upper left')
st.pyplot(fig)





# Görüntülenme sayısı 0 olan ürünlerin sayısı
zero_page_views = merged_df[merged_df["Page Views - Total"] == 0].shape[0]
st.write(f"Görüntülenme sayısı 0 olan ürün sayısı: {zero_page_views}")

# Görüntülenme sayılarını gruplandırma
bins = [0, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
labels = ['0-10', '11-20', '21-50', '51-100', '101-200', '201-500', '501-1000', '1001-2000', '2001-5000', '5001-10000']
merged_df['Page Views Group'] = pd.cut(merged_df['Page Views - Total'], bins=bins, labels=labels)

# Gruplara göre ürün sayıları
group_counts = merged_df['Page Views Group'].value_counts().sort_index()

# Streamlit uygulamasını başlatın
st.title("Görüntülenme Sayılarına Göre Ürün Sayıları")

# Mağaza filtresi
selected_store = st.selectbox("Mağaza Seçin:", ["Tümü", "EKOZ-ja", "OZM-ca", "OZM-mx"])

# Seçilen mağazaya göre veriyi filtrele
if selected_store == "Tümü":
    filtered_df = merged_df
else:
    filtered_df = merged_df[merged_df["Region"] == selected_store]

# Filtrelenmiş veriyle gruplara göre ürün sayıları grafiği
fig, ax = plt.subplots(figsize=(10, 6))
group_counts_filtered = filtered_df['Page Views Group'].value_counts().sort_index()
bars = ax.bar(group_counts_filtered.index, group_counts_filtered)

# Çubukların üzerine sayıları ekleme
for bar in bars:
    yval = bar.get_height()
    ax.annotate(round(yval, 2), xy=(bar.get_x() + bar.get_width() / 2, yval), xytext=(0, 5), textcoords="offset points", ha='center', va='bottom')

ax.set_xlabel("Görüntülenme Sayısı Aralığı")
ax.set_ylabel("Ürün Sayısı")
ax.set_title(f"{selected_store} Mağazası Görüntülenme Sayılarına Göre Ürün Sayıları")
ax.set_xticklabels(group_counts_filtered.index, rotation=45)

st.pyplot(fig)


# EKOZ-ja bölgesini ve en yüksek sayfa görüntülemesine sahip ilk 50 satırı seç
ekoz_top_50 = merged_df[merged_df["Region"] == "EKOZ-ja"].nlargest(50, "Page Views - Total")

# Streamlit uygulamasını başlatın
st.title("EKOZ Mağazasına Ait En Yüksek Görüntülenmeye Sahip Ürünler")

# Ürün sayısı filtresi
product_count = st.slider("Kaç ürün görmek istersiniz?", 1, 50, 10)

# Ürün sayısını güncelle
ekoz_top_filtered = ekoz_top_50.head(product_count)

# Çubuk grafik oluştur
fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(ekoz_top_filtered["(Child) ASIN"], ekoz_top_filtered["Page Views - Total"], label="Page Views")
bars2 = ax.bar(ekoz_top_filtered["(Child) ASIN"], ekoz_top_filtered["Page Views Percentage - Total"], label="Page Views Percentage", alpha=0.5)
ax.set_xlabel("(Child) ASIN")
ax.set_ylabel("Değer")
ax.set_title(f"EKOZ Mağazasına Ait En Yüksek Görüntülenmeye Sahip İlk {product_count} Ürün")
ax.set_xticklabels(ekoz_top_filtered["(Child) ASIN"], rotation=45)
ax.legend()

# Sayısal değerleri çubukların üstüne ekle
for bar1, bar2 in zip(bars1, bars2):
    ax.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(), str(int(bar1.get_height())), ha="center", va="bottom")
    ax.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(), f"{bar2.get_height():.2f}", ha="center", va="bottom")

# Grafikleri göster
st.pyplot(fig)

# "Total Order Items" sutununda sıfırdan farklı değerlere sahip olan verileri seç
non_zero_total_order_items = merged_df[merged_df["Total Order Items"] != 0]

# Bölgelere göre gruplandırma ve sayıları sayma
region_counts = non_zero_total_order_items["Region"].value_counts()

# Streamlit uygulamasını başlatın
st.title("Bölgelere Göre Total Order Items Veri Sayısı")

# Bar grafik çizdirme
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(region_counts.index, region_counts)

ax.set_xlabel("Bölge")
ax.set_ylabel("Veri Sayısı")
ax.set_title("Bölgelere Göre Total Order Items Veri Sayısı")
plt.xticks(rotation=0)

# Çubukların üstüne sayıları ekle
for bar in bars:
    yval = bar.get_height()
    ax.annotate(round(yval, 2), xy=(bar.get_x() + bar.get_width() / 2, yval), xytext=(0, 5),
                textcoords="offset points", ha='center', va='bottom')

# Grafikleri göster
st.pyplot(fig)


# Görüntülenme sayısı en yüksek olan ilk 10 ürünü seç
top_page_views = merged_df.nlargest(10, "Page Views - Total")

# "AllKeepaReports" dosyasını oku
keepa_df = pd.read_excel("AllKeepaReports.xlsx")

# Resim URL'lerini ve bağlantılarını saklayacak bir liste oluşturun
image_links = []

# İlgili verileri yazdır
for idx, row in enumerate(top_page_views.iterrows(), start=1):
    child_asin = row[1]["(Child) ASIN"]
    region = row[1]["Region"]
    page_views = row[1]["Page Views - Total"]
    total_order_items = row[1]["Total Order Items"]
    
    keepa_row = keepa_df[keepa_df["ASIN"] == child_asin]
    if not keepa_row.empty:
        # Ürün bilgisi ve GÖRSEL bağlantısı
        st.write(f"{idx}. sırada - Child ASIN: {child_asin}, Region: {region}, Page Views: {page_views}, Total Order Items: {total_order_items}, [GÖRSEL]({keepa_row['Image'].values[0]})")
    else:
        st.write(f"{idx}. sırada - Child ASIN: {child_asin}, Region: {region}, Page Views: {page_views}, Total Order Items: {total_order_items}, Child ASIN keepareport datasında mevcut değildir.")


