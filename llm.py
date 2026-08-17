"""
Wraps the Gemini chat model behind a single function, so the rest of
the app doesn't need to know which provider we're using.
"""
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

_llm = None


def get_llm() -> ChatGoogleGenerativeAI:
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=settings.CHAT_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2,
        )
    return _llm


def invoke_llm(prompt: str) -> str:
    """
    Calls the LLM and always returns a plain string, regardless of
    whether the underlying SDK returns response.content as a string
    or as a list of content parts (which some Gemini SDK versions do).
    """
    response = get_llm().invoke(prompt)
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get("text", ""))
        return "".join(parts).strip()

    return str(content)
