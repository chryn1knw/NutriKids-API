## Instalasi

```
# Clone repo
git clone https://github.com/namamu/NutriKids-API.git
cd NutriKids-API

# Buat virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Menjalankan API
```
python src/app.py
```

## Testing Coverage

Kami menggunakan `pytest` untuk memastikan kualitas dan stabilitas aplikasi melalui berbagai jenis pengujian berikut:

- **API Testing**  
  Memastikan setiap endpoint menerima input dan memberikan respons sesuai dengan kontrak yang telah ditentukan.

- **Integration Testing**  
  Menguji alur kerja antar komponen utama, termasuk validasi input, pemrosesan model machine learning, dan sistem rekomendasi makanan.

- **Performance Testing**  
  Mengukur waktu respons dan memastikan performa tetap optimal pada berbagai skenario penggunaan.

- **Concurrency Testing**  
  Menilai kestabilan sistem saat menerima banyak permintaan secara bersamaan (simulasi trafik tinggi).

# Jalankan semua tes
```
pytest tests/test.py -v
```
