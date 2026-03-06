import base64
from typing import Optional, List, Any, Union
from pathlib import Path
from .core import AIWrapper

# Standard LangChain imports - handled gracefully if not installed
try:
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.outputs import ChatResult, ChatGeneration

    _HAS_LANGCHAIN = True
except ImportError:
    _HAS_LANGCHAIN = False

    # Fallback to avoid NameErrors
    class BaseChatModel:
        pass

    class BaseMessage:
        pass

    class ChatResult:
        pass


def encode_file(file_path: Union[str, Path]) -> str:
    """
    Helper to Base64 encode any file for sending to the AI Wrapper.

    Args:
        file_path: Path structure or string to the file to encode.

    Returns:
        str: Base64 formatted string.
    """
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


if _HAS_LANGCHAIN:

    class ChatAIWrapper(BaseChatModel):
        """
        LangChain-compatible ChatModel adapter.

        This allows the AI Wrapper to be used as a drop-in replacement
        for models like ChatOpenAI in LangChain agents and chains.
        """

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
            """
            Internal LangChain generator. Converts messages to prompt
            and executes via the unified AIWrapper client.
            """
            prompt = ""
            for m in messages:
                prefix = "User: " if isinstance(m, HumanMessage) else "Assistant: "
                prompt += f"{prefix}{m.content}\n"

            # Execute via unified client
            res = self.client.chat(
                prompt.strip(), project_url=self.project_url, stop=stop
            )

            # Return as LangChain structure
            message = AIMessage(content=res.text)
            return ChatResult(generations=[ChatGeneration(message=message)])

        @property
        def _llm_type(self) -> str:
            """Return identifier for this model type."""
            return "chat-ai-wrapper"

else:
    # If LangChain is missing, provide a friendly warning if the class is attempted
    class ChatAIWrapper:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is not installed. Please install 'langchain-core' to use ChatAIWrapper."
            )
