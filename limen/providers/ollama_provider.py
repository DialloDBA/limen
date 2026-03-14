"""Provider pour modèles locaux exposés via Ollama."""

from __future__ import annotations

from typing import Any

import requests

from limen.providers.base import AIProvider


class OllamaProvider(AIProvider):
    """Provider HTTP simple pour endpoints Ollama."""

    def __init__(self, model: str, endpoint: str = "http://localhost:11434/api/chat"):
        self.model = model
        self.endpoint = endpoint

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Envoie une requête synchrone à un endpoint local Ollama."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature},
        }
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens
        if response_format is not None:
            payload["format"] = response_format

        response = requests.post(self.endpoint, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
