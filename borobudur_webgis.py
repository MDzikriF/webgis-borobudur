import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Peta Interaktif Zonasi Konservasi Borobudur",
    page_icon="🏛️",
    layout="wide"
)

# Title dan deskripsi
st.title("🏛️ Peta Interaktif Zonasi Konservasi dan Aksesibilitas Wisata Edukasi Situs Purbakala")
st.markdown("**Studi Kasus: Candi Borobudur, Magelang, Jawa Tengah**")

# ============================================================================
# DATA DUMMY PREPARATION (Simulasi hasil analisis spasial di QGIS)
# ============================================================================

# Koordinat Candi Borobudur
borobudur_center = {"lat": -7.6075, "lon": 110.2039}

# 1. DATA SITUS UTAMA (Candi Borobudur)
sites_data = {
    "name": ["Candi Borobudur - Kompleks Utama"],
    "century": ["Abad 8"],
    "kingdom": ["Kerajaan Syailendra"],
    "status": ["Warisan Dunia UNESCO"],
    "risk_level": ["Sedang"],
    "geometry": [Point(borobudur_center["lon"], borobudur_center["lat"])]
}
sites_gdf = gpd.GeoDataFrame(sites_data, crs="EPSG:4326")

# 2. DATA ZONA PENYANGGA (Buffer Zone - 1km dan 2km)
def create_buffer_circle(center_lon, center_lat, radius_km):
    """Buat circle buffer dalam derajat (approximation)"""
    # 1 degree ≈ 111 km
    radius_deg = radius_km / 111.0
    points = []
    for angle in np.linspace(0, 360, 64):
        rad = np.radians(angle)
        lon = center_lon + radius_deg * np.cos(rad)
        lat = center_lat + radius_deg * np.sin(rad)
        points.append((lon, lat))
    return Polygon(points)

buffer_zone_data = {
    "zone_type": ["Buffer 500m - Zona Ketat", "Buffer 1km - Zona Terbatas", "Buffer 2km - Zona Pengawasan"],
    "capacity": ["0 (Larangan Penuh)", "Terbatas", "Terbatas Moderat"],
    "description": [
        "Area dengan risiko getaran tertinggi. Tidak boleh ada konstruksi baru.",
        "Area dengan risiko getaran sedang. Aktivitas wisata terbatas.",
        "Area dengan risiko getaran rendah. Pengembangan pariwisata terukur."
    ],
    "geometry": [
        create_buffer_circle(borobudur_center["lon"], borobudur_center["lat"], 0.5),
        create_buffer_circle(borobudur_center["lon"], borobudur_center["lat"], 1.0),
        create_buffer_circle(borobudur_center["lon"], borobudur_center["lat"], 2.0)
    ]
}
buffer_gdf = gpd.GeoDataFrame(buffer_zone_data, crs="EPSG:4326")

# 3. DATA FASILITAS WISATA & EDUKASI
facilities_data = {
    "name": [
        "Pusat Informasi Borobudur",
        "Museum Borobudur",
        "Rumah Sakit (Magelang)",
        "Hotel Amanjiwo",
        "Pos Parkir Utama"
    ],
    "facility_type": [
        "Pusat Informasi",
        "Museum Edukasi",
        "Layanan Kesehatan",
        "Akomodasi Wisata",
        "Fasilitas Pendukung"
    ],
    "capacity": [100, 200, 120, 60, 500],
    "service": [
        "Panduan wisata, peta, informasi UNESCO",
        "Artefak Borobudur, sejarah Dinasti Syailendra",
        "Layanan darurat untuk pengunjung",
        "Penginapan luxury dengan pemandangan Borobudur",
        "Parkir kendaraan pengunjung"
    ],
    "geometry": [
        Point(110.2050, -7.6100),
        Point(110.2080, -7.6120),
        Point(110.1950, -7.6000),
        Point(110.2200, -7.5900),
        Point(110.2100, -7.6200)
    ]
}
facilities_gdf = gpd.GeoDataFrame(facilities_data, crs="EPSG:4326")

# 4. DATA POS PEMANTAUAN/PENJAGA SITUS
monitoring_data = {
    "name": [
        "Pos Pengawas Utama (Barat Laut)",
        "Pos Pengawas (Timur Laut)",
        "Pos Pemantauan Struktural",
        "Pos Keamanan (Selatan)"
    ],
    "patrol_schedule": [
        "24/7",
        "08:00-18:00",
        "Monitoring otomatis + visual 12 jam",
        "Pemeriksaan keliling setiap jam"
    ],
    "status": ["Aktif", "Aktif", "Aktif", "Aktif"],
    "geometry": [
        Point(110.1950, -7.6000),
        Point(110.2150, -7.5950),
        Point(110.2100, -7.6100),
        Point(110.2050, -7.6200)
    ]
}
monitoring_gdf = gpd.GeoDataFrame(monitoring_data, crs="EPSG:4326")

