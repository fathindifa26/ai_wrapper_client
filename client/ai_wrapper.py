"""
AI Wrapper Client Library

Simple Python client untuk akses AI Wrapper API.
Mudah digunakan untuk development dan production.

USAGE:
    from client.ai_wrapper import AIWrapper

    # Initialize client
    client = AIWrapper(base_url="http://your-vm:8000")

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
import json
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass
from pathlib import Path

# Optional LangChain imports
try:
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.outputs import ChatResult, ChatGeneration

    _HAS_LANGCHAIN = True
except ImportError:
    _HAS_LANGCHAIN = False

    # Mock classes for type hinting if langchain not installed
    class BaseChatModel:
        pass

    class BaseMessage:
        pass

    class ChatResult:
        pass


@dataclass
class ChatResponse:
    """Response from AI chat following Gemini-style standardization."""

    status: str
    project_id: Optional[str] = None
    response: Optional[str] = None  # Original text response
    candidates: Optional[List[Dict[str, Any]]] = None  # Standardized Gemini candidates
    error: Optional[str] = None
    files_uploaded: Optional[int] = None

    @property
    def success(self) -> bool:
        return self.status == "success"

    @property
    def text(self) -> str:
        """Get the main text response from candidates or response field."""
        if self.candidates and len(self.candidates) > 0:
            parts = self.candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                if "text" in part:
                    return part["text"]
        return self.response or ""

    def __str__(self) -> str:
        if self.success:
            return f"[{self.project_id}] {self.text}"
        return f"[ERROR] {self.error}"


class AIWrapper:
    """
    Base client for AI Wrapper API.

    Example:
        >>> client = AIWrapper("http://localhost:8000")
        >>> res = client.chat("Hello!")
        >>> print(res.text)
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 300):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def chat(
        self,
        prompt: str,
        project_url: Optional[str] = None,
        files: Optional[List[str]] = None,
    ) -> ChatResponse:
        """Send chat request. Supports multimedia and tool calls via standardized output."""
        payload = {"prompt": prompt, "project_url": project_url, "files": files}

        try:
            response = requests.post(
                f"{self.base_url}/chat", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            return ChatResponse(
                status=data.get("status", "error"),
                project_id=data.get("project_id"),
                response=data.get("response"),
                candidates=data.get("candidates"),
                error=data.get("error"),
                files_uploaded=data.get("files_uploaded"),
            )
        except Exception as e:
            return ChatResponse(status="error", error=str(e))

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


# Helper functions to encode files
def encode_file(file_path: Union[str, Path]) -> str:
    """Base64 encode file for multimedia input."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# Convenience function for quick usage
def quick_chat(prompt: str, base_url: str = "http://localhost:8000", **kwargs) -> str:
    """Quick one-liner chat."""
    client = AIWrapper(base_url)
    return client.chat(prompt, **kwargs).text


# --- LangChain Integration ---
if _HAS_LANGCHAIN:

    class ChatAIWrapper(BaseChatModel):
        """Custom LangChain ChatModel that connects to AI Wrapper API."""

        base_url: str = "http://localhost:8000"
        project_url: Optional[str] = None
        timeout: int = 600
        client: Optional[AIWrapper] = None

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if not self.client:
                self.client = AIWrapper(base_url=self.base_url, timeout=self.timeout)

        def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[Any] = None,
            **kwargs: Any,
        ) -> ChatResult:
            # 1. Convert LangChain messages to a single prompt
            prompt = ""
            for m in messages:
                prefix = "User: " if isinstance(m, HumanMessage) else "Assistant: "
                prompt += f"{prefix}{m.content}\n"

            # 2. Call AI Wrapper API via unified client
            res = self.client.chat(prompt.strip(), project_url=self.project_url)

            # 3. Handle response
            message = AIMessage(content=res.text)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        @property
        def _llm_type(self) -> str:
            return "chat-ai-wrapper"
