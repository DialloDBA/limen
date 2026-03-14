"""Provider OpenAI-compatible.

Ce provider peut aussi fonctionner avec des endpoints compatibles OpenAI
lorsqu'un `base_url` personnalisé est fourni.
"""

from __future__ import annotations

import os
from typing import Any

from limen.providers.base import AIProvider

try:
    from openai import OpenAI
except ModuleNotFoundError:  # pragma: no cover - dépendance optionnelle en test local
    OpenAI = None


class OpenAIProvider(AIProvider):
    """Provider reposant sur le SDK OpenAI."""

    def __init__(self, model: str, api_key: str | None = None, base_url: str | None = None):
        if OpenAI is None:
            raise RuntimeError(
                "The openai package is not installed. Install requirements.txt to use OpenAIProvider."
            )
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"), base_url=base_url)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Exécute une complétion via l'API chat completions."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if response_format is not None:
            kwargs["response_format"] = response_format

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""