# 5. DATA CANDI LAIN DI SEKITAR BOROBUDUR (untuk filter periodisasi)
other_temples = {
    "name": ["Candi Mendut", "Candi Pawon", "Candi Ngawen"],
    "century": ["Abad 8", "Abad 8", "Abad 8"],
    "kingdom": ["Kerajaan Syailendra", "Kerajaan Syailendra", "Kerajaan Mataram Kuno"],
    "period": ["Buddha", "Buddha", "Hindu-Buddha"],
    "status": ["Terpelihara", "Terpelihara", "Terawat"],
    "risk_level": ["Rendah", "Rendah", "Sedang"],
    "geometry": [
        Point(110.1950, -7.6300),
        Point(110.2100, -7.6400),
        Point(110.1850, -7.6100)
    ]
}
other_temples_gdf = gpd.GeoDataFrame(other_temples, crs="EPSG:4326")

# ============================================================================
# SIDEBAR UNTUK FILTER & KONTROL
# ============================================================================

st.sidebar.header("⚙️ Kontrol Peta")

# Layer visibility toggles
show_site = st.sidebar.checkbox("📍 Situs Candi Utama", value=True)
show_buffer = st.sidebar.checkbox("🔴 Zona Buffer/Kerentanan", value=True)
show_facilities = st.sidebar.checkbox("🟢 Fasilitas Wisata & Edukasi", value=True)
show_monitoring = st.sidebar.checkbox("🔵 Pos Pemantauan/Penjaga", value=True)
show_other_temples = st.sidebar.checkbox("🏯 Candi Lain di Sekitar", value=True)

# Filter berdasarkan periodisasi
st.sidebar.subheader("Filter Periodisasi Historis")
periods = st.sidebar.multiselect(
    "Pilih periode candi yang ingin ditampilkan:",
    options=["Hindu", "Buddha", "Hindu-Buddha"],
    default=["Hindu", "Buddha", "Hindu-Buddha"]
)

# ============================================================================
# PEMBUAT PETA FOLIUM INTERAKTIF
# ============================================================================

