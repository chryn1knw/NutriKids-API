## Instalasi

```
# Clone repository
git clone https://github.com/chryn1knw/NutriKids-API.git
cd NutriKids-API

# Buat virtual environment
python -m venv .venv

# Aktifkan environment
source .venv/bin/activate      # Untuk Linux/macOS
.venv\Scripts\activate         # Untuk Windows

# Install dependencies
pip install -r requirements.txt
```
## Menjalankan API
```bash
python src/app.py
```

## Testing Coverage

`pytest` untuk memastikan kualitas dan stabilitas aplikasi melalui berbagai jenis pengujian berikut:

- **API Testing**  
  Memastikan setiap endpoint menerima input dan memberikan respons sesuai dengan kontrak yang telah ditentukan.

- **Integration Testing**  
  Menguji alur kerja antar komponen utama, termasuk validasi input, pemrosesan model machine learning, dan sistem rekomendasi makanan.

# Jalankan semua tes
```bash
pytest tests/ -v
```
