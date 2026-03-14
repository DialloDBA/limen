"""Schémas structurés utilisés pour standardiser les entrées et sorties de Limen."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DecisionType(str, Enum):
    """Décisions possibles du moteur de seuil."""

    ANSWER_ALONE = "answer_alone"
    CONSULT_PEERS = "consult_peers"
    DELEGATE_EXPERT = "delegate_expert"
    REFUSE_OR_ESCALATE = "refuse_or_escalate"


class CompetenceAssessment(BaseModel):
    """Évaluation de la capacité estimée du système sur une question."""

    confidence: float = Field(ge=0.0, le=1.0)
    risk: float = Field(ge=0.0, le=1.0)
    domain: str = Field(default="general")
    complexity: str = Field(default="medium")
    rationale: str = Field(default="")


class CritiquePayload(BaseModel):
    """Charge structurée produite par l'agent critique."""

    summary: str
    confirmed_errors: list[str] = Field(default_factory=list)
    likely_weaknesses: list[str] = Field(default_factory=list)
    suggested_fixes: list[str] = Field(default_factory=list)
    severity_score: int = Field(ge=0, le=10)
    revision_useful: bool = Field(default=False)


class MemoryRecord(BaseModel):
    """Entrée de mémoire persistante.

    Cette structure permet de conserver une trace lisible et rejouable
    des décisions, résultats et artefacts partagés entre agents.
    """

    key: str
    value: Any
    source: str
    tags: list[str] = Field(default_factory=list)


class LimenResult(BaseModel):
    """Résultat final renvoyé par l'orchestrateur."""

    question: str
    assessment: CompetenceAssessment
    decision: DecisionType
    draft: str | None = None
    critique: CritiquePayload | None = None
    final_answer: str
    memory_updates: list[str] = Field(default_factory=list)
