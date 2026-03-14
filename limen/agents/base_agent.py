"""Classe de base de tous les agents Limen.

Les agents ne connaissent pas directement le fournisseur sous-jacent.
Ils manipulent seulement une interface provider commune.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from limen.providers.base import AIProvider


@dataclass(slots=True)
class AgentConfig:
    """Configuration générique d'un agent."""

    name: str
    system_prompt: str
    temperature: float = 0.2
    max_tokens: int | None = None
    response_format: dict[str, Any] | None = None


class BaseAgent:
    """Agent générique reposant sur un provider externe."""

    def __init__(self, provider: AIProvider, config: AgentConfig):
        self.provider = provider
        self.config = config

    def ask(self, user_input: str) -> str:
        """Envoie une requête standardisée au provider associé."""
        return self.provider.complete(
            system_prompt=self.config.system_prompt,
            user_prompt=user_input,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format=self.config.response_format,
        )
