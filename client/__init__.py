"""
AI Wrapper Client - Modular Package

This package provides a clean interface to the AI Wrapper API.
It supports both direct client usage and LangChain integration.
"""

from .models import ChatResponse
from .core import AIWrapper, quick_chat
from .adapters import ChatAIWrapper, encode_file

__all__ = [
    "AIWrapper",
    "ChatAIWrapper",
    "ChatResponse",
    "quick_chat",
    "encode_file",
]
