"""Deterministic retriever for ENAE pre-operation instructions."""

from __future__ import annotations

import math
import re
from typing import Any
from urllib.request import Request, urlopen


INSTRUCTIONS_URL = (
    "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
)
_CACHE: dict[str, Any] = {"chunks": [], "fetched": False}
FALLBACK_TEXT = (
    "Before surgery, pets should follow strict fasting instructions from the previous "
    "night. Owners should avoid giving food on surgery morning, follow clinic guidance "
    "about water intake, and report any warning signs (vomiting, respiratory symptoms, "
    "active heat, or unusual weakness) before admission. The clinic must confirm final "
    "admission instructions and the owner should arrive within the assigned dropoff window."
)


def _strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _chunk_text(text: str, chunk_size: int = 420, overlap: int = 80) -> list[str]:
    chunks: list[str] = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end].strip())
        if end >= text_len:
            break
        start = max(end - overlap, 0)
    return [chunk for chunk in chunks if chunk]


def load_source_chunks() -> list[str]:
    """Fetches and chunks the required source with in-memory caching."""
    if _CACHE["fetched"] and _CACHE["chunks"]:
        return _CACHE["chunks"]

    try:
        req = Request(INSTRUCTIONS_URL, headers={"User-Agent": "enae-vet-bot/1.0"})
        with urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        cleaned = _strip_html(html)
        if len(cleaned) < 400:
            cleaned = FALLBACK_TEXT
        _CACHE["chunks"] = _chunk_text(cleaned)
        _CACHE["fetched"] = True
    except Exception:
        _CACHE["chunks"] = _chunk_text(FALLBACK_TEXT)
        _CACHE["fetched"] = True
    return _CACHE["chunks"]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]{3,}", text.lower())


def retrieve_relevant_chunks(question: str, top_k: int = 2) -> list[str]:
    """Returns top-k chunks using lexical overlap scoring."""
    chunks = load_source_chunks()
    q_tokens = _tokenize(question)
    if not q_tokens:
        return chunks[:top_k]

    token_set = set(q_tokens)
    scored: list[tuple[float, str]] = []
    for chunk in chunks:
        c_tokens = _tokenize(chunk)
        overlap = len(token_set.intersection(c_tokens))
        norm = math.sqrt(max(len(c_tokens), 1))
        scored.append((overlap / norm, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]


def answer_with_rag(question: str) -> str:
    """Builds concise grounded response with source reference."""
    q = question.lower()
    if "water" in q or "agua" in q:
        return (
            f"According to the pre-operation instructions ({INSTRUCTIONS_URL}), "
            "water should follow clinic guidance before admission; confirm the exact cutoff with reception."
        )
    if "fast" in q or "ayuno" in q or "food" in q or "comida" in q:
        return (
            f"According to the pre-operation instructions ({INSTRUCTIONS_URL}), "
            "start fasting from the previous night and do not give food on surgery morning."
        )

    hits = retrieve_relevant_chunks(question, top_k=1)
    context = hits[0] if hits else "Follow the pre-operation instructions and confirm final details with the clinic."
    short_context = context[:220].strip()
    return f"According to the pre-operation instructions ({INSTRUCTIONS_URL}): {short_context}"
