# 🏛️ WebGIS Zonasi Konservasi Situs Purbakala Candi Borobudur

Peta interaktif berbasis web untuk visualisasi dan monitoring zonasi konservasi, aksesibilitas wisata, serta analisis risiko getaran struktural pada Candi Borobudur, situs warisan dunia UNESCO.

## 🎯 Tujuan

Publikasi hasil analisis spasial pelestarian situs purbakala dari QGIS menjadi WebGIS interaktif yang dapat diakses oleh:
- Balai Pelestarian Kebudayaan (BPK)
- Dinas Kebudayaan & Pariwisata
- Pemangku kebijakan pariwisata
- Masyarakat luas (edukasi publik)

Tanpa memerlukan instalasi aplikasi QGIS atau software GIS lainnya.

## 🌐 Live Demo

**Akses peta interaktif**: https://webgis-borobudur.streamlit.app

*(Ganti URL dengan hasil deployment Anda)*

## 🗺️ Fitur Utama

### Simbolisasi & Styling Kartografi
- 🔴 **Merah** - Situs Candi Utama (Zona Konservasi Ketat)
- 🟠 **Oranye/Kuning** - Zona Buffer & Kerentanan Getaran (500m, 1km, 2km)
- 🟢 **Hijau** - Fasilitas Wisata & Pusat Edukasi
- 🔵 **Biru** - Pos Pemantauan & Penjaga Situs
- 🟤 **Coklat** - Candi Lain di Sekitar (Mendut, Pawon, Ngawen)

### Interaktivitas
- **Pop-up Info**: Klik setiap marker untuk melihat atribut detail
  - Situs: Nama, Abad, Kerajaan, Status Konservasi, Tingkat Risiko
  - Fasilitas: Nama, Tipe, Kapasitas, Layanan
  - Monitoring: Jadwal Patroli, Status, Fungsi
- **Layer Control**: Tampilkan/sembunyikan layer via checkbox
- **Filter Dinamis**: Pilih periode historis (Hindu, Buddha, Hindu-Buddha)
- **Zoom & Pan**: Arahkan zoom untuk area detail tertentu
- **Scale Control**: Tampil skala peta

### Analisis & Dokumentasi
- Legenda komprehensif dengan interpretasi warna
- Ringkasan Eksekutif: Temuan ancaman ekspansi permukiman
- Tabel data pendukung (4 tabs):
  - Situs Purbakala
  - Fasilitas Wisata
  - Pos Pemantauan
  - Candi Lain
- Rekomendasi mitigasi risiko

## 🛠️ Teknologi

| Komponen | Tool | Versi |
|----------|------|-------|
| Web Framework | Streamlit | 1.28.1 |
| Mapping Library | Folium | 0.14.0 |
| Geospatial | GeoPandas | 0.13.2 |
| Geometri | Shapely | 2.0.1 |
| Data Processing | Pandas, NumPy | 2.0.3, 1.24.3 |
| Hosting | Streamlit Cloud | Free tier |

## 📦 Instalasi & Setup Lokal

### Prasyarat
- Python 3.8+
- pip atau conda

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/[USERNAME]/webgis-borobudur.git
cd webgis-borobudur
```

2. **Buat virtual environment** (opsional tapi recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Jalankan aplikasi**
```bash
streamlit run borobudur_webgis.py
```

5. **Buka di browser**
- Otomatis membuka `http://localhost:8501`
- Atau manual buka: http://localhost:8501

## 🚀 Deployment ke Streamlit Cloud

### Persiapan GitHub

1. Push kode ke GitHub repository publik:
```bash
git add .
git commit -m "Add WebGIS Borobudur app"
git push origin main
```

2. Pastikan file ini ada di repo:
   - `borobudur_webgis.py` (file utama)
   - `requirements.txt` (dependencies)
   - `.gitignore` (optional)

### Deploy via Streamlit Cloud

1. Buka https://streamlit.io/cloud
2. Login dengan akun GitHub
3. Klik "Create app"
4. Pilih:
   - Repository: `webgis-borobudur`
   - Branch: `main`
   - Main file: `borobudur_webgis.py`
5. Klik "Deploy!" dan tunggu 2-3 menit

**Live URL akan tampil seperti**: `https://webgis-borobudur.streamlit.app`

*Lihat `PANDUAN_DEPLOYMENT.md` untuk detail lengkap.*

## 📊 Struktur Data

### 5 Layer Geospatial

1. **Situs Purbakala** (Point)
   - 1 data: Candi Borobudur
   - Attributes: name, century, kingdom, status, risk_level

2. **Zona Buffer** (Polygon)
   - 3 data: Buffer 500m, 1km, 2km
   - Attributes: zone_type, capacity, description

3. **Fasilitas Wisata** (Point)
   - 5 data: Museum, Pusat Info, RS, Hotel, Parkir
   - Attributes: name, facility_type, capacity, service

4. **Pos Pemantauan** (Point)
   - 4 data: Pos di berbagai lokasi
   - Attributes: name, patrol_schedule, status

5. **Candi Lain** (Point)
   - 3 data: Mendut, Pawon, Ngawen
   - Attributes: name, century, kingdom, period, status, risk_level

**Catatan**: Data saat ini adalah dummy untuk demo. Untuk data real, gunakan shapefile hasil export QGIS.

## 📈 Pengembangan Lebih Lanjut

- [ ] Integrasi data real dari shapefile QGIS
- [ ] Heatmap pengunjung per zona
- [ ] Time-series monitoring struktural 10 tahun
- [ ] API sensor real-time untuk vibrasi getaran
- [ ] Optimasi mobile UI
- [ ] Export data as GeoJSON/CSV
- [ ] User authentication untuk akses internal BPK
- [ ] Multilingual support (EN, ID)
- [ ] Basemap variants (Satelit, Terrain)
- [ ] PostgreSQL + PostGIS backend

## 📚 Referensi & Dokumentasi

- [Streamlit Docs](https://docs.streamlit.io)
- [Folium Mapping](https://python-visualization.github.io/folium/)
- [GeoPandas Guide](https://geopandas.org/)
- [UNESCO Borobudur Heritage](https://whc.unesco.org/en/list/592/)

## 📋 Informasi Tugas

**Matakuliah**: Sistem Informasi Geografis (SIG)
**Topik**: WebGIS Publication & Interaktif Mapping
**Periode**: Semester 2024
**Deliverables**:
- ✅ Live URL peta interaktif
- ✅ 2 buah screenshot (full view + pop-up)
- ✅ Laporan alur SDLC sistem

## 👨‍💻 Author

[Nama Anda] | [Nim] | [Universitas]

## 📞 Support & Issues

Jika ada pertanyaan atau bug:
1. Buka GitHub Issues
2. Atau hubungi pengembang

## 📄 License

MIT License - Bebas digunakan untuk keperluan edukasi dan komersial

---

**Happy Mapping! 🗺️🎉**

Made with ❤️ using Streamlit + Folium
