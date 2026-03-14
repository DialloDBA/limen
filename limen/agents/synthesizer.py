"""Agent chargé de produire la réponse finale consolidée."""

from __future__ import annotations

from limen.agents.base_agent import BaseAgent


class SynthesizerAgent(BaseAgent):
    """Arbitre le brouillon, la critique et la mémoire pour répondre au mieux."""

    def finalize(
        self,
        question: str,
        draft: str,
        critique_json: str | None = None,
        memory_context: str = "",
    ) -> str:
        """Produit la réponse finale la plus fiable possible."""
        prompt = (
            f"Project Memory Context:\n{memory_context}\n\n"
            f"User Question:\n{question}\n\n"
            f"Draft:\n{draft}\n\n"
            f"Critique JSON:\n{critique_json or '{}'}\n"
        )
        return self.ask(prompt)
