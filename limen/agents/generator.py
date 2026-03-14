"""Agent chargé de produire un premier brouillon de réponse."""

from __future__ import annotations

from limen.agents.base_agent import BaseAgent


class GeneratorAgent(BaseAgent):
    """Produit une réponse initiale puis, si besoin, une version révisée."""

    def generate(self, question: str, memory_context: str = "") -> str:
        """Génère un premier brouillon en tenant compte du contexte mémoire."""
        prompt = (
            f"Project Memory Context:\n{memory_context}\n\n"
            f"User Question:\n{question}\n"
        )
        return self.ask(prompt)

    def revise(self, question: str, draft: str, critique_json: str, memory_context: str = "") -> str:
        """Produit une version révisée à partir du brouillon et de la critique."""
        prompt = (
            f"Project Memory Context:\n{memory_context}\n\n"
            f"User Question:\n{question}\n\n"
            f"Previous Draft:\n{draft}\n\n"
            f"Critique JSON:\n{critique_json}\n\n"
            "Revise the draft using the critique and preserve correct parts."
        )
        return self.ask(prompt)
