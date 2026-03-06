from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ChatResponse:
    """
    Standardized response from the AI Wrapper API.

    Attributes:
        status (str): "success" or "error".
        project_id (Optional[str]): The unique ID of the AI project context.
        response (Optional[str]): Original raw text response from the API.
        candidates (Optional[List[Dict[str, Any]]]): Gemini-style standardized output chunks.
        error (Optional[str]): Error message if status is "error".
        files_uploaded (Optional[int]): Number of files successfully processed in the request.
    """

    status: str
    project_id: Optional[str] = None
    response: Optional[str] = None
    candidates: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    files_uploaded: Optional[int] = None

    @property
    def success(self) -> bool:
        """Check if the request was successful."""
        return self.status == "success"

    @property
    def text(self) -> str:
        """
        Extract the main text content from the response candidates.
        Falls back to the raw 'response' field if candidates are missing.
        """
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
