"""
Basic Usage Examples - AI Wrapper Client

Contoh dasar menggunakan AI Wrapper API dari aplikasi Anda.
"""

from client.ai_wrapper import AIClient

# ============================================================================
# SETUP: Ganti dengan URL VM Anda
# ============================================================================
API_URL = "http://your-vm-ip:8000"  # Ganti dengan IP VM Anda


# ============================================================================
# Example 1: Single Project Mode (menggunakan default AI_URL dari server)
# ============================================================================
def example_single_project():
    """Menggunakan default project yang di-set di server."""
    print("=" * 70)
    print("Example 1: Single Project Mode")
    print("=" * 70)

    client = AIClient(API_URL)

    # Tidak perlu kirim project_url, pakai default dari server
    response = client.chat("What is artificial intelligence? Be brief.")

    if response.success:
        print(f"✓ Response: {response.response}")
    else:
        print(f"✗ Error: {response.error}")


# ============================================================================
# Example 2: Multi-Project Mode (specify different projects)
# ============================================================================
def example_multi_project():
    """Menggunakan multiple projects secara dynamic."""
    print("\n" + "=" * 70)
    print("Example 2: Multi-Project Mode")
    print("=" * 70)

    client = AIClient(API_URL)

    # Project A
    project_a = "[PROJECT_URL_A]"
    response_a = client.chat("What is Python?", project_url=project_a)
    print(f"Project A: {response_a.response[:100]}...")

    # Project B
    project_b = "[PROJECT_URL_B]"
    response_b = client.chat("What is JavaScript?", project_url=project_b)
    print(f"Project B: {response_b.response[:100]}...")


# ============================================================================
# Example 3: Error Handling
# ============================================================================
def example_error_handling():
    """Best practice error handling."""
    print("\n" + "=" * 70)
    print("Example 3: Error Handling")
    print("=" * 70)

    client = AIClient(API_URL)

    try:
        response = client.chat("Explain machine learning")

        if response.success:
            print(f"✓ Success: {response.response}")
        else:
            # Handle different error types
            if "NOT_LOGGED_IN" in response.error:
                print("✗ Session expired - need to re-login on server")
            elif "SEND_FAILED" in response.error:
                print("✗ Failed to send prompt - UI issue")
            elif "timeout" in response.error.lower():
                print("✗ Request timeout - AI taking too long")
            else:
                print(f"✗ Error: {response.error}")

    except Exception as e:
        print(f"✗ Unexpected error: {e}")


# ============================================================================
# Example 4: Batch Processing
# ============================================================================
def example_batch_processing():
    """Process multiple questions."""
    print("\n" + "=" * 70)
    print("Example 4: Batch Processing")
    print("=" * 70)

    client = AIClient(API_URL)

    questions = ["What is AI?", "What is ML?", "What is DL?"]

    results = []
    for i, question in enumerate(questions, 1):
        print(f"Processing {i}/{len(questions)}: {question}")
        response = client.chat(question)

        if response.success:
            results.append({"question": question, "answer": response.response})
        else:
            print(f"  ✗ Failed: {response.error}")

    print(f"\n✓ Successfully processed {len(results)}/{len(questions)} questions")


# ============================================================================
# Example 5: Monitoring API Health
# ============================================================================
def example_monitoring():
    """Monitor API status and active projects."""
    print("\n" + "=" * 70)
    print("Example 5: Monitoring API Health")
    print("=" * 70)

    client = AIClient(API_URL)

    # Check API status
    status = client.get_status()
    print(f"API Status: {status['api_status']}")
    print(f"Browser Engine: {status['browser_engine']}")
    print(f"Total Contexts: {status['context_pool']['total_contexts']}")

    # List active projects
    projects = client.list_projects()
    print(f"\nActive Projects ({projects['total_projects']}):")
    for project_id in projects["active_projects"]:
        print(f"  - {project_id}")


# ============================================================================
# Example 6: Using in Your Application
# ============================================================================
def example_application_integration():
    """Example of integrating into your application."""
    print("\n" + "=" * 70)
    print("Example 6: Application Integration")
    print("=" * 70)

    # Initialize client once at app startup
    ai_client = AIClient(API_URL)

    # Use in your application logic
    def process_user_question(user_input: str) -> str:
        """Process user question through AI."""
        response = ai_client.chat(user_input)

        if response.success:
            return response.response
        else:
            # Log error and return fallback
            print(f"AI Error: {response.error}")
            return "Sorry, I couldn't process your question right now."

    # Example usage
    user_question = "What is quantum computing?"
    answer = process_user_question(user_question)
    print(f"Q: {user_question}")
    print(f"A: {answer}")


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI WRAPPER CLIENT - USAGE EXAMPLES")
    print("=" * 70)
    print(f"API URL: {API_URL}")
    print("\nNote: Update API_URL variable to your VM IP address!")
    print("=" * 70)

    # Run examples
    try:
        example_single_project()
        # example_multi_project()
        # example_error_handling()
        # example_batch_processing()
        # example_monitoring()
        # example_application_integration()

    except Exception as e:
        print(f"\n✗ Failed to run examples: {e}")
        print("  Make sure:")
        print("  1. API server is running: python run.py")
        print("  2. API_URL is correct")
        print("  3. Server is accessible from this machine")
