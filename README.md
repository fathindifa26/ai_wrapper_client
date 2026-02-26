# AI Wrapper Client

Python client library untuk mengakses AI Wrapper API secara efisien. Library ini dirancang untuk memudahkan integrasi automation chat ke berbagai project tanpa harus mengelola dependensi browser secara langsung.

## 🚀 Instalasi

Install langsung menggunakan `pip` dari repository ini:

```bash
pip install git+https://github.com/fathindifa26/ai_wrapper_client.git
```

## 📖 Cara Penggunaan

### 1. Inisialisasi Client
```python
from client.ai_wrapper import AIClient

# Gunakan alamat IP VM atau server API Anda
client = AIClient(base_url="http://[IP_VM_ANDA]:8000")
```

### 2. Kirim Chat (Single Project)
Mode default menggunakan konfigurasi project utama yang ada di server.
```python
response = client.chat("Halo, jelaskan apa itu AI secara singkat.")

if response.success:
    print(f"AI: {response.response}")
else:
    print(f"Error: {response.error}")
```

### 3. Kirim Chat (Multi-Project)
Anda bisa menentukan project URL yang berbeda untuk setiap request.
```python
project_url = "https://imagine.wpp.ai/chat/PROJ_ID/foundational"
response = client.chat("Apa kabar?", project_url=project_url)
```

## 🛠️ Fitur Utama
- **Lightweight**: Hanya membutuhkan library `requests`.
- **Easy Deployment**: Tidak perlu install Playwright/Chrome di sisi client.
- **Support Parallelism**: Mendukung akses ke banyak project sekaligus.

## 📝 Troubleshooting
- Pastikan port `8000` di server tujuan sudah dibuka.
- Jika muncul error `NOT_LOGGED_IN`, berarti session di server perlu di-refresh oleh admin.
