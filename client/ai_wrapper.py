"""
AI Wrapper Client Library

Simple Python client untuk akses AI Wrapper API.
Mudah digunakan untuk development dan production.

USAGE:
    from client_library import AIClient

    # Initialize client
    client = AIClient(base_url="http://your-vm:8000")

    # Single project mode (uses default AI_URL from server)
    response = client.chat("What is AI?")

    # Multi-project mode (specify project URL)
    response = client.chat(
        "Hello",
        project_url="https://imagine.wpp.ai/chat/PROJECT_ID/foundational"
    )
"""

import requests
import base64
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChatResponse:
    """Response from AI chat."""
    status: str
    project_id: Optional[str] = None
    response: Optional[str] = None
    error: Optional[str] = None
    images_uploaded: Optional[int] = None  # Count of images uploaded

    @property
    def success(self) -> bool:
        """Check if request was successful."""
        return self.status == "success"

    def __str__(self) -> str:
        """String representation."""
        if self.success:
            files_str = f" [{self.images_uploaded} image(s) uploaded]" if self.images_uploaded else ""
            return f"[{self.project_id}]{files_str} {self.response}"
        else:
            return f"[ERROR] {self.error}"


class AIClient:
    """
    Client untuk AI Wrapper API.

    Example:
        >>> client = AIClient("http://vm-server:8000")
        >>> response = client.chat("What is Python?")
        >>> print(response.response)
    """

    def __init__(self, base_url: str, timeout: int = 180):
        """
        Initialize AI client.

        Args:
            base_url: Base URL of AI Wrapper API (e.g., "http://vm:8000")
            timeout: Request timeout in seconds (default: 180)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verify connection to API server."""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            if response.status_code != 200:
                print(f"Warning: API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not connect to API: {e}")

    def chat(
        self,
        prompt: str,
        project_url: Optional[str] = None,
        images: Optional[List[str]] = None
    ) -> ChatResponse:
        """
        Send chat request to AI with optional base64-encoded images.

        Args:
            prompt: The prompt/question to send
            project_url: Optional project URL. If not provided, uses default from server.
            images: Optional list of base64-encoded image strings

        Returns:
            ChatResponse object with status and response

        Raises:
            requests.exceptions.RequestException: If request fails

        Example (text-only):
            >>> response = client.chat("Explain quantum computing")
            >>> if response.success:
            ...     print(response.response)

        Example (with image):
            >>> import base64
            >>> with open("image.png", "rb") as f:
            ...     img_b64 = base64.b64encode(f.read()).decode()
            >>> response = client.chat("What's in this image?", images=[img_b64])
            >>> print(response.response)
        """
        payload = {
            "prompt": prompt,
            "project_url": project_url,
            "images": images  # Can be None
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            return ChatResponse(
                status=data.get("status", "error"),
                project_id=data.get("project_id"),
                response=data.get("response"),
                error=data.get("error"),
                images_uploaded=data.get("images_uploaded")
            )

        except requests.exceptions.Timeout:
            return ChatResponse(
                status="error",
                error="Request timeout - AI taking too long to respond"
            )
        except requests.exceptions.RequestException as e:
            return ChatResponse(
                status="error",
                error=f"Request failed: {str(e)}"
            )

    def get_status(self) -> Dict[str, Any]:
        """
        Get API status and active projects.

        Returns:
            Dict with API status information

        Example:
            >>> status = client.get_status()
            >>> print(f"Active projects: {status['context_pool']['total_contexts']}")
        """
        response = requests.get(f"{self.base_url}/status", timeout=5)
        response.raise_for_status()
        return response.json()

    def list_projects(self) -> Dict[str, Any]:
        """
        List all active project contexts.

        Returns:
            Dict with project information

        Example:
            >>> projects = client.list_projects()
            >>> print(projects['active_projects'])
        """
        response = requests.get(f"{self.base_url}/projects", timeout=5)
        response.raise_for_status()
        return response.json()

    def reload_engine(self) -> Dict[str, str]:
        """
        Reload browser engine (useful if it crashes).

        Returns:
            Dict with reload status

        Example:
            >>> result = client.reload_engine()
            >>> print(result['status'])
        """
        response = requests.post(f"{self.base_url}/reload", timeout=30)
        response.raise_for_status()
        return response.json()


# Helper function to encode images
def encode_image(image_path: str) -> str:
    """
    Helper to read and base64-encode an image file.

    Args:
        image_path: Path to image file (relative or absolute)

    Returns:
        Base64-encoded string

    Raises:
        FileNotFoundError: If image file doesn't exist

    Example:
        >>> img_b64 = encode_image("photo.jpg")
        >>> response = client.chat("Describe this", images=[img_b64])
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# Convenience function for quick usage
def quick_chat(
    prompt: str,
    base_url: str = "http://localhost:8000",
    project_url: Optional[str] = None,
    images: Optional[List[str]] = None
) -> str:
    """
    Quick one-liner chat function with optional base64 images.

    Args:
        prompt: The question/prompt
        base_url: API base URL
        project_url: Optional project URL
        images: Optional list of base64-encoded image strings

    Returns:
        AI response text or error message

    Example (text-only):
        >>> answer = quick_chat("What is AI?", base_url="http://vm:8000")
        >>> print(answer)

    Example (with image):
        >>> img_b64 = encode_image("photo.jpg")
        >>> answer = quick_chat("Describe this", images=[img_b64])
        >>> print(answer)
    """
    client = AIClient(base_url)
    response = client.chat(prompt, project_url, images=images)
    return response.response if response.success else f"Error: {response.error}"


if __name__ == "__main__":
    # Demo usage
    print("AI Wrapper Client Library - Demo\n")

    # Initialize client (change to your VM URL)
    client = AIClient("http://localhost:8000")

    # Check status
    print("1. Checking API status...")
    status = client.get_status()
    print(f"   API Status: {status['api_status']}")
    print(f"   Active Projects: {status['context_pool']['total_contexts']}")

    # Example chat
    print("\n2. Sending chat request...")
    response = client.chat("What is Python? Jawab singkat.")

    if response.success:
        print(f"   Success! Project: {response.project_id}")
        print(f"   Response: {response.response}")
    else:
        print(f"   Failed: {response.error}")

    # Quick chat example
    print("\n3. Using quick_chat function...")
    answer = quick_chat("Hello! Jawab singkat.", "http://localhost:8000")
    print(f"   Answer: {answer}")
