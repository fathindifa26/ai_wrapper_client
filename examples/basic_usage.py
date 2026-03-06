"""
Basic Usage Examples - AI Wrapper Client

Contoh dasar menggunakan AI Wrapper API dengan struktur modular baru.
"""

from client import AIWrapper, ChatAIWrapper, encode_file

# ============================================================================
# SETUP: Ganti dengan URL VM Anda
# ============================================================================
API_URL = "http://localhost:8000"  # Ganti dengan IP VM Anda


# ============================================================================
# Example 1: Direct Chat (Standard)
# ============================================================================
def example_direct_chat():
    """Contoh dasar mengirim pesan teks."""
    print("=" * 70)
    print("Example 1: Direct Chat")
    print("=" * 70)

    client = AIWrapper(API_URL)

    # Kirim prompt sederhana
    response = client.chat("Apa itu kecerdasan buatan? Jawab singkat.")

    if response.success:
        print(f"✓ Response: {response.text}")
        print(f"  Project ID: {response.project_id}")
    else:
        print(f"✗ Error: {response.error}")


# ============================================================================
# Example 2: Multimedia Chat (Images/Documents)
# ============================================================================
def example_multimedia_chat():
    """Contoh mengirim file (Base64) ke AI."""
    print("\n" + "=" * 70)
    print("Example 2: Multimedia Chat")
    print("=" * 70)

    client = AIWrapper(API_URL)

    # Encode file ke base64
    try:
        # Ganti dengan path file yang ada di komputer Anda
        file_path = "README.md"
        encoded_file = encode_file(file_path)

        response = client.chat("Tolong ringkas isi file ini.", files=[encoded_file])

        if response.success:
            print(f"✓ AI Summary: {response.text}")
        else:
            print(f"✗ Error: {response.error}")
    except FileNotFoundError:
        print("✗ Skip: File tidak ditemukan untuk testing multimedia.")


# ============================================================================
# Example 3: Integrasi LangChain (Modular Adapter)
# ============================================================================
def example_langchain_integration():
    """Menggunakan ChatAIWrapper di ekosistem LangChain."""
    print("\n" + "=" * 70)
    print("Example 3: LangChain Integration")
    print("=" * 70)

    try:
        # ChatAIWrapper bertindak sebagai BaseChatModel
        llm = ChatAIWrapper(base_url=API_URL)

        # Test pemanggilan langsung via LangChain interface
        from langchain_core.messages import HumanMessage

        print("Mengirim pesan via LangChain...")
        res = llm.invoke([HumanMessage(content="Halo LangChain!")])
        print(f"✓ LangChain Response: {res.content}")

    except ImportError:
        print(
            "✗ Skip: LangChain belum terinstall. Jalankan 'pip install langchain-core'."
        )


# ============================================================================
# Example 4: Monitoring API Health
# ============================================================================
def example_monitoring():
    """Mengecek status server dan project yang aktif."""
    print("\n" + "=" * 70)
    print("Example 4: Monitoring API Health")
    print("=" * 70)

    client = AIWrapper(API_URL)

    try:
        status = client.get_status()
        print(f"API API_STATUS: {status['api_status']}")
        print(f"Active Contexts: {status['context_pool']['total_contexts']}")

        projects = client.list_projects()
        print(f"Registered Projects: {projects['active_projects']}")
    except Exception as e:
        print(f"✗ Error monitoring: {e}")


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI WRAPPER CLIENT - USAGE EXAMPLES")
    print("=" * 70)

    # Jalankan contoh
    example_direct_chat()
    example_multimedia_chat()
    example_langchain_integration()
    example_monitoring()

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
