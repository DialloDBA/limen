"""Composant d'estimation de compétence.

Dans cette version, l'estimation est produite par un agent dédié.
Le composant se charge surtout de parser et valider la sortie.
"""

from __future__ import annotations

from limen.agents.assessor import AssessorAgent
from limen.core.schemas import CompetenceAssessment
from limen.utils.json_utils import extract_json_object


class CompetenceEstimator:
    """Adapte un agent d'évaluation à une interface métier stable."""

    def __init__(self, assessor: AssessorAgent):
        self.assessor = assessor

    def assess(self, question: str, memory_context: str = "") -> CompetenceAssessment:
        """Retourne une évaluation structurée validée par Pydantic."""
        raw_output = self.assessor.assess(question, memory_context=memory_context)
        payload = extract_json_object(raw_output)
        return CompetenceAssessment(**payload)
