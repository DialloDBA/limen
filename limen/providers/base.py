"""Interface commune à tous les providers de modèles.

L'objectif est d'éviter toute dépendance forte à un fournisseur unique.
Chaque agent manipule donc une abstraction homogène.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Contrat minimal que tout provider doit implémenter."""

    @abstractmethod
    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Retourne une complétion texte pour une paire system/user prompt."""
        raise NotImplementedError
