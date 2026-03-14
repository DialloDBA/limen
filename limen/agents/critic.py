"""Agent chargé de détecter les failles d'un brouillon."""

from __future__ import annotations

from limen.agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):
    """Évalue un brouillon et renvoie une critique structurée."""

    def review(self, question: str, draft: str, memory_context: str = "") -> str:
        """Analyse la proposition initiale et renvoie une critique JSON."""
        prompt = (
            f"Project Memory Context:\n{memory_context}\n\n"
            f"User Question:\n{question}\n\n"
            f"Draft to Review:\n{draft}\n"
        )
        return self.ask(prompt)
