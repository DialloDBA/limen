"""Agent spécialisé dans l'évaluation de compétence et de risque."""

from __future__ import annotations

from limen.agents.base_agent import BaseAgent


class AssessorAgent(BaseAgent):
    """Produit une estimation structurée pour guider la décision."""

    def assess(self, question: str, memory_context: str = "") -> str:
        """Retourne une estimation JSON de confiance et de risque."""
        prompt = (
            f"Project Memory Context:\n{memory_context}\n\n"
            f"User Question:\n{question}\n"
        )
        return self.ask(prompt)