def create_interactive_map(
    sites_gdf, buffer_gdf, facilities_gdf, monitoring_gdf, other_temples_gdf,
    show_site, show_buffer, show_facilities, show_monitoring, show_other_temples,
    selected_periods
):
    """Buat peta Folium dengan styling dan pop-up interaktif"""
    
    # Inisialisasi peta dengan center di Borobudur
    m = folium.Map(
        location=[borobudur_center["lat"], borobudur_center["lon"]],
        zoom_start=14,
        tiles="OpenStreetMap",
        control_scale=True
    )
    
    # ===== LAYER 1: SITUS UTAMA (MERAH) =====
    if show_site:
        for idx, row in sites_gdf.iterrows():
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="color: #C41E3A; margin: 5px 0;">{row['name']}</h4>
                <hr style="margin: 5px 0;">
                <b>Abad Pembuatan:</b> {row['century']}<br>
                <b>Kerajaan/Dinasti:</b> {row['kingdom']}<br>
                <b>Status Konservasi:</b> <span style="color: green; font-weight: bold;">{row['status']}</span><br>
                <b>Tingkat Risiko:</b> <span style="color: orange;">{row['risk_level']}</span><br>
                <b>Koordinat:</b> {row['geometry'].y:.4f}, {row['geometry'].x:.4f}
            </div>
            """
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=15,
                popup=folium.Popup(popup_html, max_width=300),
                color="darkred",
                fill=True,
                fillColor="#C41E3A",
                fillOpacity=0.8,
                weight=3,
                tooltip="Klik untuk detail: Candi Borobudur"
            ).add_to(m)
    
    # ===== LAYER 2: ZONA BUFFER (ORANYE/KUNING dengan Gradasi) =====
    if show_buffer:
        colors = ["#FF4500", "#FFA500", "#FFD700"]  # OrangeRed, Orange, Gold
        labels = ["Buffer 500m - Zona Ketat", "Buffer 1km - Zona Terbatas", "Buffer 2km - Zona Pengawasan"]
        
        for idx, (color, label) in enumerate(zip(colors, labels)):
            row = buffer_gdf.iloc[idx]
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="color: {color}; margin: 5px 0;">{label}</h4>
                <hr style="margin: 5px 0;">
                <b>Deskripsi:</b> {row['description']}<br>
                <b>Kapasitas Kunjungan:</b> {row['capacity']}<br>
                <b>Status:</b> Zona konservasi aktif
            </div>
            """
            folium.GeoJson(
                gpd.GeoSeries([row['geometry']]).__geo_interface__,
                style_function=lambda x, c=color: {
                    'fillColor': c,
                    'color': c,
                    'weight': 2,
                    'fillOpacity': 0.3,
                    'dashArray': '5, 5'
                },
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=label
            ).add_to(m)
    
    # ===== LAYER 3: FASILITAS WISATA (HIJAU) =====
    if show_facilities:
        for idx, row in facilities_gdf.iterrows():
            popup_html = f"""
            <div style="font-family: Arial; width: 280px;">
                <h4 style="color: #2E7D32; margin: 5px 0;">🟢 {row['name']}</h4>
                <hr style="margin: 5px 0;">
                <b>Tipe Fasilitas:</b> {row['facility_type']}<br>
                <b>Kapasitas Harian:</b> {row['capacity']} orang<br>
                <b>Layanan:</b> {row['service']}<br>
                <b>Koordinat:</b> {row['geometry'].y:.4f}, {row['geometry'].x:.4f}
            </div>
            """
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=10,
                popup=folium.Popup(popup_html, max_width=300),
                color="darkgreen",
                fill=True,
                fillColor="#4CAF50",
                fillOpacity=0.8,
                weight=2,
                tooltip=f"Fasilitas: {row['name']}"
            ).add_to(m)
    
    # ===== LAYER 4: POS PEMANTAUAN (BIRU) =====
    if show_monitoring:
        for idx, row in monitoring_gdf.iterrows():
            popup_html = f"""
            <div style="font-family: Arial; width: 280px;">
                <h4 style="color: #1565C0; margin: 5px 0;">🔵 {row['name']}</h4>
                <hr style="margin: 5px 0;">
                <b>Jadwal Patroli:</b> {row['patrol_schedule']}<br>
                <b>Status:</b> <span style="color: green; font-weight: bold;">{row['status']}</span><br>
                <b>Fungsi:</b> Pemantauan struktural & keamanan situs<br>
                <b>Koordinat:</b> {row['geometry'].y:.4f}, {row['geometry'].x:.4f}
            </div>
            """
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color="darkblue",
                fill=True,
                fillColor="#2196F3",
                fillOpacity=0.8,
                weight=2,
                tooltip=f"Pos: {row['name']}"
            ).add_to(m)
    
    # ===== LAYER 5: CANDI LAIN (FILTER BERDASARKAN PERIODISASI) =====
    if show_other_temples:
        filtered_temples = other_temples_gdf[other_temples_gdf['period'].isin(selected_periods)]
        for idx, row in filtered_temples.iterrows():
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="color: #6D4C41; margin: 5px 0;">🏯 {row['name']}</h4>
                <hr style="margin: 5px 0;">
                <b>Abad:</b> {row['century']}<br>
                <b>Kerajaan:</b> {row['kingdom']}<br>
                <b>Periode:</b> {row['period']}<br>
                <b>Status:</b> {row['status']}<br>
                <b>Risiko:</b> {row['risk_level']}
            </div>
            """
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color="brown",
                fill=True,
                fillColor="#A1887F",
                fillOpacity=0.7,
                weight=2,
                tooltip=f"Candi: {row['name']}"
            ).add_to(m)
    
    # Skala sudah ditambahkan melalui control_scale=True pada Map
    
    # Tambah layer control untuk legend
    folium.LayerControl().add_to(m)
    
    return m

# Buat dan tampilkan peta
m = create_interactive_map(
    sites_gdf, buffer_gdf, facilities_gdf, monitoring_gdf, other_temples_gdf,
    show_site, show_buffer, show_facilities, show_monitoring, show_other_temples,
    periods
)

# Tampilkan peta di Streamlit
st.subheader("📍 Visualisasi Peta Interaktif")
st_folium(m, width=1200, height=600)

# ============================================================================
# LEGENDA & PENJELASAN SIMBOLISASI
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔴 Simbolisasi Warna
    
    - **🔴 MERAH**: Situs Utama (Zona Inti Konservasi Ketat)
    - **🟠 ORANYE/KUNING**: Zona Buffer & Kerentanan Getaran
    - **🟢 HIJAU**: Fasilitas Wisata & Edukasi
    - **🔵 BIRU**: Pos Pemantauan/Penjaga
    - **🟤 COKLAT**: Candi Lain di Sekitar
    """)

