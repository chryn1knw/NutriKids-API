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

# Jalankan semua tes
```
pytest tests/test.py -v
```

## Testing Coverage
Kami menggunakan pytest untuk melakukan:

-API Testing: Memastikan setiap endpoint menerima input dan merespons sesuai kontrak.
-Integration Testing: Menguji integrasi antar komponen utama (input validation, model ML, dan filter makanan).
-Performance Testing: Menjamin response time tetap optimal.
-Concurrency Testing: Menilai kestabilan saat terjadi banyak permintaan bersamaan.