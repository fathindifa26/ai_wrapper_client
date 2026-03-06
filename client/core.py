import requests
from typing import Optional, List, Dict, Any
from .models import ChatResponse


class AIWrapper:
    """
    The main client for interacting with the AI Wrapper API.

    Handles HTTP communication, timeouts, and standardized response parsing.

    Example:
        >>> from client import AIWrapper
        >>> client = AIWrapper(base_url="http://localhost:8000")
        >>> response = client.chat("Hello!")
        >>> print(response.text)
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 300):
        """
        Initialize the AI Wrapper client.

        Args:
            base_url (str): The URL where the AI Wrapper API is running.
            timeout (int): Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def chat(
        self,
        prompt: str,
        project_url: Optional[str] = None,
        files: Optional[List[str]] = None,
        stop: Optional[List[str]] = None,
    ) -> ChatResponse:
        """
        Send a chat message to the AI, optionally with multimedia files and stop sequences.

        Args:
            prompt (str): The text message to send.
            project_url (Optional[str]): Explicit project URL if not using the server's default.
            files (Optional[List[str]]): List of base64-encoded strings representing files.
            stop (Optional[List[str]]): List of strings that should stop the generation (truncated on client side).

        Returns:
            ChatResponse: Standardized response object containing text or error details.
        """
        payload = {"prompt": prompt, "project_url": project_url, "files": files}

        try:
            response = requests.post(
                f"{self.base_url}/chat", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            res_text = data.get("response")
            candidates = data.get("candidates")

            # Client-side truncation for stop sequences
            if stop and res_text:
                for s in stop:
                    if s in res_text:
                        res_text = res_text.split(s)[0]

                # Also truncate candidates accordingly
                if candidates:
                    for cand in candidates:
                        parts = cand.get("content", {}).get("parts", [])
                        for part in parts:
                            if "text" in part:
                                for s in stop:
                                    if s in part["text"]:
                                        part["text"] = part["text"].split(s)[0]

            return ChatResponse(
                status=data.get("status", "error"),
                project_id=data.get("project_id"),
                response=res_text,
                candidates=candidates,
                error=data.get("error"),
                files_uploaded=data.get("files_uploaded"),
            )
        except Exception as e:
            return ChatResponse(status="error", error=str(e))

    def get_status(self) -> Dict[str, Any]:
        """Fetch server status and browser engine health."""
        response = requests.get(f"{self.base_url}/status", timeout=5)
        response.raise_for_status()
        return response.json()

    def list_projects(self) -> Dict[str, Any]:
        """List currently active AI project contexts in the server."""
        response = requests.get(f"{self.base_url}/projects", timeout=5)
        response.raise_for_status()
        return response.json()

    def reload_engine(self) -> Dict[str, str]:
        """Trigger a reload of the browser engine if needed."""
        response = requests.post(f"{self.base_url}/reload", timeout=30)
        response.raise_for_status()
        return response.json()


def quick_chat(prompt: str, base_url: str = "http://localhost:8000", **kwargs) -> str:
    """
    A convenience function for sending a single prompt and getting text back immediately.

    Args:
        prompt (str): The text message.
        base_url (str): The API base URL.
        **kwargs: Additional arguments passed to AIWrapper.chat (e.g., files, project_url).

    Returns:
        str: The AI's response text.
    """
    client = AIWrapper(base_url)
    return client.chat(prompt, **kwargs).text
