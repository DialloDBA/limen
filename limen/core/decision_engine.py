"""Moteur de décision basé sur des seuils simples.

Cette première version privilégie la lisibilité et l'explicabilité.
Elle pourra être remplacée plus tard par un système appris ou calibré.
"""

from __future__ import annotations

from dataclasses import dataclass

from limen.core.schemas import CompetenceAssessment, DecisionType


@dataclass(slots=True)
class DecisionThresholds:
    """Seuils utilisés pour choisir le prochain comportement du système."""

    answer_confidence: float = 0.75
    consult_confidence: float = 0.45
    max_risk_for_direct_answer: float = 0.35
    max_risk_for_consultation: float = 0.75


class DecisionEngine:
    """Décide s'il faut répondre, consulter, déléguer ou escalader."""

    def __init__(self, thresholds: DecisionThresholds):
        self.thresholds = thresholds

    def decide(self, assessment: CompetenceAssessment) -> DecisionType:
        """Applique une logique de seuil déterministe et explicable."""
        if (
            assessment.confidence >= self.thresholds.answer_confidence
            and assessment.risk <= self.thresholds.max_risk_for_direct_answer
        ):
            return DecisionType.ANSWER_ALONE

        if (
            assessment.confidence >= self.thresholds.consult_confidence
            and assessment.risk <= self.thresholds.max_risk_for_consultation
        ):
            return DecisionType.CONSULT_PEERS

        if assessment.risk < 0.90:
            return DecisionType.DELEGATE_EXPERT

        return DecisionType.REFUSE_OR_ESCALATE