with col2:
    st.markdown("""
    ### 📊 Fitur Interaktif
    
    ✓ **Pop-up Info**: Klik setiap marker untuk melihat detail
    ✓ **Layer Control**: Tampilkan/sembunyikan layer via checkbox
    ✓ **Filter Dinamis**: Pilih periode historis untuk filter candi
    ✓ **Zoom & Pan**: Arahkan zoom untuk area detail tertentu
    """)

with col3:
    st.markdown(f"""
    ### 📍 Data Referensi
    
    **Situs Utama**: Candi Borobudur
    - Lat: {borobudur_center['lat']:.4f}
    - Lon: {borobudur_center['lon']:.4f}
    
    **Tahun Analisis**: {datetime.now().year}
    **Sistem Proyeksi**: EPSG:4326 (WGS84)
    """)

# ============================================================================
# RINGKASAN EKSEKUTIF & REKOMENDASI
# ============================================================================

st.markdown("---")
st.subheader("📋 Ringkasan Eksekutif & Temuan Analisis")

executive_summary = """
#### Temuan Ancaman Ekspansi Permukiman di Zona Penyangga Candi Borobudur

**Konteks Masalah:**
Candi Borobudur sebagai Warisan Dunia UNESCO menghadapi tekanan pariwisata massal yang terus meningkat. 
Analisis spasial menunjukkan eskalasi pembangunan permukiman dan infrastruktur komersial di sekitar zona 
penyangga (buffer zone), khususnya dalam radius 2 km dari kompleks candi utama.

**Temuan Utama:**
1. **Risiko Getaran Struktural**: Konstruksi di Buffer 500m & 1km dapat menyebabkan microseismic activity 
   yang mengancam integritas struktur batu candi berusia 1.200+ tahun.

2. **Inkonsistensi Zonasi**: Terdapat permukiman dan fasilitas wisata di zona ketat 500m yang seharusnya 
   bebas konstruksi. Kapasitas pengunjung harian mencapai 3.000+ orang, jauh melebihi daya dukung lingkungan.

3. **Kesenjangan Layanan Edukasi**: Hanya 2 fasilitas pusat informasi untuk menjangkau 2 juta pengunjung/tahun. 
   Kebutuhan akan interpretive center dan guided tour berkualitas masih tinggi.

**Rekomendasi Mitigasi:**
- ✅ Pengendalian ketat pembangunan dalam Buffer 500m (zero-construction zone)
- ✅ Peningkatan kapasitas pusat edukasi dan penjaga situs melalui teknologi monitoring berbasis AI
- ✅ Implementasi sistem zonasi terukur dengan KPI aksesibilitas wisata berkelanjutan
- ✅ Koordinasi lintas sektor: BPK, Dinas Pariwisata, LIPI, dan operator wisata untuk sustainability plan
"""

st.info(executive_summary)

# ============================================================================
# DATA TABLE UNTUK REFERENSI
# ============================================================================

st.markdown("---")
st.subheader("📊 Tabel Data Pendukung Analisis")

tab1, tab2, tab3, tab4 = st.tabs(["Situs Purbakala", "Fasilitas Wisata", "Pos Pemantauan", "Candi Lain"])

with tab1:
    st.dataframe(
        sites_gdf[['name', 'century', 'kingdom', 'status', 'risk_level']],
        use_container_width=True
    )

with tab2:
    st.dataframe(
        facilities_gdf[['name', 'facility_type', 'capacity', 'service']],
        use_container_width=True
    )

with tab3:
    st.dataframe(
        monitoring_gdf[['name', 'patrol_schedule', 'status']],
        use_container_width=True
    )

with tab4:
    st.dataframe(
        other_temples_gdf[['name', 'century', 'kingdom', 'period', 'status', 'risk_level']],
        use_container_width=True
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px; margin-top: 20px;">
    <p>🏛️ Peta Interaktif WebGIS - Zonasi Konservasi Situs Purbakala</p>
    <p>Balai Pelestarian Kebudayaan | Dinas Kebudayaan Provinsi Jawa Tengah</p>
    <p>Data Dummy untuk Tujuan Edukasi | Tahun 2024</p>
</div>
""", unsafe_allow_html=True)
