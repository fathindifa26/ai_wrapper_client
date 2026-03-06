# AI Wrapper Client

Python client library untuk mengakses AI Wrapper API secara efisien. Library ini dirancang untuk memudahkan integrasi automation chat ke berbagai project tanpa harus mengelola dependensi browser secara langsung.

## 🚀 Instalasi

Install langsung menggunakan `pip` di environment Anda:

```bash
pip install -e .
```

Jika ingin menggunakan fitur LangChain:
```bash
pip install ".[langchain]"
```

## 📖 Cara Penggunaan

### 1. Inisialisasi Client (Direct)
```python
from client import AIWrapper

# Gunakan alamat IP VM atau server API Anda
client = AIWrapper(base_url="http://[IP_VM_ANDA]:8000")
```

### 2. Kirim Chat (Standard)
```python
response = client.chat("Halo, siapa namamu?")

if response.success:
    print(f"AI: {response.text}")
else:
    print(f"Error: {response.error}")
```

### 3. Integrasi LangChain (Advanced)
Gunakan `ChatAIWrapper` untuk integrasi dengan LangChain Agents atau Chains.
```python
from client import ChatAIWrapper

llm = ChatAIWrapper(base_url="http://localhost:8000")
# Model ini bisa langsung dimasukkan ke AgentExecutor atau Chain
```

## 🛠️ Fitur Utama
- **Modular Architecture**: Kode terbagi rapi ke `models`, `core`, dan `adapters`.
- **Gemini-Style Response**: Mendukung field `candidates` untuk kemudahan parsing tool calls.
- **Multimedia Support**: Bisa kirim image/dokumen via base64.
- **LangChain Native**: Terintegrasi penuh sebagai objek `BaseChatModel`.

## 📝 Troubleshooting
- Pastikan port `8000` di server tujuan sudah dibuka.
- Jika Agent looping, pastikan `handle_parsing_errors=True` di AgentExecutor.
- Gunakan `client.get_status()` untuk mengecek kesehatan engine di server.

## 🔗 Links
- **Contoh Penggunaan Lengkap**: [examples/basic_usage.py](examples/basic_usage.py)
- **Bahasa Lain (Node.js, Java, dll)**: [examples/other_languages.md](examples/other_languages.md)
